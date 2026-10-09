# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- edge: 한 모듈이 다른 모듈에 기대는 관계 하나를 나타낸다
- initializer: 프로젝트가 ln 프로토콜을 쓰기 시작하게 한다
- module_ref: ln 모듈 하나가 무엇인지 나타낸다
- project_layout: 어디가 ln 프로젝트이고 그 패키지인지 알아낸다
- raw_import: 아직 모듈로 풀지 않은 import 하나를 나타낸다
- signature_extractor: 소스 파일이 바깥에 무엇을 내놓는지 읽어 낸다
- violation: 규칙 위반 하나와 그 풀이를 나타낸다

## l1
- graph: 모듈 사이 의존 관계에 대한 물음에 답한다
- scanner: 소스 코드를 모듈과 의존 관계로 옮긴다
- surface: 모듈, 층, 패키지가 바깥에 무엇을 공개하는지 정한다

## l2
- blaster: 한 모듈을 바꿀 때 영향이 어디까지 가는지 보고한다
- checker: 프로젝트가 ln 규칙을 지키는지 판정한다
- doc_generator: 생성되는 문서와 __init__ 이 코드와 어긋나지 않게 한다
- reviewer: 위반은 아니지만 사람이 볼 만한 구조를 짚는다
- signature_lister: 공개 시그니처를 문서 없이 필요할 때 보여 준다

## l3
- hook_runner: Claude Code 가 편집하는 순간에 lnt 의 판단을 전한다
- map_exporter: 모듈 지도를 기계가 읽을 형태로 내놓는다
- mover: 모듈을 다른 층으로 옮겨도 프로젝트가 그대로 동작하게 한다

## l4
- cli: 사람과 에이전트가 lnt 를 명령으로 쓰게 한다
<!-- lnt:generated:end -->

## Notes

의존은 항상 아래로만. l4 cli 가 진입점이며 모든 하위를 조립한다.
__init__.py 는 패키지 루트까지 모두 lnt doc 이 만든다. __main__.py 는 진입 스크립트라 다른 코드처럼 둔다.
