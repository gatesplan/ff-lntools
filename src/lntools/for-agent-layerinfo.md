# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- edge: 모듈 간 의존 간선. kind runtime/type_only/inherits, 표면 초과 경로 extra
- module_ref: ln 모듈 하나. 이름, 스코프, 선언 층, 파일 목록, 외부 의존 여부
- project_layout: 프로젝트 루트와 src/<pkg> 탐색. LAYER_RE
- signature_extractor: 모듈 __init__ 공개 이름과 클래스 메서드 시그니처를 ast 로 추출
- violation: 규칙 위반 C1~C4 레코드와 포맷

## l1
- graph: 모듈 그래프. 계산 층, 역의존, 인터페이스 경유 blast, 순환 탐지
- scanner: src/<pkg> 를 훑어 모듈과 간선 생성. 상대/절대/층 단위 import 해석, TYPE_CHECKING 구분

## l2
- blaster: blast 결과 텍스트 보고서
- checker: C1 방향, C2 표면, C3 층 일치, C4 순환 검사
- doc_generator: layerinfo/layerinfo-ln 생성과 검사, moduleinfo sources hash stamp/stale

## l3
- hook_runner: Claude Code 훅 진입. stdin JSON 해석, exit 2 / additionalContext 채널 선택

## l4
- cli: lnt 명령줄. check, blast, map, doc, hook
<!-- lnt:generated:end -->

## Notes

의존은 항상 아래로만. l4 cli 가 진입점이며 모든 하위를 조립한다.
