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


### 1) 메타(Meta)
- 날짜(Date): 2026-02-21
- 회차(Session): #02
- 작업 유형(Task Type): Spec
- 대상 파일(Target File(s)): docs/spec_template.md, docs/spec_examples.md
- 환경(Environment): Windows, Python 3.10+

### 2) 입력 요약(민감정보 제거) (Input Summary - Redacted)
- 목표(Goal): 모호한 Spec과 명확한 Spec을 비교하여 재현성 차이를 관찰한다.
- 제약사항(Constraints): 표준 라이브러리만 사용, 출력 스키마 고정, 테스트 필수.
- 엣지 케이스(Edge cases): 비정상 라인, 필드 누락, 따옴표 포함, 토큰 마스킹
- 하지 말 것(What NOT to do): 사내/독점 로그 사용 금지, 합성(샘플) 예시만 사용.

### 3) 모델 & 도구 (Model & Tools)
- 모델(Model): (예: GPT-5 / Claude / Gemini)
- 모드/도구(Mode/Tool): 채팅(Chat)
- 프롬프트 버전(Prompt Version): v1

### 4) 프롬프트(공유 가능) (Prompt - Safe to share)
- 모호 프롬프트(Vague prompt):
  (붙여넣기)
- 명확 Spec 프롬프트(Clear spec prompt):
  (붙여넣기)

### 5) 결과 요약 (Output Summary)
- 모호 프롬프트 결과(Vague output):
  - 스키마가 고정되지 않음 / 가정이 제각각임 / 테스트가 약함
- 명확 Spec 결과(Clear output):
  - 스키마 고정 / 비정상 처리 정책이 명시됨 / 테스트 포함
- 리스크(Risks):
  - 명확 Spec이라도 까다로운 파싱 규칙을 놓칠 수 있음 → 예시를 더 추가해야 함

### 6) 적용 전 검증 계획 (Verification Plan - Before Applying)
- 로컬에서 유닛 테스트 실행
- 반례/역케이스 시도:
  - latency_ms 누락
  - msg에 따옴표 포함
  - 필드 사이 공백 추가
  - token 마스킹
- 루브릭(정확성/보안/테스트)으로 리뷰

### 7) 결정 (Decision)
- 결정(Decision): 채택(Adopt)
- 이유(Why): Spec 템플릿이 재현성을 크게 향상시킨다.
- 다음 행동(Next action): 3회차에서 이 템플릿으로 실제 “Draft” 코드를 생성한다.


### 1) Meta
- Date:
- Session: #03
- Task Type: Draft
- Target File(s): labs/lab03/log_parser.py
- Environment: Windows, Python 3.10+

### 2) Input Summary (Redacted)
- Goal: 고정된 Spec을 기반으로 검증 가능한 초안(Draft) 구현을 생성한다.
- Constraints: 시그니처 고정, 스키마 고정, 에러 dict 형식 고정
- Edge cases: 비정상 라인, 필드 누락, 추가 공백, 토큰 마스킹
- What NOT to do: 외부 의존성 금지, 숨겨진 가정 금지

### 3) Model & Tools
- Model:
- Mode/Tool:
- Prompt Version: v1

### 4) Prompt (Safe to share)
(붙여넣기) Draft 생성 프롬프트

### 5) Output Summary
- Implemented:
  - mask_tokens: (요약)
  - parse_line: (요약)
- Risks / TODOs:
  - TODO: (예: 여러 token 처리, msg 이스케이프 처리 등)

### 6) Verification Plan (Before Applying)
- main() 데모 실행
- 수동 반례 테스트:
  - divide 케이스는 해당 없음
  - 비정상 라인 / latency_ms 누락 / 정수 변환 실패
  - msg에 따옴표 포함(향후)
- Next: 이후 회차에서 유닛 테스트 추가

### 7) Decision
- Decision: Adopt / Modify / Reject
- Why:
- Next action: