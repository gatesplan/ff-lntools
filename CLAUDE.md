# 프로젝트 프로토콜

## 구조 규칙

이 프로젝트는 ln-structure 를 따른다. 규칙과 해결 방법은 필요할 때 `.claude/for-agent-codingprotocol-ln-structure.md` 를 읽는다.

## 프로젝트 설명

`ff-lntools`. ln-structure 프로젝트용 정적 검사(`lnt check`), 영향 범위(`lnt blast`),
문서 생성(`lnt doc`), Claude Code 훅(`lnt hook`). 표준 라이브러리만 사용. Python 3.10+.

이 프로젝트 자체가 ln-structure 이며 자기 자신을 검사한다. 훅이 `.claude/settings.json` 에 등록되어 있다.

- 소스: `src/lntools/l0..l4`. 모듈 목록은 `src/lntools/for-agent-layerinfo.md`
- 테스트: `tests/` 미러 구조. fixture 는 `tests/fixtures/sample` (의도된 위반 13건이 심어진 샘플)
- 실행: `python -m pytest -q`, `lnt check`, `lnt doc --check`. `lnt` 는 이 저장소의 편집 설치라 소스를 그대로 돈다
- 개발 env: conda `py312`. 배포는 `uv tool install -e . --python 3.14` (사용자 bin 의 `lnt`). 훅은 `lnt hook ...` 으로 부른다
- 이 셸의 `python` 은 conda env 를 활성화하지 않으면 Microsoft Store 바로가기다. 개발 명령은 py312 의 python 으로 돌린다
- conda env 에는 lntools 를 깔지 않는다. 깔려 있으면 그 env 를 활성화했을 때 그쪽 `lnt` 가 먼저 잡힌다. 옮기는 방법은 `MIGRATION.md`

## 추가 규칙

- fixture 의 위반 목록을 바꾸면 `tests/l2/checker/test_checker.py` 의 기대값을 같이 바꾼다
- 출력 문자열은 ASCII 와 한글만. 훅 경로는 UTF-8 로 고정되어 있다
- 문서 수정 후 `lnt doc --check` 가 0 이어야 한다
