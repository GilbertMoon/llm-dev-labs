# Draft 수용 기준 (Lab #03)

초안(Draft)은 **검증 가능(verifiable)** 할 때에만 수용된다.

## 필수(Must-have, 강제 요구사항)
1) 고정 API:
   - parse_line(line: str) -> dict
   - parse_text(text: str) -> list[dict]
   - parse_file(path: str) -> list[dict]

2) 고정 출력 형식:
   - 정상(Valid) 결과 dict는 다음 키를 **정확히(EXACT)** 포함해야 한다:
     timestamp, level, service, user, path, status, latency_ms, message, masked
   - 비정상(Invalid) 결과 dict는 **정확히(EXACTLY)** 다음과 같아야 한다:
     {"error": true, "raw": "<line>", "reason": "<short reason>"}

3) 무크래시 정책(No crash policy):
   - 비정상 라인은 호출자에게 예외를 던지면 안 된다.

4) TODO 정책:
   - 파싱 동작이 모호하거나 위험할 경우, TODO를 포함하고 가장 안전한 기본값을 선택한다.

## 권장(Should-have)
5) 파싱은 추가 공백에 대해 관대해야 한다.
6) 토큰 마스킹은 최소 1개 이상의 "token=..." 부분 문자열에 대해 동작해야 한다.
7) main() 데모가 실행되며 JSON Lines를 출력해야 한다.

## 거절 조건(Reject if)
- 함수 시그니처 또는 스키마 키를 변경함
- 타입이 일관되지 않게 반환됨(예: user가 어떤 경우엔 문자열)
- 비정상 입력에서 크래시함
- 불확실성을 숨김(TODO 없음, 그런데 동작이 불명확함)