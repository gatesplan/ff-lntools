---
name: init-protocol
description: 프로젝트에 Ln 구조 코딩 프로토콜 초기화. 새 프로젝트 시작 시 사용.
version: 2.1.0
user-invocable: true
---

# Init Protocol

`lnt init` 을 실행한다. 프로토콜 문서 복사, CLAUDE.md 생성, Claude Code 훅 병합을 한 번에 한다.

## 실행

```bash
if ! command -v lnt >/dev/null 2>&1; then
    echo "lnt 없음. 어느 Python 환경에서든 잡히도록 사용자 bin 에 설치:"
    echo "  uv tool install --python 3.14 ff-lntools   (또는 pipx install ff-lntools)"
    exit 1
fi
lnt init
```

## 이후

- `src/<pkg>/lN/` 구조를 만든 뒤 `lnt doc` 으로 layerinfo 문서를 생성한다
- `lnt check` 로 규칙을 확인한다. 훅이 편집마다 자동 실행한다
