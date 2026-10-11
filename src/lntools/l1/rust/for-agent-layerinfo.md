# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- path_resolver: Rust 경로가 패키지의 어느 모듈을 가리키는지 푼다
- surface_renderer: 표면 파일이 어떤 모양인지 정한다

## l1
- source_parser: Rust 소스를 문법 트리로 읽는다

## l2
- signature_extractor: 소스 파일에 무엇이 정의되어 있는지 읽어 낸다
- use_reader: 소스 파일이 무엇에 기대고 어디에 덧붙는지 읽어 낸다
- use_rewriter: 모듈이 옮겨 갈 때 그 모듈을 가리키는 경로를 맞춘다

## l3
- rust_language: Rust 의 읽기와 쓰기를 lnt 의 언어 약속에 맞춰 묶는다
<!-- lnt:generated:end -->

## Notes

바깥의 l0.language 약속을 구현한다. 외부 패키지 tree-sitter 는 source_parser 만 쓴다.
경로 규칙(C5)과 매크로 규칙은 아직 정하지 않아 검사하지 않는다. 매크로가 펼쳐져 만드는 코드는 보지 못한다.
