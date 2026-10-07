# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- edge: 모듈 간 의존 간선. kind runtime/type_only/inherits, 표면 초과 경로 extra, 가져온 이름 names, 층 단위 import 표시
- initializer: lnt init. 프로토콜 문서 복사, CLAUDE.md, 훅 병합, 스킬 설치
- module_ref: ln 모듈 하나. 이름, 스코프, 선언 층, 파일 목록, 외부 의존 여부
- project_layout: 프로젝트 루트와 src/<pkg> 탐색. 층 폴더 이름 규칙 LAYER_RE
- raw_import: 해석 전 import 문 하나. target, names, kind, external
- signature_extractor: 모듈 파일의 공개 클래스와 타입 별칭, 클래스 메서드 시그니처, 층 __init__ 의 이름-모듈 매핑을 ast 로 추출
- violation: 규칙 위반 C1~C4 레코드와 포맷, 종류별 풀이

## l1
- graph: 모듈 그래프. 계산 층, 역의존, 인터페이스 경유 blast, 순환 탐지
- scanner: src/<pkg> 를 훑어 모듈과 간선 생성. 상대/절대/층 단위 import 해석, TYPE_CHECKING 구분
- surface: 모듈, 중첩 모듈, 층의 표면 계산과 __init__.py 생성. 중첩 모듈은 안쪽 맨 위 층을 공개

## l2
- blaster: blast 결과 텍스트 보고서
- checker: C1 방향, C2 표면(표면 너머, 표면에 없는 이름, 층 안 이름 겹침), C3 층 일치, C4 순환 검사
- doc_generator: layerinfo 와 __init__.py 생성과 검사. 예전 층별 문서 알림, moduleinfo stamp 는 호환용
- reviewer: lnt review. 위반이 아닌 점검 대상. 우회 의존, 아무도 쓰지 않는 모듈, 클래스가 여럿인 파일, 숨은 타입 노출
- signature_lister: lnt sig. 층이나 모듈의 공개 시그니처를 문서 없이 그 자리에서 계산

## l3
- hook_runner: Claude Code 훅 진입. stdin JSON 해석, exit 2 / additionalContext 채널 선택
- mover: lnt move. 모듈 층 이동, import 재작성, tests 미러, __init__ 와 문서 재생성

## l4
- cli: lnt 명령줄. check, blast, map, sig, review, doc, move, hook, init
<!-- lnt:generated:end -->

## Notes

의존은 항상 아래로만. l4 cli 가 진입점이며 모든 하위를 조립한다.
패키지 루트 __init__ 과 __main__ 은 사람이 쓴다. 나머지 __init__.py 는 lnt doc 이 만든다.
