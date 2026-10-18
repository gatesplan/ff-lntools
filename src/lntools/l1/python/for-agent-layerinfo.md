# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- import_reader: Python 파일을 받아, 파일 안의 import 문이 가리키는 모듈과 이름을 돌려준다
- import_rewriter: Python 파일과 모듈의 옛 위치, 새 위치를 받아, 옛 위치를 가리키는 import 문을 새 위치로 고친다
- signature_extractor: 모듈 폴더를 받아 공개 클래스와 공개 메서드의 시그니처를 돌려준다
- surface_renderer: 표면 종류와 공개 이름 목록을 받아 __init__.py 의 내용을 돌려준다

## l1
- python_language: 아래 층 모듈들을 조립해 언어 인터페이스를 Python 용으로 구현한다
<!-- lnt:generated:end -->

## Notes

바깥의 l0.language 약속을 구현한다. 안쪽 모듈은 바깥 l0 의 RawImport 만 쓴다.
