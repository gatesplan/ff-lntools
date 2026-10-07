# 표준 ln-structure
import 체인에 기반하여 깊이 체인을 만드는 파일, 폴더 규칙

## 목적
AI 생성 코드의 의존성 관리를 선형화하고, 계층의 목적 없이 구조만 남는 확장을 무한하게 할 수 있는 체계를 제공.

## 기본 규칙
1. 항상 폴더 구조 사용
   - 모든 단순 모듈은 `ln/modulename/` 폴더로 구성
   - 모든 중첩 모듈은 `ln/modulename/lm/submoudle_name` 폴더로 구성
   - __init__는 모듈이 공개하는 것만을 re-export 한다.
   - 파일 하나에 클래스 하나, 클래스 하나에 책임 하나. 여러 개념을 한 모듈에 몰면 그 모듈이 허브가 되어 영향 범위(blast)가 무뎌진다.

2. l0, l1, ... ln 층 규칙
   - 외부 라이브러리 의존이 없는 모듈 (표준 라이브러리만 허용)의 위치
   - 층(ln)에는 어떠한 의미도, 역할도 부여하지 않는다.
   - 층은 오직 의존성 관계만을 따라 결정한다.

3. 미러 테스트 구조
   - `tests/` 구조는 `src/` 구조와 동일
   - `src/l1/order/` → `tests/l1/order/`

4. 임포트 규칙
   - 항상 낮은 레벨의 모듈만 임포트할 수 있다
   - 낮은 레벨의 표면만 임포트할 수 있고, 중첩 구조 심부로 들어가 임포트해선 안 된다.
   - `if TYPE_CHECKING:` 안의 임포트도 의존이다. 층 판정에 포함한다.
   - 모듈 간 순환은 금지. 모듈 내부 파일 간 순환은 규칙 밖 (허용).

5. 진입점 규칙
   - 외부 진입점은 마지막 층에 위치하며, 외부에서는 마지막 층의 진입점만 re-export 한다.
   - 진입점(연결 모듈)은 1파일 1클래스, 단일 책임 규칙의 예외. 모든 구현체를 알고 조립하는 것이 역할이다.

6. 층 결정 규칙
   - 모듈의 층 = 의존하는 모듈의 최고 층 + 1. 의존이 없으면 l0.
   - 선언 층(디렉토리)과 계산 층이 다르면 위반. `lnt check`가 판정한다.


## 디렉토리 구조

### 단순 모듈

```
src/fishfactory/
  ln/
    modulename/
      modulename.py
      __init__.py

tests/
  ln/
    modulename/
      test_modulename.py
```

### 중첩 모듈

```
src/fishfactory/
  ln/
    modulename/
      l0/
      l1/
      l2/
      __init__.py

tests/
  ln/
    modulename/
      test_modulename.py
      test_integration.py
```

## __init__.py 패턴

**규칙: 항상 상대 임포트 사용**

### 모듈 __init__.py

```python
# src/fishfactory/l1/order/__init__.py

from .order import Order  # 상대 임포트

__all__ = ['Order']
```

**이유:**
- 모듈 이동 시 경로 불변 (l1 -> l2 이동 시 수정 불필요)
- 레벨 변경 자동 반영 (디렉토리 위치 = 계층 상태)
- 다른 프로젝트 복사 시 패키지명 변경 불필요

**효과:**
```python
# 사용자 코드
from fishfactory.l1.order import Order  # 짧은 import
```

### 레이어 __init__.py

각 레이어 폴더(ln/)의 `__init__.py`는 해당 레이어의 모든 모듈을 re-export한다.
단, 즉시 import하지 않고 PEP 562 모듈 `__getattr__`로 지연 로드한다.
층에 모듈이 많아도 요청한 모듈만 로드된다.

```python
# src/fishfactory/l1/__init__.py
import importlib

# 공개 이름 -> 모듈 폴더명. lnt doc이 생성한다
_EXPORTS = {
    'Order': 'order',
    'Pair': 'pair',
}
__all__ = list(_EXPORTS)

def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f'.{_EXPORTS[name]}', __name__)
        return getattr(mod, name)
    raise AttributeError(name)
```

**효과:**
```python
from fishfactory.l1 import Order, Pair  # 레이어 단위 import. order, pair만 로드
```

### 패키지 최상단 __init__.py

패키지 루트의 `__init__.py`는 최상위 레이어의 메인 비즈니스 모듈만 노출한다.

```python
# src/fishfactory/__init__.py

from .l3.portfolio import Portfolio  # 최상위 파사드만

__all__ = ['Portfolio']
```

**효과:**
```python
from fishfactory import Portfolio  # 최단 경로 import
```

## 상위 층 호출이 필요할 때

하위 모듈이 상위 모듈을 호출해야 하는 상황은 세 갈래로 처리한다. 순서대로 검토한다.

### 1. 층을 올린다

A가 B에 의존하면 A를 B보다 위로 옮긴다. 대부분 이걸로 끝난다.
`lnt move A lK`로 이동하고 `lnt check`로 연쇄 이동을 확인한다.

### 2. 1:1 상호 호출이면 한 모듈로 합친다

A와 B가 서로 호출하고, 항상 함께 바뀌고, 각각 하나뿐이면 둘은 동작 단위가 하나다.
같은 모듈 폴더에 두 파일로 둔다. 모듈 내부 순환은 규칙 밖이다.

```
ln/trading_engine/
  engine.py       # class Engine
  strategy.py     # class Momentum
  __init__.py     # Engine만 공개
```

Python 순환 import는 상대 객체를 파라미터로 받는 경우 타입 표기용이므로 `TYPE_CHECKING`으로 끊는다.

```python
# ln/trading_engine/strategy.py
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .engine import Engine

class Momentum:
    def on_tick(self, engine: Engine, price: float) -> None:
        engine.place_order('buy', 1)
```

### 3. 1:N 또는 패키지 외부 코드면 의존성 역전

한쪽이 여러 구현(전략 N개, 플러그인)이거나 패키지 밖 사용자 코드를 호출해야 하면
1, 2로 풀리지 않는다. 이때만 역전을 쓴다.

- 인터페이스(Protocol 또는 ABC)는 소비자와 구현체 양쪽보다 낮은 층에 둔다. 소비자 모듈 안도 된다.
- 구현체는 인터페이스를 **명시 상속**하고 메서드에 `@override`를 붙인다.
  구조적 타이핑만 쓰면 import 간선이 없어 `lnt blast`가 영향 범위를 추적하지 못한다.
- 연결(생성과 주입)은 진입점에서만 한다.
- 모듈 로드 시 스스로 등록하는 방식(import 부수효과)은 금지. 등록 목록이 코드 한 곳에 보여야 한다.

```python
# l0/order_placer/order_placer.py
from typing import Protocol

class OrderPlacer(Protocol):
    def place_order(self, side: str, qty: float) -> None: ...

# l1/strategy/strategy.py
from typing import Protocol
from shop.l0.order_placer import OrderPlacer

class Strategy(Protocol):
    def on_tick(self, placer: OrderPlacer, price: float) -> None: ...

# l2/momentum/momentum.py
from typing_extensions import override
from shop.l0.order_placer import OrderPlacer
from shop.l1.strategy import Strategy

class Momentum(Strategy):
    @override
    def on_tick(self, placer: OrderPlacer, price: float) -> None:
        placer.place_order('buy', 1)

# l2/engine/engine.py
from typing_extensions import override
from shop.l0.order_placer import OrderPlacer
from shop.l1.strategy import Strategy

class Engine(OrderPlacer):
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    @override
    def place_order(self, side: str, qty: float) -> None:
        pass

    def run(self) -> None:
        self.strategy.on_tick(self, 100.0)

# l3/app/app.py  (진입점. 연결은 여기서만)
from shop.l2.engine import Engine
from shop.l2.momentum import Momentum

class App:
    def __init__(self):
        self.engine = Engine(strategy=Momentum())
```

import는 전부 아래로 흐르고, 런타임 호출은 Engine <-> Momentum 양방향이다.
Engine과 Momentum은 같은 l2에 있으면서 서로를 모른다.

## 문서

저장하는 문서는 `for-agent-layerinfo.md` 하나다. 나머지는 그 자리에서 조회하거나 코드를 읽는다.

```
1. for-agent-layerinfo.md
   위치: src/fishfactory/ (중첩 모듈은 그 모듈 폴더에 따로)
   내용: 층별 모듈 목록과 모듈마다 책임 한 줄
   세션 시작 훅이 넣어 준다

2. 시그니처: 문서로 두지 않는다
   lnt sig l1            # 층
   lnt sig l1.order      # 모듈
   lnt sig order         # 모듈 이름

3. 상세: 문서로 두지 않는다. 코드를 읽는다
```

모듈 목록은 `lnt doc`이 마커 사이에 생성한다. 책임 한 줄은 사람이 마커 안의 각 줄에 쓰고, 다음 생성 때 보존된다.
새 모듈은 `[설명 필요]`로 들어간다. 코드만 보고 알 수 없는 설계 이유와 코드 밖 계약은 마커 밖 Notes에 짧게 쓴다.

```markdown
# for-agent-layerinfo.md

<!-- lnt:generated:start -->
## l0
- candle: 캔들 하나. 시고저종과 거래량
## l1
- order: 주문 객체. 체결과 취소 상태
<!-- lnt:generated:end -->

## Notes

(자유 기술. 보존됨)
```

## 도구 `lnt`

`ff-lntools` 패키지. 프로젝트 env에 설치되어 있어야 한다.

```
lnt check [--file PATH]     # 층 방향, 표면 import, 층 일치, 모듈 간 순환 검사. 위반 시 exit 1
lnt blast MODULE            # MODULE에 의존하는 상위 모듈 목록 (상속 경유 포함)
lnt sig [TARGET ...]        # 층이나 모듈의 공개 시그니처. 없으면 전체
lnt doc [--check]           # layerinfo 생성 / 불일치 검사
lnt move MODULE lK          # 층 이동 + import 경로 재작성
```

Claude Code 훅(`.claude/settings.json`)이 편집마다 `check`, `blast`, layerinfo 검사를 실행해
위반은 오류로, 영향 범위와 layerinfo 불일치는 정보로 세션에 주입한다.

## 전체 예시

```
project/
  src/fishfactory/
    for-agent-layerinfo.md                # 모듈 목록과 책임

    l0/
      candle/
        candle.py
        __init__.py
      token/
        token.py
        __init__.py

    l1/
      order/
        order.py
        __init__.py
      pair/
        pair.py
        __init__.py

    l3/
      portfolio/
        l0/
          tick_snapshot.py
          __init__.py
        l1/
          file_backend.py
          __init__.py
        l2/
          storage_l1.py
          __init__.py
        l3/
          portfolio.py
          __init__.py
        for-agent-layerinfo.md            # portfolio 안의 모듈 목록과 책임
        __init__.py

  tests/
    l0/
      candle/
        test_candle.py
      token/
        test_token.py

    l1/
      order/
        test_order.py
      pair/
        test_pair.py

    l3/
      portfolio/
        test_portfolio.py
        test_integration.py
```

## 파일 배치 규칙

### 소스 코드
- 위치: `src/fishfactory/ln/modulename/`
- 메인 파일: `modulename.py` (또는 중첩 Ln)
- Export: `__init__.py`

### 테스트
- 위치: `tests/ln/modulename/`
- 명명: `test_*.py`
- 구조: 소스 미러

### 문서
- 위치: `src/fishfactory/for-agent-layerinfo.md`. 중첩 모듈은 그 모듈 폴더에 따로 둔다
- 형식: 위 '문서' 절
