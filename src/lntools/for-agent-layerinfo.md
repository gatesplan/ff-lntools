# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- edge: 모듈 사이의 import 관계 하나를 나타내는 자료형
- initializer: 프로젝트 경로를 받아 ln 프로토콜 문서와 Claude Code 훅 설정을 설치한다
- language: 언어마다 다르게 구현해야 하는 작업을 정의한 인터페이스
- module_ref: ln 모듈 하나의 위치와 구성을 나타내는 자료형
- project_layout: 파일이나 폴더 경로를 받아 가까운 ln 프로젝트의 루트와 패키지 폴더를 돌려준다
- violation: 규칙 위반 하나를 나타내는 자료형

## l1
- graph: 모듈과 import 관계를 받아 계산 층, 순환, 영향받는 상위 모듈을 돌려준다
- python: 언어 인터페이스의 Python 구현
- rust: 언어 인터페이스의 Rust 구현
- scanner: 패키지를 받아 모듈 목록과 import 관계를 돌려준다
- surface: 모듈 목록을 받아 각 표면 파일의 공개 이름과 파일 내용을 돌려준다

## l2
- blaster: 모듈 이름을 받아, 모듈을 바꿀 때 영향받는 상위 모듈 목록을 돌려준다
- checker: 의존 그래프와 표면을 받아 ln 규칙(C1~C7) 위반 목록을 돌려준다
- doc_generator: 패키지를 받아 모듈 지도와 표면 파일을 쓰고, 저장본과 다른 파일 목록을 돌려준다
- reviewer: 의존 그래프를 받아, 규칙 위반은 아니지만 책임 배치가 의심스러운 곳의 질문 목록을 돌려준다
- signature_lister: 층이나 모듈 이름을 받아 공개 시그니처 목록을 돌려준다

## l3
- hook_runner: Claude Code 훅 입력을 받아 세션에 넣을 모듈 지도나 위반 메시지를 출력한다
- map_exporter: 패키지를 받아 지도 도구용 JSON 을 돌려준다
- mover: 모듈 이름과 목표 층을 받아 모듈 폴더를 옮기고, 옮긴 모듈을 가리키는 import 경로를 고친다

## l4
- cli: 명령줄 인자대로 lnt 명령을 실행하고 종료 코드를 돌려준다
<!-- lnt:generated:end -->

## Notes

의존은 항상 아래로만. l4 cli 가 진입점이며 모든 하위를 조립한다. 언어 구현(l1.python, l1.rust)을 고르는 곳도 cli 하나다.
언어마다 다른 일(소스 읽기, 덧붙이기 읽기, 표면 파일 모양, import 고치기, 언어 설정 파일, 위반 풀이)은 l0.language 의 약속을 거친다. 나머지 모듈은 언어를 모른다.
__init__.py 는 패키지 루트까지 모두 lnt doc 이 만든다. __main__.py 는 진입 스크립트라 다른 코드처럼 둔다.
