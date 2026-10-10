# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- import_reader: 소스 파일이 무엇에 기대는지 읽어 낸다
- import_rewriter: 모듈이 옮겨 갈 때 그 모듈을 가리키는 import 를 맞춘다
- signature_extractor: 소스 파일에 무엇이 정의되어 있는지 읽어 낸다
- surface_renderer: 표면 파일이 어떤 모양인지 정한다

## l1
- python_language: Python 의 읽기와 쓰기를 lnt 의 언어 약속에 맞춰 묶는다
<!-- lnt:generated:end -->

## Notes

바깥의 l0.language 약속을 구현한다. 안쪽 모듈은 바깥 l0 의 RawImport 만 쓴다.
