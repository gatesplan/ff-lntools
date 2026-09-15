# 프로젝트 프로토콜

## 구조 및 코딩 규칙

프로토콜 문서는 프로젝트 루트 기준 `.claude/`에서 찾는다.

- Ln 구조: `@.claude/for-agent-codingprotocol-ln-structure.md` 참조
- Python 코딩: `@.claude/for-agent-codingprotocol-python.md` 참조

## 프로젝트 설명

`ff-lntools`. ln-structure 프로젝트용 정적 검사(`lnt check`), 영향 범위(`lnt blast`),
문서 생성(`lnt doc`), Claude Code 훅(`lnt hook`). 표준 라이브러리만 사용. Python 3.10+.

이 프로젝트 자체가 ln-structure 이며 자기 자신을 검사한다. 훅이 `.claude/settings.json` 에 등록되어 있다.

- 소스: `src/lntools/l0..l4`. 모듈 목록은 `src/lntools/for-agent-layerinfo.md`
- 테스트: `tests/` 미러 구조. fixture 는 `tests/fixtures/sample` (의도된 위반 12건이 심어진 샘플)
- 실행: `python -m pytest -q`, `python -m lntools check`, `python -m lntools doc --check`
- 개발 env: conda `py312`. 배포는 py310, py312 양쪽에 `pip install -e .`

## 추가 규칙

- fixture 의 위반 목록을 바꾸면 `tests/l2/checker/test_checker.py` 의 기대값을 같이 바꾼다
- 출력 문자열은 ASCII 와 한글만. 훅 경로는 UTF-8 로 고정되어 있다
- 문서 수정 후 `python -m lntools doc --check` 가 0 이어야 한다
