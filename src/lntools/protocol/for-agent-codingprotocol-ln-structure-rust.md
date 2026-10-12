# ln-structure: Rust

공통 규칙은 `for-agent-codingprotocol-ln-structure.md` 에 있다. 이 문서는 Rust 에서 그 규칙을 어떻게 쓰는지 정한다.

## 대상

- 패키지 = 라이브러리 크레이트 하나. 패키지 루트는 `src/` 이고 층 폴더는 `src/l0`, `src/l1`, ... 이다
- `lnt` 는 패키지 안에 `.rs` 소스만 있으면 Rust 로 본다. 소스로 가를 수 없으면 프로젝트 루트에 `Cargo.toml` 이 있을 때 Rust 로 본다
- 워크스페이스의 여러 크레이트, Python 과 섞인 프로젝트(PyO3 등)는 아직 다루지 않는다

## 공개 이름

- 모듈이 공개하는 이름은 `pub` 인 struct, enum, trait, type 별칭(, union)뿐이다
- 자유 함수는 타입의 연관 함수(`impl Order { pub fn new() -> Self }`)로, 상수는 연관 상수(`pub const MAX: u32`)로 둔다
- `pub(crate)` 항목은 표면에 들어가지 않는다. 모듈 밖에서 쓸 타입은 `pub` 으로 쓴다
- 중첩 모듈과 패키지 루트의 맨 위 층 모듈은 `pub use` 로 같은 스코프 안쪽 이름을 다시 내보낼 수 있다. 다시 내보낸 이름도 그 모듈의 공개 이름이다.
  트레이트는 별칭이 없으니 이 길로 꺼낸다(아래 '중첩 모듈 mod.rs'). 그 밖의 `pub use` 는 공개 이름이 아니다

## 디렉토리 구조

테스트 위치는 ln 규칙이 아니다. 이 문서의 예시는 Rust 관례대로 모듈 폴더의 `tests.rs`(단위 테스트)와
크레이트의 `tests/`(통합 테스트)를 쓴다.

### 단순 모듈

```
Cargo.toml
clippy.toml               # lnt init 이 둔다
src/
  lib.rs                  # 패키지 표면 (lnt doc)
  ln/
    mod.rs                # 층 표면 (lnt doc)
    modulename/
      mod.rs              # 모듈 표면 (lnt doc)
      modulename.rs       # 본체
      tests.rs            # 단위 테스트 (선택)
```

### 중첩 모듈

```
src/
  ln/
    modulename/
      mod.rs              # 모듈 표면: 안쪽 맨 위 층 (lnt doc)
      l0/
        mod.rs
        sub/
          mod.rs
          sub.rs
      l1/
      for-agent-layerinfo.md
```

## 표면 파일 = `mod.rs`, `lib.rs`

모든 `mod.rs` 와 `lib.rs` 는 `lnt doc` 이 만든다. 손으로 고치지 않는다. 모듈 선언(`mod`)과 공개 이름의 `pub use` 만 들어간다.
`lib.rs` 에 크레이트 속성(`#![deny(...)]`)이나 코드를 쓰면 `lnt doc` 이 덮어쓰지 않고 알린다. 린트 설정은 `Cargo.toml` 의 `[lints]` 에 둔다.

### 모듈 mod.rs (모듈 표면)

```rust
// src/l1/order/mod.rs  (lnt doc 이 씀)
mod order;
#[cfg(test)]
mod tests;

pub use order::Order;
```

폴더의 파일은 비공개 `mod` 다. 바깥에서는 `pub use` 한 이름만 보이고, 안쪽 파일로 들어가는 경로
(`crate::l1::order::order::Order`)는 컴파일러가 막는다(E0603).

```rust
// src/l2/report/report.rs
use crate::l1::order::Order;   // 모듈 표면 경로
```

### 층 mod.rs (층 표면)

```rust
// src/l1/mod.rs  (lnt doc 이 씀)
#![allow(unused_imports)]

pub(crate) mod order;
pub(crate) mod pair;

pub use order::Order;
pub use pair::Pair;
```

```rust
// src/l2/report/report.rs
use crate::l1::{Order, Pair};   // 층 단위 경로
```

- 모듈 폴더는 `pub(crate) mod` 다. 크레이트 밖에서는 깊은 경로가 막힌다
- 층 표면의 이름은 다 쓰이지 않아도 되므로 `unused_imports` 경고를 끈다
- 같은 층에서 공개 이름이 겹치면 `pub use` 가 컴파일 오류(E0252)가 된다. `lnt doc` 은 겹치는 이름을 층 표면에서 빼고 `lnt check` 가 C2 로 알린다

### 중첩 모듈 mod.rs

안쪽 맨 위 층 모듈들의 표면을 공개한다. 안쪽 층은 비공개라 중첩 모듈 밖에서 안쪽으로 들어가는 경로는 컴파일러가 막는다.

```rust
// src/l3/portfolio/mod.rs  (lnt doc 이 씀. 안쪽 맨 위 층이 l1 이고 거기에 store 가 있다)
mod l0;
mod l1;

pub use l1::store::Store;
```

맨 위 층 모듈이 아래 층 이름을 꺼내 줄 수 있다. 타입은 `pub type` 별칭으로, 트레이트는 `pub use` 로 꺼낸다.
바깥 모듈은 꺼낸 트레이트를 `impl Env for Model` 로 구현한다. 이 impl 은 타입의 모듈에 있으니 C6 에 걸리지 않는다.

```rust
// src/l2/formula/l2/kit/kit.rs  (formula 의 맨 위 층. 바깥에 드러낼 이름을 모은다)
pub use crate::l2::formula::l1::Env;                     // 트레이트: l1/eval 이 쓰는 약속
pub type Formula = crate::l2::formula::l1::Formula;      // 타입은 별칭으로도 된다
```

- `pub use` 가 가리킬 수 있는 것은 같은 중첩 모듈 안쪽의 표면 이름이다. 패키지 루트의 맨 위 층이면 패키지 안의 표면 이름이다
- 스코프 밖(바깥 패키지의 층, 외부 크레이트, `std`)을 가리키면 `lnt check` 가 C2 로 알리고 표면에서 뺀다
- 맨 위 층이 아닌 모듈의 `pub use` 는 표면에 들어가지 않는다
- `lnt sig` 은 다시 내보낸 이름 아래에 원래 정의의 시그니처를 보인다

### lib.rs (패키지 표면)

```rust
// src/lib.rs  (lnt doc 이 씀. 맨 위 층이 l3 이고 거기에 portfolio 가 있다)
mod l0;
mod l1;
mod l2;
mod l3;

pub use l3::portfolio::Portfolio;
```

```rust
// 크레이트 밖 (다른 크레이트, src/main.rs, examples/, tests/)
use shop::Portfolio;
```

### clippy 설정

`order/order.rs` 처럼 모듈 폴더와 같은 이름의 파일에 clippy 가 `module_inception` 경고를 낸다.
모듈 폴더가 `pub(crate)` 이므로 `clippy.toml` 의 `allow-private-module-inception = true` 로 끈다. `lnt init` 이 넣는다.
경고를 없애려고 파일 이름을 바꾸지 않는다. 파일 이름이 세부 책임의 이름이다.

## 경로 (use)

- 층을 건너는 경로는 `crate::` 로 쓴다: `use crate::l1::order::Order;`, 층 단위는 `use crate::l1::{Order, Pair};`
- 모듈 폴더 안 파일끼리는 `super::` 로 쓴다: `use super::side::Side;`. 테스트는 `use super::Order;`
- 경로 규칙(C5)은 아직 정하지 않았다. `lnt` 는 Rust 경로의 모양을 검사하지 않는다
- 외부 크레이트를 쓰는 모듈은 l1 이상이다. 표준 크레이트(std, core, alloc)는 외부가 아니다
- `#[cfg(test)]` 가 붙은 항목과 `#[cfg(test)] mod tests;` 로 선언된 파일은 의존이 아니다. 다른 `cfg` 갈래는 모두 의존으로 센다
- 식 안에 바로 쓴 경로(`crate::l1::order::Order::new()`)와 매크로 인자 안의 `crate::` 경로도 의존이다

## 덧붙이기(impl) 위치: C6

- `impl T { ... }` 는 T 를 정의한 모듈 폴더 안에만 둔다. 폴더 안의 다른 파일은 된다
- `impl Trait for T` 는 T 의 모듈이나 Trait 의 모듈 안에 둔다
  - 아무 타입에나 거는 구현(`impl<T: Bound> Trait for T`)과 외부 타입에 대한 구현(`impl MyTrait for String`)은 Trait 의 모듈에 둔다
- 테스트 코드(`#[cfg(test)]`) 안은 보지 않는다

메서드 호출에는 `use` 가 필요 없다. 위 층이 아래 층 타입에 메서드를 붙이면 그 타입을 가진 모든 모듈이 import 없이
위 층 코드를 부르게 되어, 방향(C1)과 영향 범위(`lnt blast`)가 보이지 않는다. 트레이트 구현도 그 트레이트를 쓰는 모든 곳에서 통하므로 같다.

위 층에서 아래 층 타입을 확장해야 하면 확장 트레이트를 쓴다. 쓰는 쪽이 트레이트를 `use` 해야 메서드가 보이므로 의존이 드러난다.

```rust
// src/l3/report/report.rs
use crate::l1::order::Order;

pub trait OrderExt {
    fn line(&self) -> String;
}

impl OrderExt for Order {
    fn line(&self) -> String {
        format!("qty {}", self.qty)
    }
}

// 쓰는 쪽: use crate::l3::report::OrderExt; 가 있어야 order.line() 이 보인다
```

선택 기능의 구현(serde 등)을 파일 하나에 모으지 않는다. 타입 정의에 붙인다:
`#[cfg_attr(feature = "serde", derive(serde::Serialize))]`

## 매크로

- 매크로가 펼쳐져 만드는 코드의 의존은 `lnt` 가 보지 못한다. 매크로 인자 안의 `crate::` 경로는 센다
- 매크로 규칙은 아직 정하지 않았다. 직접 정의하기 전에 함수, 제네릭, 트레이트로 되는지 먼저 본다

## 상위 층 호출 예시

### 1:1 상호 호출을 한 모듈로 합칠 때

```
ln/trading_engine/
  mod.rs          # Engine 만 공개 (lnt doc)
  engine.rs       # pub struct Engine
  momentum.rs     # pub(crate) struct Momentum. 서로 use super::engine::Engine, use super::momentum::Momentum
```

모듈 안 파일끼리의 순환은 규칙 밖이고 Rust 도 허용한다.

### 의존성 역전

인터페이스는 트레이트다. 구현은 `impl Trait for T` 로 늘 명시 선언되므로(구조적 타이핑이 없다) `lnt blast` 가 트레이트를 거쳐 영향 범위를 잡는다.
주입 받는 자리는 `Box<dyn Trait>` 를 기본으로 쓴다. 제네릭(`Engine<S: Strategy>`)은 성능이 필요한 곳에만 쓴다.

```rust
// src/l0/order_placer/order_placer.rs
pub trait OrderPlacer {
    fn place_order(&mut self, side: Side, qty: u32);
}

// src/l1/strategy/strategy.rs
use crate::l0::order_placer::OrderPlacer;

pub trait Strategy {
    fn on_tick(&mut self, placer: &mut dyn OrderPlacer, price: u32);
}

// src/l1/book/book.rs
use crate::l0::order_placer::{OrderPlacer, Side};

#[derive(Default)]
pub struct Book { /* ... */ }

impl OrderPlacer for Book {
    fn place_order(&mut self, side: Side, qty: u32) { /* ... */ }
}

// src/l2/momentum/momentum.rs
use crate::l0::order_placer::{OrderPlacer, Side};
use crate::l1::strategy::Strategy;

#[derive(Default)]
pub struct Momentum;

impl Strategy for Momentum {
    fn on_tick(&mut self, placer: &mut dyn OrderPlacer, price: u32) {
        placer.place_order(Side::Buy, 1);
    }
}

// src/l2/engine/engine.rs
use crate::l1::book::Book;
use crate::l1::strategy::Strategy;

pub struct Engine {
    strategy: Box<dyn Strategy>,
    book: Book,
}

impl Engine {
    pub fn new(strategy: Box<dyn Strategy>) -> Self {
        Self { strategy, book: Book::default() }
    }

    pub fn tick(&mut self, price: u32) {
        self.strategy.on_tick(&mut self.book, price);
    }
}

// src/l3/app/app.rs  (진입점. 연결은 여기서만)
use crate::l2::{Engine, Momentum};

pub struct App;

impl App {
    pub fn run() {
        let mut engine = Engine::new(Box::new(Momentum));
        engine.tick(100);
    }
}
```

스스로 등록하는 크레이트(inventory, linkme, ctor)는 쓰지 않는다. 등록 목록은 진입점 코드 한 곳에 보여야 한다.

## 전체 예시

```
project/
  Cargo.toml
  clippy.toml
  src/
    lib.rs                                # 패키지 표면
    for-agent-layerinfo.md                # 모듈 목록과 책임

    l0/
      mod.rs                              # 층 표면
      candle/
        mod.rs
        candle.rs
        tests.rs
      order_placer/
        mod.rs
        order_placer.rs
        side.rs

    l1/
      mod.rs
      strategy/
        mod.rs
        strategy.rs
      book/                               # 중첩 모듈. 안쪽 층에도 모듈 폴더를 둔다
        mod.rs
        l0/
          mod.rs
          position/
            mod.rs
            position.rs
        l1/
          mod.rs
          ledger/
            mod.rs
            ledger.rs
        for-agent-layerinfo.md            # book 안의 모듈 목록과 책임

    l2/
      mod.rs
      engine/
      momentum/

    l3/
      mod.rs
      app/
        mod.rs
        app.rs

  tests/
    app.rs                                # 통합 테스트. 패키지 표면(shop::App)만 쓴다
```

## 파일 배치 규칙

### 소스 코드
- 위치: `src/ln/modulename/`
- 메인 파일: `modulename.rs` (또는 중첩 Ln)
- 표면: `mod.rs` (패키지는 `src/lib.rs`)

### 고아 판정에서 패키지 밖 쓰임으로 보는 것
- `src/main.rs`, `src/bin/`, `examples/`, `benches/` 의 `use 크레이트이름::...` (tests 제외)

### lnt 가 보지 못하는 것
- 매크로가 펼쳐져 만드는 코드, `build.rs`, `include!`
- 워크스페이스의 다른 크레이트
