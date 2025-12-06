# Pipeline Orchestrator Quick Reference

## Overview

The Pipeline Orchestrator automates the Spec-Driven Development workflow after specification creation. It executes 6 phases with user approval gates between each.

**Command:** `/sp.autopilot`

---

## Basic Usage

### 1. Full Pipeline (From Spec to Implementation)

```bash
# Step 1: Create specification
/sp.specify "Add task editing feature"

# Step 2: Run automated pipeline
/sp.autopilot

# Pipeline executes:
# → Phase 1: Spec Validation (6-item checklist)
# → Phase 2: Clarification (if needed)
# → Phase 3: Planning (/sp.plan)
# → Phase 4: ADR Detection (suggest only)
# → Phase 5: Task Breakdown (/sp.tasks + /sp.analyze)
# → Phase 6: Implementation (/sp.implement)

# Step 3: Commit and create PR (manual)
/sp.git.commit_pr
```

---

## Advanced Usage

### Resume from Specific Phase

```bash
# Resume from planning (skip validation/clarification)
/sp.autopilot --resume planning

# Resume from tasks (spec and plan already done)
/sp.autopilot --resume tasks

# Resume from implementation only
/sp.autopilot --resume implementation
```

**Supported Resume Points:**
- `validation` - Start from spec validation
- `clarification` - Start from clarification questions
- `planning` - Start from plan generation
- `adr` - Start from ADR detection
- `tasks` - Start from task breakdown
- `implementation` - Start from implementation

### Skip Specific Phases

```bash
# Skip ADR detection entirely
/sp.autopilot --skip-adr

# Combine with resume
/sp.autopilot --resume planning --skip-adr
```

---

## Approval Gates

The pipeline **pauses for user approval** after each phase:

```
Phase 3 complete: Plan generated with 5 architecture decisions. Proceed to ADR detection?

Options:
→ Yes, continue pipeline
→ No, let me review manually
→ Skip next phase
```

**User Responses:**
- **Yes, continue** → Auto-proceed to next phase
- **No, let me review** → Exit pipeline (can resume later)
- **Skip next phase** → Continue but skip upcoming phase

---

## Phase Details

### Phase 1: Spec Validation

**Purpose:** Ensure spec meets quality standards

**Checklist (6 items):**
1. Intent is clear (unfamiliar reader can understand)
2. Constraints are testable (not vague)
3. Success criteria are SMART
4. Non-goals are explicit
5. No implementation details leaked
6. Readable by another person

**Results:**
- **PASS** (all items) → Skip clarification, proceed to planning
- **WARN** (1-2 items fail) → Suggest clarification, let user decide
- **BLOCK** (≥3 items fail) → Must fix before proceeding

---

### Phase 2: Clarification (Conditional)

**Trigger:** Runs if validation returned WARN or BLOCK

**Questions Asked:**
1. Is the feature scope clear?
2. Would a planner know what feature structure to design?
3. Are there any remaining ambiguities?
4. Is this specification ready for planning?

**Output:** Updates spec.md with answers, re-runs validation

---

### Phase 3: Planning

**Action:** Invokes `/sp.plan` to generate architecture

**Artifacts Created:**
- `specs/{feature}/plan.md` - Technical architecture
- Architecture decisions documented

**Validation:** Checks against constitution constraints

---

### Phase 4: ADR Detection

**Purpose:** Identify architecturally significant decisions

**3-Part Test:**
- **Impact:** Long-term consequences? (score ≥ 7/10)
- **Alternatives:** Multiple options considered? (≥ 2)
- **Scope:** Cross-cutting influence? (score ≥ 6/10)

**If ADR-worthy decision detected:**
```
📋 Architectural decision detected: state-management-approach
Run `/sp.adr state-management-approach` to document

Options:
→ Yes, pause for ADR creation
→ No, skip ADRs for now
→ Create ADRs later (continue pipeline)
```

**Behavior:**
- **Yes** → Pipeline pauses, user runs `/sp.adr {title}`, then resumes with `/sp.autopilot --resume tasks`
- **No/Later** → Continue to Phase 5

---

### Phase 5: Task Breakdown

**Actions:**
1. Invokes `/sp.tasks` - Generate dependency-ordered tasks
2. Invokes `/sp.analyze` - Cross-artifact consistency check

**Artifacts Created:**
- `specs/{feature}/tasks.md` - Implementation task breakdown

**Validation:** Ensures spec ↔ plan ↔ tasks alignment

---

### Phase 6: Implementation

**Action:** Invokes `/sp.implement`

**Process:**
- Execute each task in dependency order
- Write tests (TDD: red → green → refactor)
- Validate against acceptance criteria
- Run full test suite after each task

**Completion:** All tasks done, all tests passing

---

## Error Handling

### Auto-Retry on Failure

If any phase fails, the pipeline **auto-retries once**:

```
⚠️  Phase 3 failed: template file not found
🔄 Auto-retrying (attempt 2/2)...
```

**Outcomes:**
- **Retry succeeds** → Continue to next phase
- **Retry fails** → Show recovery options and pause

### Recovery Options

```
❌ Phase 3 failed after 2 attempts: template file not found

Recovery options:
- Fix manually and resume with `/sp.autopilot --resume planning`
- Restart pipeline from beginning: `/sp.autopilot`
- Exit and debug issue manually
```

---

## Pipeline Reports

### Execution Report (on completion)

```markdown
# Pipeline Execution Report: 002-edit-task

## Timeline
- Started: 2025-12-06T10:30:00Z
- Completed: 2025-12-06T10:55:00Z
- Total Duration: 25 minutes

## Phase Results
| Phase          | Status | Duration | Issues |
|----------------|--------|----------|--------|
| Validation     | PASS   | 2m       | 0      |
| Clarification  | SKIP   | -        | -      |
| Planning       | PASS   | 5m       | 0      |
| ADR Detection  | WARN   | 1m       | 2 suggested |
| Tasks          | PASS   | 3m       | 0      |
| Implementation | PASS   | 14m      | 0      |

## Artifacts Generated
- specs/002-edit-task/plan.md (created)
- specs/002-edit-task/tasks.md (created)
- src/task_editor.py (created)
- tests/test_task_editor.py (created)

## Next Steps
1. Review implementation
2. Run /sp.git.commit_pr to create PR
3. Optional: Create 2 suggested ADRs
```

### PHR Creation (automatic)

After pipeline completes, a PHR is auto-created:

**Location:** `history/prompts/{feature}/NNNN-pipeline-execution-{feature}.misc.prompt.md`

**Contents:**
- Full user command with arguments
- Pipeline execution log
- Phase-by-phase results
- Artifacts generated
- User decisions at approval gates
- Errors and retry attempts

---

## Configuration (Optional)

The pipeline works with sensible defaults. To customize behavior, create:

**File:** `.specify/config/pipeline.json`

**Example Customizations:**

```json
{
  "pipeline": {
    "skip_phases": [],                    // Auto-skip phases
    "auto_approve_phases": ["validation"], // No gate for these
    "require_approval_phases": ["implementation"]
  },
  "validation": {
    "max_clarifications": 3,              // [NEEDS CLARIFICATION] limit
    "block_threshold": 3                  // Failures before blocking
  },
  "adr": {
    "enabled": true,                      // Enable ADR detection
    "significance_thresholds": {
      "impact_score": 7.0,                // 0-10 scale
      "min_alternatives": 2,
      "scope_score": 6.0
    }
  },
  "implementation": {
    "test_strategy": "tdd",               // tdd | test-after | no-tests
    "test_coverage_threshold": 80
  }
}
```

**Note:** Configuration is **optional**. Pipeline uses defaults if file doesn't exist.

---

## Troubleshooting

### "No spec.md found for current feature"

**Cause:** `/sp.autopilot` run before `/sp.specify`

**Fix:**
```bash
/sp.specify "your feature description"
/sp.autopilot
```

---

### "Cannot resume from 'tasks' - missing required artifacts"

**Cause:** Trying to resume from tasks phase without plan.md

**Fix:**
```bash
# Option 1: Resume from earlier phase
/sp.autopilot --resume planning

# Option 2: Run missing command manually
/sp.plan
/sp.autopilot --resume tasks
```

---

### Pipeline Paused Mid-Execution

**Cause:** User selected "No, let me review" at approval gate

**Resume:**
```bash
# Continue from where you left off
/sp.autopilot --resume {next-phase}

# Or restart from beginning
/sp.autopilot
```

---

### Phase Failed After Auto-Retry

**Example:**
```
❌ Phase 3 failed after 2 attempts: constitution.md not found
```

**Fix:**
1. Debug the issue (e.g., create missing file)
2. Resume from failed phase:
   ```bash
   /sp.autopilot --resume planning
   ```

---

## Best Practices

### 1. Review Spec Before Running Pipeline

Always manually review spec.md before running `/sp.autopilot`:
- Check for `[NEEDS CLARIFICATION]` markers
- Verify user stories are clear
- Ensure edge cases are documented

### 2. Use Resume for Iterative Refinement

If you need to tweak plan.md or tasks.md manually:
```bash
/sp.autopilot --resume tasks  # Skip re-running planning
```

### 3. Create ADRs for Significant Decisions

When pipeline suggests ADRs, create them immediately:
```bash
# Pipeline suggests: state-management-approach
/sp.adr state-management-approach

# Then resume pipeline
/sp.autopilot --resume tasks
```

### 4. Review Implementation Before Committing

Pipeline completes implementation but **does not auto-commit**:
```bash
# Review changes first
git diff

# Then commit and create PR
/sp.git.commit_pr
```

---

## Workflow Examples

### Example 1: Happy Path (No Issues)

```bash
$ /sp.specify "Add ability to mark tasks as high priority"
✅ Spec created: specs/003-priority-tasks/spec.md

$ /sp.autopilot
Phase 1: Validation PASS → Approve? Yes
Phase 2: Clarification SKIPPED
Phase 3: Planning PASS → Approve? Yes
Phase 4: ADR Detection (1 suggested) → Create later
Phase 5: Tasks PASS → Approve? Yes
Phase 6: Implementation PASS (10/10 tests)

✅ Pipeline complete! Next: /sp.git.commit_pr
```

---

### Example 2: Spec Validation Failures

```bash
$ /sp.autopilot
Phase 1: Validation WARN (2 items failed)
  - Non-goals not explicit
  - Implementation details leaked ("API endpoints")

Proceed to clarification? Yes

Phase 2: Clarification
  Q1: Is the feature scope clear? → Yes, CRUD operations only
  Q2: Would planner know structure? → Yes, follows 001-add-task pattern
  Q3: Remaining ambiguities? → None
  Q4: Ready for planning? → Yes

✅ Spec updated, re-validated: PASS
Proceed to planning? Yes

[Continue normally...]
```

---

### Example 3: Pausing for ADR Creation

```bash
$ /sp.autopilot --resume planning
Phase 3: Planning PASS
  Generated plan.md with 5 decisions

Phase 4: ADR Detection
  📋 Detected 2 ADR-worthy decisions:
     1. task-priority-data-model
     2. priority-filtering-strategy

  Create ADRs now? Yes, pause for ADR creation

⏸️  Pipeline paused. Please run:
   /sp.adr task-priority-data-model
   /sp.adr priority-filtering-strategy

Resume with: /sp.autopilot --resume tasks

$ /sp.adr task-priority-data-model
✅ ADR created: history/adr/0001-task-priority-data-model.md

$ /sp.adr priority-filtering-strategy
✅ ADR created: history/adr/0002-priority-filtering-strategy.md

$ /sp.autopilot --resume tasks
Phase 5: Tasks PASS → Approve? Yes
Phase 6: Implementation PASS

✅ Pipeline complete!
```

---

### Example 4: Phase Failure with Auto-Retry

```bash
$ /sp.autopilot --resume tasks
Phase 5: Tasks executing...

⚠️  Phase 5 failed: tasks-template.md not found
🔄 Auto-retrying (attempt 2/2)...

✅ Phase 5 succeeded on retry

Proceed to implementation? Yes

[Continue normally...]
```

---

## Summary

**Single Command Workflow:**
```bash
/sp.specify "feature description"  # Create spec
/sp.autopilot                      # Automate rest of workflow
/sp.git.commit_pr                  # Commit and PR (manual)
```

**Key Benefits:**
- ⏱️  **Time Savings:** 23-40% reduction (5-10 min per feature)
- ✅ **Quality Gates:** Validation before every phase
- 🔄 **Resilience:** Auto-retry on failures
- 📋 **Traceability:** Automatic PHR documentation
- 🎯 **User Control:** Approval gates at every phase transition

**No Automation Of:**
- Spec creation (use spec-architect via `/sp.specify`)
- ADR creation (suggested only, user runs `/sp.adr`)
- Git operations (user runs `/sp.git.commit_pr`)

---

**For detailed agent logic, see:** `.claude/agents/pipeline-orchestrator.md`
**For command internals, see:** `.claude/commands/sp.autopilot.md`
**For configuration options, see:** `.specify/config/pipeline.example.json`
