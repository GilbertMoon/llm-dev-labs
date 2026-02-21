# LLM Development Labs

Hands-on labs for building a reproducible AI-augmented development workflow.

## Folder structure
- labs/      : per-session hands-on exercises
- prompts/   : prompt templates (driver/reviewer/tester, etc.)
- docs/      : ADR, runbook, policies
- quality/   : checklists, rubrics, gates
- logs/      : AI usage logs (reproducibility)

## Rules (important)
- Do NOT paste secrets, tokens, customer data, or proprietary code.
- Always log prompts + outputs summary + verification plan.
- Prefer structured outputs (JSON, checklist) to reduce ambiguity.


# AI Usage Log (Reproducible)

> Rule: Never paste secrets, tokens, customer data, or proprietary code.
> If needed, redact / mask before sending to any model.

---

## Entry Template

### 1) Meta
- Date:
- Session:
- Task Type: (Spec / Draft / Refine / Doc / Review / Test / Debug)
- Target File(s):
- Environment: (OS, language, runtime, framework)

### 2) Input Summary (Redacted)
- Goal (1~2 lines):
- Constraints:
- Edge cases to consider:
- What NOT to do: (security / scope / style)

### 3) Model & Tools
- Model:
- Mode/Tool: (ChatGPT / Claude / Gemini / IDE assistant / etc.)
- Temperature (if applicable):
- Prompt Version: (v1/v2…)

### 4) Prompt (Safe to share)
Paste the exact prompt you used (no secrets).

### 5) Output Summary
- Key suggestions:
- Potential risks / unknowns:
- Any TODOs / assumptions from the model:

### 6) Verification Plan (Before Applying)
- Checks to run (tests / lint / typecheck):
- Counterexamples to try:
- Review checklist items:

### 7) Decision
- Decision: (Adopt / Modify / Reject)
- Why:
- Next action:

### 1) Meta
- Date: 2026-02-21
- Session: #01
- Task Type: Refine (proposal only)
- Target File(s): labs/lab01/calc.py
- Environment: Windows 10/11, Python 3.x

### 2) Input Summary (Redacted)
- Goal: Ask for refactoring ideas to make calc.py safer and more testable.
- Constraints: No external deps, keep valid-input behavior.
- Edge cases: divide by zero, empty CSV, spaces, non-numeric tokens, trailing commas.
- What NOT to do: Do not rewrite yet; do not over-engineer.

### 3) Model & Tools
- Model: (e.g., GPT / Claude / Gemini)
- Mode/Tool: Chat interface
- Prompt Version: v1

### 4) Prompt (Safe to share)
(붙여넣기) 위 프롬프트 전문

### 5) Output Summary
- Key suggestions:
  - Add input validation for divide(b==0) and type checks.
  - Make parse_and_sum robust: strip spaces, handle empty items, clear error messages.
  - Consider type hints and docstrings.
- Potential risks / unknowns:
  - Behavior changes for invalid inputs (decide policy).
  - Exceptions: ValueError vs custom exception.
- TODOs / assumptions:
  - Define “invalid csv token” policy: skip? fail? collect errors?

### 6) Verification Plan (Before Applying)
- Checks to run:
  - Add unit tests first, then refactor safely.
  - Run tests for edge/invalid cases.
- Counterexamples to try:
  - divide(10,0)
  - parse_and_sum("")
  - parse_and_sum("1, 2, 3")
  - parse_and_sum("1,,3")
  - parse_and_sum("1,a,3")
- Review checklist:
  - No behavior change for valid inputs
  - Clear exceptions
  - Tests cover edge cases

### 7) Decision
- Decision: Modify
- Why: Need to define policy for invalid inputs before implementing.
- Next action: In Session #02, write a Spec that defines invalid-input policy.