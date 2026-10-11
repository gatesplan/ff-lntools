# 프로젝트 프로토콜

## 구조 규칙

이 프로젝트는 ln-structure 를 따른다. 규칙과 해결 방법은 필요할 때 `.claude/for-agent-codingprotocol-ln-structure.md`(공통)와
`.claude/for-agent-codingprotocol-ln-structure-<언어>.md`(파일 이름, 표면 파일, import 문법과 예시)를 읽는다.

## 프로젝트 설명

`ff-lntools`. ln-structure 프로젝트용 정적 검사(`lnt check`), 영향 범위(`lnt blast`),
문서 생성(`lnt doc`), Claude Code 훅(`lnt hook`). Python 과 Rust 프로젝트를 다룬다.
의존은 Rust 를 읽는 tree-sitter, tree-sitter-rust 뿐이고 나머지는 표준 라이브러리. Python 3.10+.

이 프로젝트 자체가 ln-structure 이며 자기 자신을 검사한다. 훅이 `.claude/settings.json` 에 등록되어 있다.

- 소스: `src/lntools/l0..l4`. 모듈 목록은 `src/lntools/for-agent-layerinfo.md`
- 테스트: `tests/` 미러 구조. fixture 는 `tests/fixtures/sample` (의도된 위반 13건이 심어진 샘플),
  `tests/fixtures/rust_sample` (Rust, 위반 14건), `tests/fixtures/rust_clean` (Rust, cargo 로 컴파일되는 예제),
  `tests/fixtures/rust_rich` (Rust 기능을 고루 쓰는 예제. 외부 크레이트를 받아야 cargo 테스트가 돈다)
- 실행: `python -m pytest -q`, `lnt check`, `lnt doc --check`
- 개발 python 은 uv 의 3.14: `uv run --no-project --python 3.14 --with pytest --with tree-sitter --with tree-sitter-rust -- python -m pytest -q`.
  커밋 전에는 최소판 3.10 으로도 돌린다: 같은 명령에서 `--python` 에 conda `py310` 의 python 경로를 준다.
  Rust 표면을 cargo 로 확인하는 테스트는 cargo(`~/.cargo/bin`)가 없으면 건너뛴다
- 사용자 bin 의 `lnt` 는 uv tool 에 일반 설치한 판이다. 소스를 고쳐도 바로 바뀌지 않아, 작업 중에 다른 프로젝트의 훅이 깨지지 않는다.
  고친 소스로 검사하려면 `PYTHONPATH=src uv run --no-project --python 3.14 --with tree-sitter --with tree-sitter-rust -- python -m lntools check`. 판을 확인한 뒤 `uv tool install --reinstall . --python 3.14` 로 올린다
- 훅은 `lnt hook ...` 으로 부른다
- 이 셸의 `python` 은 conda env 를 활성화하지 않으면 Microsoft Store 바로가기다. 개발 명령은 위의 uv 나 conda env 의 python 으로 돌린다
- conda env 에는 lntools 를 깔지 않는다. 깔려 있으면 그 env 를 활성화했을 때 그쪽 `lnt` 가 먼저 잡힌다. 옮기는 방법은 `MIGRATION.md`

## 추가 규칙

- fixture 의 위반 목록을 바꾸면 `tests/l2/checker/test_checker.py` 의 기대값을 같이 바꾼다
- 출력 문자열은 ASCII 와 한글만. 훅 경로는 UTF-8 로 고정되어 있다
- 문서 수정 후 `lnt doc --check` 가 0 이어야 한다
