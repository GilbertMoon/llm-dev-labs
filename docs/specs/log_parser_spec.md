# 예시 B (템플릿을 적용한 명확 Spec)

## 1) 무엇(목표)
- 한 문장 목표: 애플리케이션 로그를 파싱하여, 후속 분석을 위한 구조화된 JSON Lines 형식으로 출력한다.
- 왜 필요한가: 에러 개수를 집계하고, 엔드포인트(path)별 응답 시간을 측정하고 싶다.

## 2) 제약사항
- 언어: Python 3.10+
- 외부 의존성: 없음(표준 라이브러리만 사용)
- 성능: 노트북 환경에서 10만(100k) 라인을 수 초 내 처리해야 함(스트림 처리)
- 보안: 로그에 비밀정보가 있을 수 있으므로, 토큰(token)을 마스킹해야 함

## 3) 입출력(I/O)
### 입력(Inputs)
- 입력 출처: 멀티라인 문자열 1개 OR 텍스트 파일 경로 1개
- 입력 형식(각 라인):
  - `[YYYY-MM-DD HH:MM:SS] LEVEL service=<name> user=<id> path=<url> status=<int> latency_ms=<int> msg="<free text>"`
- 입력 예시(3줄):
  - `[2026-02-21 10:11:12] INFO service=api user=42 path=/login status=200 latency_ms=31 msg="ok"`
  - `[2026-02-21 10:11:13] WARN service=api user=42 path=/login status=429 latency_ms=12 msg="rate limit"`
  - `[2026-02-21 10:11:14] ERROR service=api user=42 path=/pay status=500 latency_ms=201 msg="db timeout token=abcd-1234"`

### 출력(Outputs)
- 출력 형식: JSON Lines (입력 라인 1개당 JSON 객체 1개)
- 각 출력 JSON은 다음 키를 **정확히(EXACT)** 포함해야 함:
  - timestamp (string)
  - level (string)
  - service (string)
  - user (int)
  - path (string)
  - status (int)
  - latency_ms (int)
  - message (string)
  - masked (bool)  // token 형태 문자열이 마스킹되면 true
- 출력 예시(ERROR 라인 기준):
  - {"timestamp":"2026-02-21 10:11:14","level":"ERROR","service":"api","user":42,"path":"/pay","status":500,"latency_ms":201,"message":"db timeout token=[REDACTED]","masked":true}

- 에러 출력 형식:
  - 라인이 유효하지 않으면 **절대 크래시하지 말 것**
  - 아래 형식의 에러 JSON을 출력:
    - {"error": true, "raw": "<original line>", "reason": "<short reason>"}

## 4) 엣지 케이스
1) 필드 사이에 공백이 추가로 들어가는 경우
2) 필드 누락(예: latency_ms 없음)
3) user/status/latency가 정수가 아닌 경우
4) msg에 따옴표(") 또는 등호(=)가 포함되는 경우
5) 파일이 매우 큰 경우(라인 단위 스트리밍 처리)

## 5) 하지 말 것(비목표 / 금지사항)
- 전체 로그 관리 시스템을 만들지 말 것
- 환경 변수나 비밀정보를 읽지 말 것
- DB에 저장하지 말 것(문자열 반환/출력만)

## 6) 수용 기준(완료 정의)
- AC1: 유효한 라인은 필수 키와 올바른 타입을 갖는 JSON을 생성한다.
- AC2: 유효하지 않은 라인은 크래시 없이 에러 JSON을 생성한다.
- AC3: token 형태 문자열(예: `token=...`)은 `[REDACTED]`로 마스킹된다.
- AC4: 입력이 파일 경로/멀티라인 문자열 두 경우 모두 동작한다.
- AC5: 최소 10개의 유닛 테스트 케이스(정상/엣지/비정상)를 포함한다.

## 7) 테스트 체크리스트
- 정상: 유효한 3줄 입력
- 엣지: 공백 추가, msg에 따옴표 포함
- 비정상: 필드 누락, 정수 파싱 실패, 빈 줄