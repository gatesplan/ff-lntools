# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- path_resolver: Rust 경로를 받아, 경로가 가리키는 패키지 안 모듈과 이름을 돌려준다
- surface_renderer: 표면 종류와 공개 이름 목록을 받아 mod.rs 나 lib.rs 의 내용을 돌려준다

## l1
- source_parser: Rust 파일을 받아 문법 트리를 돌려준다

## l2
- signature_extractor: 모듈 폴더를 받아 공개 항목과 공개 메서드의 시그니처를 돌려준다
- use_reader: Rust 파일을 받아, 파일 안의 use 가 가리키는 모듈과 impl 블록의 위치를 돌려준다
- use_rewriter: Rust 파일과 모듈의 옛 위치, 새 위치를 받아, 옛 위치를 가리키는 use 경로를 새 위치로 고친다

## l3
- rust_language: 아래 층 모듈들을 조립해 언어 인터페이스를 Rust 용으로 구현한다
<!-- lnt:generated:end -->

## Notes

바깥의 l0.language 약속을 구현한다. 외부 패키지 tree-sitter 는 source_parser 만 쓴다.
경로 규칙(C5)과 매크로 규칙은 아직 정하지 않아 검사하지 않는다. 매크로가 펼쳐져 만드는 코드는 보지 못한다.
