# ff-lntools
[English](README.md) | 한국어

AI 코딩 에이전트(Claude Code 등)와 함께 Python 프로젝트를 만들 때 쓰는 구조 규칙 **ln-structure** 와,
그 규칙을 기계적으로 검사하고 문서를 생성하는 도구 `lnt`.

표준 라이브러리만 사용. Python 3.10+. Windows / macOS / Linux.


## 1. ln-structure 란

모듈을 **의존성 깊이**로만 층(layer)에 배치하는 구조다. 층 이름은 `l0`, `l1`, ... 이고 아무 의미도 없다.
오직 "무엇에 의존하는가"로 위치가 정해진다.

```
src/shop/
  l0/                       # 아무것도 의존하지 않음 (표준 라이브러리만)
    candle/
      candle.py             # class Candle
      __init__.py           # from .candle import Candle
  l1/                       # l0 만 의존
    order/
      order.py              # class Order  (from shop.l0.candle import Candle)
      __init__.py
  l2/                       # l0, l1 만 의존
    report/
      report.py
      __init__.py
  for-agent-layerinfo.md    # 전체 모듈 목록 (생성됨)
tests/
  l1/order/test_order.py    # src 와 같은 구조
```

규칙은 네 개다.

| 코드 | 규칙 |
|---|---|
| C1 | import 는 **자기보다 낮은 층**만. 같은 층도 금지 |
| C2 | 모듈 **표면**(`shop.l1.order`)까지만 import. 그 안의 파일이나 중첩 모듈 내부로 들어가지 않음 |
| C3 | 모듈의 층 = 의존하는 모듈의 최고 층 + 1. 의존이 없으면 l0. 외부 패키지를 쓰면 최소 l1 |
| C4 | 모듈 간 순환 금지 |

왜 이렇게 하는가.

- 에이전트가 만든 코드의 의존성이 얽히는 것을 구조적으로 막는다. 순환이 생길 수 없다
- 어떤 모듈을 고쳤을 때 영향 범위가 "그보다 위 층"으로 한정된다. 도구가 정확히 계산할 수 있다
- 층에 의미가 없으므로 "이건 서비스인가 유틸인가" 같은 분류 논쟁이 없다. 의존을 추가하면 층이 올라갈 뿐이다
- 에이전트는 모듈 지도(모듈마다 책임 한 줄)에서 시작해 시그니처는 `lnt sig` 로 조회하고, 상세는 코드를 읽는다

상세 규칙(중첩 모듈, 상호 호출 처리, 의존성 역전, `__init__` 패턴)은
[`src/lntools/protocol/for-agent-codingprotocol-ln-structure.md`](src/lntools/protocol/for-agent-codingprotocol-ln-structure.md).

## 2. 도구가 하는 일

규칙을 사람이 지키는 데 의존하지 않고 도구가 검사한다. 특히 Claude Code 훅으로 연결하면
에이전트가 파일을 편집할 때마다 자동으로 검사되어 위반이 오류로 돌아온다.

| 명령 | 역할 |
|---|---|
| `lnt init` | 프로젝트에 프로토콜 문서, `CLAUDE.md`, Claude Code 훅 설치 |
| `lnt check` | C1~C4 검사. 위반 시 exit 1 |
| `lnt blast MODULE` | 이 모듈을 고치면 영향받는 상위 모듈 목록 |
| `lnt map` | 모듈 목록, 층, 의존 한눈에 |
| `lnt sig [대상]` | 층이나 모듈의 공개 시그니처. 저장하지 않고 그 자리에서 계산 |
| `lnt review` | 위반은 아니지만 볼 만한 것: 우회 의존, 아무도 쓰지 않는 모듈, 클래스가 여럿인 파일. 항상 exit 0 |
| `lnt doc` | 모듈 지도(`for-agent-layerinfo.md`) 생성 |
| `lnt doc --check` | 문서가 코드와 어긋났는지 검사 |
| `lnt move MODULE lK` | 모듈을 다른 층으로 옮기고 import 경로, 테스트, 문서를 전부 갱신 |

## 3. 시작하기

### 설치

```
pip install ff-lntools
```

프로젝트가 쓰는 Python 환경(venv, conda env)마다 설치한다. 훅이 `python -m lntools` 로 호출하기 때문이다.

### Claude Code 스킬 설치 (1회)

```
lnt init --skill
```

`~/.claude/skills/init-protocol/SKILL.md` 가 생긴다. 이후 Claude Code 안에서 `/init-protocol` 을 치면
아래 `lnt init` 과 같은 일을 한다. Claude Code 를 쓰지 않으면 이 단계는 건너뛴다.

### 프로젝트 세팅

```
cd my-project
lnt init
```

생기는 것:

```
my-project/
  CLAUDE.md                                   # 없을 때만 생성. 프로토콜 문서를 가리킴
  .claude/
    for-agent-codingprotocol-ln-structure.md  # 규칙. 세션마다 넣지 않고 필요할 때 읽는다
    settings.json                             # Claude Code 훅. 기존 설정이 있으면 hooks 만 병합
```

### 코드 작성과 검사

`src/<패키지>/l0/`, `l1/` ... 아래에 모듈 폴더를 만든다. 모듈 하나 = 폴더 하나 = 파일 하나(원칙) = 클래스 하나.

```
lnt check          # 규칙 검사
lnt doc            # 문서 생성
lnt map            # 구조 확인
```

`lnt check` 가 C3 위반("선언 l2, 계산 l1")을 내면 `lnt move 모듈 l1` 로 옮긴다.

## 4. Claude Code 훅 동작

`lnt init` 이 `.claude/settings.json` 에 훅 두 개를 등록한다.

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup|resume|clear|compact",
      "hooks": [{"type": "command", "command": "python -m lntools hook session-start"}]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{"type": "command", "command": "python -m lntools hook post-edit", "timeout": 30}]
    }]
  }
}
```

- **SessionStart**: 세션이 시작될 때 `for-agent-layerinfo.md`(전체 모듈 목록)를 에이전트 컨텍스트에 넣는다.
  에이전트가 grep 부터 시작하지 않고 구조를 알고 시작한다
- **PostToolUse**: 에이전트가 `src/**/*.py` 를 편집할 때마다 실행된다
  - 규칙 위반이 있으면 **exit 2 + stderr**. 위반 종류별 해결 방법과 함께 에이전트에게 오류로 전달되어 고치기 전에는 진행하지 못한다
  - 위반이 없으면 영향 범위(`blast`), 편집한 모듈의 우회 의존, 모듈 지도 불일치(`lnt doc` 으로 해결)를 정보로 전달한다

훅은 에이전트가 호출하는 것이 아니라 Claude Code 가 자동으로 실행한다. 에이전트가 "규칙을 잊어도" 검사된다.

## 5. 문서 체계

저장하는 문서는 패키지 루트의 `for-agent-layerinfo.md` 하나다(중첩 모듈은 그 안에 하나씩).
층별 모듈 목록과 모듈마다 책임 한 줄을 담는다. 목록은 `lnt doc` 이 `<!-- lnt:generated:start -->` 와 `end`
마커 사이에서 맞추고, 책임 한 줄은 사람이 쓰며 다시 생성해도 보존된다. 마커 밖은 Notes 로 보존된다.

시그니처는 저장하지 않는다. `lnt sig` 가 코드에서 그 자리에서 계산한다.

```
$ lnt sig l1.order
## l1.order
Order.__init__(symbol: str, qty: float)  # order.py
Order.fill(qty: float) -> None  # order.py
```

모듈별 상세 문서는 없다. 코드를 읽는다. 코드만 보고 알 수 없는 것(설계 이유, 코드 밖 계약)은 Notes 에 짧게 쓴다.

## 6. 자주 나오는 질문

**하위 모듈이 상위 모듈을 써야 하는데?**
층을 올리면 된다. 안 올라가는 경우(양방향 호출, 플러그인, 패키지 밖 코드)만 의존성 역전을 쓴다.
규칙 문서의 "상위 층 호출이 필요할 때" 절.

**두 클래스가 서로 호출하는데?**
동작 단위가 하나라면 같은 모듈 폴더에 두 파일로 둔다. 모듈 내부 순환은 규칙 밖이다.

**층이 많아지면?**
중첩 모듈을 쓴다. `l3/portfolio/` 안에 다시 `l0/`, `l1/` 을 둘 수 있다. 바깥에서는 `portfolio` 표면만 보인다.

**기존 프로젝트에 적용하면?**
`lnt init` 후 `lnt check`. 위반이 나오면 `lnt move` 로 하나씩 옮긴다. 이미 손으로 쓴 layerinfo 문서가 있으면
`lnt doc` 이 한 줄 설명을 살리고 나머지를 생성 영역으로 바꾼다(이전 내용은 git 에 있다).

## 7. 개발

```
git clone https://github.com/gatesplan/ff-lntools
cd ff-lntools
pip install -e .[dev]
python -m pytest -q
python -m lntools check       # 이 프로젝트 자체가 ln-structure 이며 자기 자신을 검사한다
```

연구 프로토콜(실험 폴더, 논문 노트)은 별도 저장소
[ff_coding_agent_protocol_md](https://github.com/gatesplan/ff_coding_agent_protocol_md).

