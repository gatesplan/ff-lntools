---
name: init-protocol
description: 프로젝트에 Ln 구조 코딩 프로토콜 초기화. 새 프로젝트 시작 시 사용.
version: 2.0.0
user-invocable: true
---

# Init Protocol

`lnt init` 을 실행한다. 프로토콜 문서 복사, CLAUDE.md 생성, Claude Code 훅 병합을 한 번에 한다.

## 실행

```bash
if ! python -c "import lntools" 2>/dev/null; then
    if [ "${CONDA_DEFAULT_ENV:-}" = "base" ] || [ -z "${CONDA_DEFAULT_ENV:-}${VIRTUAL_ENV:-}" ]; then
        echo "lntools 없음. 활성 env 가 없거나 base 라 설치하지 않음."
        echo "프로젝트 env 활성화 후: pip install ff-lntools"
        exit 1
    fi
    echo "lntools 설치: $(python -c 'import sys; print(sys.executable)')"
    python -m pip install -q ff-lntools
fi
python -m lntools init
```

## 이후

- `src/<pkg>/lN/` 구조를 만든 뒤 `lnt doc` 으로 layerinfo 문서를 생성한다
- `lnt check` 로 규칙을 확인한다. 훅이 편집마다 자동 실행한다
