## 8. Rust 에서 따로 요구되거나 권장되는 것

Rust 는 모듈마다 공개 범위(visibility)를 컴파일러로 강제하지만, 의존 방향과 비순환을 강제하는 단단한 경계는 크레이트(crate)에만 둔다. 공식 문서는 책임의 수, 파일당 타입 수, 크기 한도를 정하지 않으며, 그 빈자리를 빌림 검사(borrow checking), 일관성(coherence) 규칙, 컴파일 단위, `unsafe` 의 범위 같은 언어의 압력과 린트, 실무 관례가 채운다. 기준 시점은 2026년 10월(안정판 1.99, edition 2024)이다. edition 2024 는 모듈과 공개 범위 규칙을 바꾸지 않았고, 모듈 체계의 마지막 개편은 2018 edition 이다(Edition Guide 2018).

### 8.1 컴파일러와 Cargo 가 강제하는 것: 공개 범위는 모듈 트리를 따르고, 비순환은 크레이트에서만 강제된다

**공개 범위는 모듈 트리를 따라서만 열린다.** "By default, everything is *private*"(기본은 모두 비공개)이고, 비공개 항목은 "the current module and its descendants"(현재 모듈과 그 자손)만 쓴다(Reference: Visibility). 제한 공개(restricted visibility: `pub(crate)`, `pub(super)`, `pub(in path)`, 1.18 부터)도 조상 모듈만 가리킬 수 있어, 형제 사이의 순서("2층은 1층을 쓰되 거꾸로는 안 된다")는 표현할 수 없다. 다시 내보내기(re-export)는 범위를 넓히지 못해, `pub(crate)` 항목을 `pub use` 하면 E0364 오류다(Reference: Visibility; 실험 R1).

**일관성과 버전의 단위는 크레이트다.** 크레이트는 "a unit of compilation and linking, as well as versioning"(컴파일, 링크, 버전의 단위)이다(Reference: Crates). 고아 규칙(orphan rule)은 트레이트나 타입이 현재 크레이트에 있어야 impl 을 허용하고(E0117), 고유 impl(inherent impl)은 타입과 같은 크레이트에만 있으면 된다(E0116)(Reference: Implementations). 그래서 다른 모듈에 둔 고유 impl 도 컴파일된다(실험 R1). `#[non_exhaustive]` 도 정의한 크레이트 안에서는 효과가 없다(Reference: Type system attributes).

**모듈 순환은 허용되고 패키지 순환은 금지된다.** Reference 가 막는 순환은 `use` 재지정의 순환뿐이다(Reference: Use declarations). RFC 1560(2016)이 "The order of declarations of items should be irrelevant"(선언 순서는 무관해야 한다)를 원칙으로 삼은 의도된 결과다. 서로를 `use` 하는 두 모듈은 rustc 1.99.0 에서 진단 없이 컴파일되고(실험 R1), 모듈 분석기 cargo-modules 의 소스에도 모듈 순환이 있다. 반면 Cargo 는 패키지 순환을 오류로 거부하고(dev-dependency 는 예외) 패키지를 나눠 "strictly acyclic"(엄격히 비순환)하게 하라고 권한다(Cargo Book: Resolver). 조사 노트 하나는 이 규칙을 Cargo Book 에서 찾지 못해 실험으로만 확인했으나, resolver 장에 명시되어 있다.

정리하면 크레이트 안에서 **누구도 강제하지 않는 것**은 모듈 순환, 의존 방향과 층, impl 위치, 파일이나 모듈당 항목 수, 자유 함수(free function)와 메서드의 선택, `mod.rs` 와 `name.rs` 의 선택(한 모듈에 둘을 함께 쓰는 것만 E0761 오류다), 책임 서술과 코드의 일치다(Reference: Modules).

### 8.2 공개 범위, 다시 내보내기, SemVer: 공식 API 표면의 단위는 패키지다

**공식 문서는 내부 구조와 공개 구조를 떼어 놓으라고 권한다.** "With `pub use`, we can write our code with one structure but expose a different structure"(코드는 한 구조로 쓰고 다른 구조로 드러낼 수 있다)(Book 7.4). std 도 어댑터를 `std::iter::adapters` 에 두고 `std::iter` 에서 `pub use` 한다(Drysdale 2024). 반대로 rust-analyzer 는 "an innocent-looking `pub use`"(무해해 보이는 `pub use`)가 캡슐화를 깨기 쉽다고 경고하고, 라이브러리가 아닌 코드에서는 "two ways to use something"(같은 것을 쓰는 두 길)이 생긴다며 다시 내보내기를 피한다(rust-analyzer style.md).

**`pub` 과 `pub(crate)` 의 선택은 정리되지 않았다.** RFC 2126(2017)은 비공개 모듈 안의 `pub` 이 "tell you less than you might hope"(기대보다 적게 말해 준다)고 했고, 그 결과인 `unreachable_pub` 린트는 크레이트 밖에서 닿지 않는 `pub` 에 `pub(crate)` 를 권한다. 아직 allow 지만 문서는 "Eventually it is desired for this to become warn-by-default"(언젠가 기본 경고가 되기를 바란다)고 적는다(rustc 린트 문서). C-HIDDEN 과 Drysdale(2024)도 `pub(crate)` 를 권하는데, Drysdale 은 "as little as possible"(가능한 한 적게)이라는 조언을 수명이 긴 라이브러리의 걱정으로 한정한다. Kladov(2021d)는 한 컴파일 단위 안에서 공개 범위를 세밀히 해도 "doesn't meaningfully make the code better"(코드가 의미 있게 나아지지 않는다)며 크레이트 안팎만 가르자고 한다(본인이 밝힌 확신도 0.5).

**SemVer 는 패키지의 공개 항목에 대해 정의된다.** Cargo 지침은 공개 항목의 "renaming/moving/removing"(이름 변경, 이동, 삭제)을 major 로 보고 옛 이름의 `pub use` 를 완화책으로 둔다. 외부 크레이트의 glob import 는 상대가 항목을 더하기만 해도 깨질 수 있으므로 "should be avoided"(피해야 한다)고 한다(Cargo Book: SemVer). 이 지침은 스스로 "only *guidelines*"(지침일 뿐)이고, 크레이트 안 모듈 경로에는 SemVer 지위가 없다. glob 은 더 조여졌다. 1.94(2026-03)는 모호한 glob 다시 내보내기를 다른 크레이트에서도 보이게 했고 1.98(2026-08)은 모호한 glob import 일부를 하드 오류로 바꿨다(RELEASES.md). Kladov(2021d)도 glob 다시 내보내기를 금지하면 모든 이름이 명시되어 "useful for tooling"(도구에 유용하다)이라 한다. 다만 프렐류드(prelude)는 Tokio 1.0 이 없앤 반면 Bevy 는 권한다(tokio#3257; Bevy).

**공개 시그니처의 숨은 타입은 린트가 잡는다.** RFC 2145(2017)는 이를 하드 오류로 두던 RFC 136 을 대체해 "Private-in-public errors are relaxed and turned into lints"(오류를 린트로 완화한다)고 했고, 기준을 실제로 새는 범위인 유효 공개 범위(effective visibility)로 바꿨다. `private_interfaces`(warn)는 1.74 에 들어왔고 `unnameable_types`(allow)는 1.79 에 안정화되었다(RELEASES.md). 뒤의 것은 "reexport the type properly to make it nameable"(타입을 제대로 다시 내보내 이름 붙일 수 있게 하라)거나 그렇지 않음을 문서화하라고 권한다(rustc 린트 문서). 그러나 RFC 2145 는 이름 없는 타입에도 "legitimate uses"(정당한 쓰임)가 있다고 하며, 대표가 봉인 트레이트(sealed trait)다. C-SEALED 는 바깥에서 이름 붙일 수 없는 상위 트레이트로 바깥 구현을 막아 메서드 추가를 호환 변경으로 만드는데(Gruevski 2023), `unnameable_types` 를 켜면 이 패턴이 "trait `Sealed` is reachable but cannot be named" 경고를 낸다(실험 R1). 언어 차원의 봉인(RFC 3323)과 공개·비공개 의존 구분(RFC 3516)은 아직 불안정이다.

### 8.3 언어가 분해에 주는 압력: 빌림, impl 위치, 컴파일 단위, unsafe, 오류

**빌림 검사는 함께 변경되는 필드끼리 묶도록 민다.** 빌림 검사기(borrow checker)는 함수를 하나씩 보므로 `&mut self` 메서드는 값 전체를 빌린다(Matsakis 2018; Nomicon: Splitting Borrows). 구조체를 나누면 "often reveals smaller units of functionality"(더 작은 기능 단위가 드러나곤 한다)지만 "sometimes, the smaller structs are not good abstractions"(작은 구조체가 좋은 추상이 아닐 때도 있다)(Rust Design Patterns). Matsakis(2018)도 분해가 더 깔끔한 것은 "definitely not always"(결코 항상은 아니다)라 했다. 압력은 모듈 경계에서 가장 세다. 정의한 모듈 안에서는 비공개 필드를 따로 빌릴 수 있지만 바깥에서는 호출마다 값 전체가 빌려지고, 필드를 열면 비공개 원칙과 부딪힌다(Matsakis 2021; 이를 풀 뷰 타입의 도입 여부는 [미확인]). 경험 보고는 엇갈린다. West(2018)는 Rust 가 데이터 지향 설계에 크게 보상한다면서도 같은 교훈이 C++ 에도 통한다고 했고, LogLog Games(2024)는 재구성이 "at the most inconvenient times"(가장 곤란한 때) 강요된다고 했다. `RefCell` 같은 내부 가변성(interior mutability)은 충돌을 실행 시 패닉으로 옮길 뿐이고(West 2018), std 는 이를 "something of a last resort"(일종의 최후 수단)라 한다(std::cell). 이 압력이 모듈성을 높이는지 잰 실증은 없다.

**impl 위치 규칙은 한 번 만들어졌다가 되돌려졌다.** 고유 메서드는 import 없이, 트레이트 메서드는 트레이트만 있으면 호출되므로(Reference: Method-call expressions) impl 이 놓인 모듈은 호출 쪽 `use` 에 나타나지 않는다. RFC 155(2014)는 고유 impl 을 타입을 정의한 모듈에 두게 하며 "consistency in code layout"(코드 배치의 일관성)을 목적으로 들었다. RFC 735(2015)는 원래 동기였던 구현 세부('fake modules')가 사라졌고 규칙이 "non-DRY single use extension traits"(DRY 를 어기는 일회용 확장 트레이트)를 낳는다며 크레이트 조건으로 되돌렸고, 대가로 "ease of finding method definitions"(메서드 정의를 찾는 쉬움)를 잃는다고 인정했다(RFC 155 의 실제 구현 범위는 [미확인]). 확장 트레이트(extension trait)는 RFC 445(2014)가 `FooExt` 로 이름 짓되 "should be used sparingly"(아껴 써야 한다)고 했고, 늘어난 import 는 glob 프렐류드로 덜게 했다. 다른 언어에도 배치 규칙이 있다. Go 는 메서드를 수신자 타입의 패키지에 두게 하고, GHC 는 고아 인스턴스를 모듈 단위로(`-Worphans`), Swift 6.0 은 외부 타입의 사후 준수(retroactive conformance)를 경고한다(Go spec; GHC; SE-0364). rustc 도 함수 본문 안의 impl 이 "go against expectation"(기대에 어긋난다)며 `non_local_definitions`(warn)로 잡는다(RFC 3373; 기본 경고가 된 판은 [미확인]).

**컴파일 단위는 크레이트이고, 경계의 모양이 빌드를 좌우한다.** 서로 의존하는 모듈은 "cannot be trivially reduced further into separate crates"(쉽게 별도 크레이트로 쪼갤 수 없다)므로 크레이트가 "a wide DAG"(넓은 DAG)를 이루는 편이 낫고(Anderson 2020b), 일관성 규칙은 크레이트 분해를 막는 결합을 만든다(Anderson 2020a). Kladov(2021c)는 그 모양을 공통 어휘 크레이트, 독립 기능 여럿, 이를 묶는 잎 크레이트로 그렸다. 크레이트 안에서도 rustc 는 소스 모듈마다 코드 생성 단위(codegen unit)를 둘씩 만들어 바뀐 모듈만 다시 컴파일하려 하지만, 그 효과를 잰 자료는 없다(rustc partitioning.rs). 제네릭은 쓰는 쪽에서 단형화(monomorphization)되므로 Kladov(2021c)는 "do not put generic code at the boundaries between the crates"(크레이트 경계에 제네릭을 두지 말라)며 `&dyn Fn()` 을 권한다. 그러나 dyn 호환성(dyn compatibility, 옛 이름 object safety)은 디스패치 메서드에 타입 매개변수, `async fn`, `impl Trait` 반환을 허용하지 않는다(Reference: Traits). 1.75 에 들어온 트레이트 안 `async fn` 은 dyn 호환이 아니고, `Send` 여부는 "you as a trait author need to make a choice"(트레이트 작성자가 정해야 한다)는 문제로 남는다(Mandry 2023). 이후의 진전은 [미확인]이다.

**`unsafe` 와 불변식의 감사 단위는 모듈이다.** Nomicon 은 unsafe 가 "pollutes a whole *module*"(모듈 전체를 오염시킨다)이며 "the only bullet-proof way to limit the scope of unsafe code is at the module boundary with privacy"(unsafe 를 확실히 가두는 유일한 길은 공개 범위를 가진 모듈 경계)라 한다(Nomicon: Working with Unsafe). Jung(2016)도 unsafe 의 범위가 "the next abstraction boundary"(다음 추상 경계)에서 끝난다고 하고, RustBelt(Jung et al. 2018, 초록만 확인)는 unsafe 라이브러리가 안전한 확장이 될 검증 조건을 정의한다. 패턴 책은 불변식을 지킬 수 있는 "the smallest possible module"(가장 작은 모듈)에 unsafe 를 가두라 한다(Rust Design Patterns). 실증은 부분적이다. unsafe 를 직접 쓰는 라이브러리는 30% 미만이지만, 호출 사슬 어딘가의 unsafe 때문에 절반 넘는 라이브러리가 컴파일러로 완전히 검사되지 않으며(Evans et al. 2020, 초록만 확인), unsafe 코드는 대부분 잘 감싸져 있으나 상호 운용에 널리 쓰인다(Astrauskas et al. 2020)[2차 출처]. 경계를 필드로 좁힐 unsafe 필드(RFC 3458)는 승인되었으나 2026-09 기준 미구현이다. 일반 불변식도 같아서, 비공개 필드를 가진 타입은 모듈 밖에서 만들 수 없으니 모든 인스턴스가 검증을 통과했다고 말할 수 있다(Palmieri 2020; C-STRUCT-PRIVATE).

**오류 타입의 범위도 경계 문제다.** Jewson(2023)은 크레이트 전체 오류 enum 이 가장 흔하지만 "non-modular"(모듈적이지 않다)라며 오류 타입을 "unit of fallibility"(실패 단위) 가까이 두라 하고, 연산마다 타입을 만들면 코드가 크게 는다는 반론은 타당하다고 인정한다. Palmieri(2021)는 라이브러리와 애플리케이션의 구분이 "not the right framing"(올바른 틀이 아니다)이라며, 호출자가 반응해야 하면 enum, 보고만 하면 불투명 오류(opaque error)를 쓰라 한다. thiserror 는 전용 오류 타입에 자신을 권하지만(thiserror README) Jewson 은 라이브러리에는 쓰지 않겠다고 했다.

### 8.4 실무 지침: 단단한 경계는 크레이트에 두고, 모듈 안 구조는 관례로 정한다

**공식 문서는 모듈을 책임이 아니라 관련성과 탐색으로 나눈다.** Book 은 모듈로 "group related definitions together and name why they're related"(관련된 정의를 묶고 왜 관련되는지 이름 붙인다)라 하고, 커지면 파일로, 더 커지면 여러 크레이트로 나누라 한다(Book 7.2; Book 7.0; Book 14.3). "one task" 원칙은 함수에 쓴다(Book 12.3). 모듈 하나에 책임 하나, 파일 하나에 타입 하나, 크기 한도를 정한 공식 문서나 Rust 실무 자료는 찾지 못했다.

**실무에서 강제되는 경계는 크레이트다.** Kladov(2021b)는 1만~100만 줄 프로젝트에 평평한 `crates/*` 배치를 권하며 "there are no perfect hierarchies"(완벽한 계층은 없다)고 했다. 스스로 "in no way authoritative"(결코 권위 있는 것이 아니다)라 밝힌 경험이다. 패턴 책은 "Prefer small crates that do one thing well"(한 가지를 잘하는 작은 크레이트)을 권하지만(Rust Design Patterns) 반대 경험도 있다. rustc 는 증분·병렬 컴파일이 충분히 좋아지면 "fewer, more cohesive crates"(더 적고 응집된 크레이트)가 이상이라며 지금의 분할로 "related functionality gets scattered"(관련 기능이 흩어진다)고 인정한다(rustc-dev-guide). Tokio 0.2 는 hello world 가 크레이트 43개를 끌어오던 문제로 하위 크레이트를 한 크레이트로 합쳤고(Tokio 2019), rust-analyzer 는 "Don't use small 'helper' crates"라 한다. 크레이트 경계는 독립 소비나 안정성 약속이 필요한 자리에 생긴다. serde 는 데이터 형식 구현이 serde_derive 를 기다리지 않도록 serde_core 를 떼어 냈고, Tokio 는 std 에 `Stream` 이 들어올 때까지 tokio-stream 을 따로 두며, Bevy 와 ripgrep 은 여러 크레이트 위에 퍼사드(facade) 크레이트를 둔다(serde v1.0.220; Tokio 2020; Bevy; ripgrep `grep`).

**경계의 의도는 문서로 적는다.** Kladov(2021a)의 ARCHITECTURE.md 는 "what does the thing that I am looking at do?"(지금 보는 것은 무엇을 하나)에 답하는 코드맵(codemap)을 두되 "Avoid going into details of how each module works"(각 모듈이 어떻게 일하는지는 자세히 쓰지 말라)라고 하며, 중요한 불변식은 흔히 "an absence of something"(무언가의 부재)으로 표현된다고 한다. rust-analyzer 는 "`syntax` crate ... knows nothing about salsa or LSP" 같은 구조 불변식(architecture invariant)을 약 25개 적지만, tidy 검사가 의존 방향을 보지 않아 방향은 크레이트 경계와 문서가 지킨다(rust-analyzer architecture.md; tidy.rs).

**함수의 자리는 수신자가 정한다.** API Guidelines C-METHOD 는 "Functions with a clear receiver are methods"(수신자가 분명한 함수는 메서드)라 하되 특정 타입과 분명히 연관된 연산에 한정하고, C-CTOR 는 생성자를 연관 함수(associated function)로 둔다. Book 도 `Config::new` 가 "more idiomatic"(더 관용적)이라 하지만, 함수는 부모 모듈 경로로 부르는 것을 관용으로 소개한다(Book 12.3; Book 7.4). std 에는 `mem::swap` 같은 자유 함수가 많고, rust-analyzer 는 "Avoid creating 'doer' objects"(한 동작만 하는 객체를 만들지 말라)며 `ThingDoer::do(a, b)` 는 절충으로만 둔다(rust-analyzer style.md). 이름 공간 노릇만 하는 타입을 지지하는 글은 찾지 못했다. API Guidelines 는 스스로 "should not in any way be considered a mandate"(어떤 의미로도 강제로 여겨서는 안 된다)라 하며, 마지막 커밋은 2025-07 의 링크 수정이다.

**`mod.rs` 와 `name.rs` 는 일관성만 요구되는 선택이다.** Reference 는 `name.rs` 방식이 "avoids having many files named `mod.rs`"(`mod.rs` 가 여럿 생기지 않는다)라며 권하고, Book 은 `mod.rs` 를 "older style"(옛 방식)이라 부른다(Reference: Modules; Book 7.5). 반면 RFC 2126 은 `mod.rs` 가 "a consistent story with `lib.rs`"(`lib.rs` 와 일관된 설명)를 준다며 폐기하지 않았고, Clippy 는 정반대 린트 `mod_module_files` 와 `self_named_module_files` 를 둘 다 둔다.

### 8.5 린트와 도구: 크레이트보다 낮은 경계를 보는 표준 도구는 없다

**rustc 린트는 '내보낸 것'과 '나머지' 두 구역만 본다.** 공개 범위 린트는 모두 크레이트 밖에서 닿는지를 기준으로 하며, 크레이트 안의 의도를 보는 `unreachable_pub`, `unnameable_types`, `missing_docs` 는 allow 다. 기본 경고인 `private_interfaces`, `unused_imports`, `dead_code` 는 내보내지 않은 항목을 `pub` 여부와 상관없이 내부로 보므로, 비공개 모듈 안의 쓰이지 않는 `pub use` 는 경고를 받는다(rustc 린트 문서; rustc 소스). 린트 수준은 Cargo `[lints]` 표(1.74)로 패키지마다 정한다(Cargo Book: Manifest).

**Clippy 의 구조 린트는 기본으로 꺼져 있고, 근거는 일관성이다.** 모듈 배치, import, 공개 범위 린트는 거의 모두 restriction, pedantic, nursery 에 있다. README 는 restriction 을 "should, *emphatically*, not be enabled as a whole"(결코 통째로 켜지 말라)며 "may lint against perfectly reasonable code"(합리적인 코드도 잡을 수 있다)고 경고한다(Clippy README). 관련 린트로 `mod_module_files`·`self_named_module_files`, `inline_modules`(1.97), `pub_use`, `multiple_inherent_impl`, nursery 의 `redundant_pub_crate` 등이 있다. 기본 경고인 `module_inception` 은 1.72 부터 설정 `allow-private-module-inception` 으로 비공개 동명 모듈을 허용한다(Clippy 소스; CHANGELOG). 어느 것도 모듈 사이의 의존 방향은 보지 않고, `multiple_inherent_impl` 도 impl 블록 수만 셀 뿐 위치는 보지 않는다. 또 `unreachable_pub` 와 `redundant_pub_crate` 는 함께 만족할 수 없다. 비공개 모듈 안에서 크레이트 전체가 쓰는 항목을 `pub` 으로 쓰면 앞의 것이, `pub(crate)` 로 쓰면 뒤의 것이 걸린다.

**성숙한 도구는 크레이트와 패키지 경계에서 일한다.** cargo-semver-checks(v0.51.0, 내려받기 69만)는 거짓 양성 없이 SemVer 위반을 찾도록 설계되었으나 타입과 제네릭의 변경은 아직 놓친다고 밝힌다. cargo-public-api(v0.52.0)와 cargo-check-external-types(v0.5.0)는 공개 API 와 그 안의 외부 타입을 검사하되 nightly 의 불안정한 rustdoc JSON 에 기댄다. 크레이트 안에서는 cargo-modules(v0.27.0, 내려받기 25.5만)가 그래프를 그리고 `--acyclic` 으로 순환을 잡지만 층 규칙은 없다. 층을 선언하는 cargo-pup(별 65, 고정 nightly), arch-lint(위로 향한 의존을 위반으로 봄, 별 7), crawk(구문 분석, 별 3)는 젊고 거의 쓰이지 않는다. 구문만 보는 도구는 매크로와 glob 이 만드는 의존을 놓치고, 이름을 해석하는 도구는 툴체인을 고정해야 한다. 큰 프로젝트가 크레이트 안 배치를 기계로 검사하는 공개 사례는 플랫폼별 `cfg` 를 std 의 `sys`, `os` 모듈에 가두는 rustc tidy `pal.rs` 하나뿐이었고, 그마저 예외 목록을 둔다. 대부분은 층을 크레이트로 올리거나 불변식을 산문으로 적는다.

**로컬 실험은 이 린트들이 생성된 표면 파일에 어떻게 반응하는지 보여 준다.** ln-structure 방식으로 표면을 생성한 예제 크레이트(층 l0~l3, `mod.rs` 표면 15개, `lib.rs` 는 `App` 하나만 다시 내보냄)를 cargo 1.99.0, Clippy 0.1.99 로 검사했다(실험 R2). 생성된 그대로(`allow-private-module-inception = true`, 층 표면의 `#![allow(unused_imports)]`)는 경고가 0건이었고, 설정을 지우면 `module_inception` 8건, allow 를 지우면 `unused_imports` 6건이 났다. `unreachable_pub` 를 켜면 31건이었다(`unnameable_types` 0건, `missing_docs` 3건). restriction·nursery 린트 열 개를 켜면 `missing_docs_in_private_items` 46건, `pub_use` 20건, `mod_module_files` 15건, `redundant_pub_crate` 9건이 났고, `self_named_module_files`, `inline_modules`, `module_name_repetitions`, `multiple_inherent_impl`, `wildcard_imports`, `absolute_paths` 는 0건이었다. `redundant_pub_crate` 는 설명과 달리 크레이트 루트의 비공개 모듈에서도 발동했다. ln-structure 에 대한 함의는 별도 장에서 다룬다.

### 8.6 정리: Rust 에서 특별히 요구되거나 권장되는 것

| 항목 | 종류 | 2026-10 상태 | 근거 |
|---|---|---|---|
| 기본 비공개, 공개 범위는 조상 쪽으로만 열고 다시 내보내기로 넓힐 수 없다 | 컴파일러 강제 | E0364 | Reference: Visibility; 실험 R1 |
| 고아·일관성 규칙, 고유 impl 은 같은 크레이트에 | 컴파일러 강제(크레이트 단위) | E0116, E0117 | Reference: Implementations |
| 패키지 순환은 금지, 모듈 순환은 허용 | Cargo 강제(모듈 순환은 컴파일러가 허용) | dev-dependency 예외 | Cargo Book: Resolver; RFC 1560 |
| `pub use` 로 내부와 다른 공개 구조를 만든다 | 공식 권고 | 라이브러리 밖 코드에는 반론 | Book 7.4; rust-analyzer style.md |
| 공개 항목의 이동은 major(`pub use` 로 완화), glob 은 줄인다 | 공식 권고(패키지 단위), glob 은 일부 컴파일러 강제 | 1.94, 1.98 에 강화 | Cargo Book: SemVer; RELEASES.md |
| 닿지 않는 `pub` 대신 `pub(crate)` | 린트(allow), 공식 권고 | `redundant_pub_crate` 와 충돌 | RFC 2126; C-HIDDEN |
| 공개 시그니처의 타입은 이름 붙일 수 있게 | 린트 | warn(1.74), allow(1.79) | RFC 2145 |
| 봉인 트레이트로 바깥 구현을 막는다 | 공식 권고 | 언어 지원(RFC 3323) 불안정 | C-SEALED; Gruevski 2023 |
| 수신자가 분명하면 메서드, 생성자는 연관 함수 | 공식 권고 | 자유 함수도 관용 | C-METHOD; C-CTOR; Book 7.4 |
| 확장 트레이트는 아껴 쓰고 `FooExt` 로 | 공식 권고(RFC 관례) | 1.0 에 일부 통합 | RFC 445; RFC 735 |
| `name.rs` 권장, `mod.rs` 허용, 한 방식으로 통일 | 공식 권고, 린트 | 서로 반대인 린트 둘 | Reference: Modules; RFC 2126 |
| unsafe 는 가장 작은 모듈에, 내부 가변성은 최후 수단 | 공식 권고(형식 논증이 뒷받침) | unsafe 필드 미구현 | Nomicon; Jung 2016; std::cell |
| async 트레이트의 dyn 호환성과 `Send` 는 작성자가 정한다 | 컴파일러 강제 | 1.75 | Reference: Traits; Mandry 2023 |
| 크레이트 경계에는 제네릭 대신 `dyn` | 실무 관례(전문가 의견) | — | Kladov 2021c; Anderson 2020a |
| 오류 타입은 실패 단위나 호출자의 필요에 맞춘다 | 실무 관례(전문가 의견, 합의 없음) | 전체 enum 이 여전히 흔함 | Jewson 2023; Palmieri 2021 |
| 단단한 경계는 크레이트, 의도는 구조 불변식 문서로 | 실무 관례 | 반대 경험 있음 | Kladov 2021a, 2021b; rustc-dev-guide |
| 크레이트 안의 층, 순환, impl 위치, 파일당 타입 수 | 강제 수단 없음 | 외부 도구는 젊음 | Reference; Clippy; cargo-modules |

### 참고문헌 (8장)

공식 문서, RFC, 컴파일러 소스
- Book 7.0: Klabnik, S., Nichols, C. & Krycho, C. *The Rust Programming Language*, 7장 "Managing Growing Projects with Packages, Crates, and Modules". Rust 1.98.0 이상, edition 2024 기준. https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html (판 정보: https://doc.rust-lang.org/book/title-page.html)
- Book 7.2: "Defining Modules to Control Scope and Privacy". https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html
- Book 7.4: "Bringing Paths into Scope with the use Keyword". https://doc.rust-lang.org/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html
- Book 7.5: "Separating Modules into Different Files". https://doc.rust-lang.org/book/ch07-05-separating-modules-into-different-files.html
- Book 12.3: "Improving Error Handling and Modularity". https://doc.rust-lang.org/book/ch12-03-improving-error-handling-and-modularity.html
- Book 14.3: "Cargo Workspaces". https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html
- Reference: Visibility: *The Rust Reference*, "Visibility and privacy" (master, 2026-10). https://doc.rust-lang.org/reference/visibility-and-privacy.html
- Reference: Crates: "Crates and source files". https://doc.rust-lang.org/reference/crates-and-source-files.html
- Reference: Use declarations. https://doc.rust-lang.org/reference/items/use-declarations.html
- Reference: Modules. https://doc.rust-lang.org/reference/items/modules.html
- Reference: Implementations. https://doc.rust-lang.org/reference/items/implementations.html
- Reference: Type system attributes (`non_exhaustive`). https://doc.rust-lang.org/reference/attributes/type_system.html
- Reference: Method-call expressions. https://doc.rust-lang.org/reference/expressions/method-call-expr.html
- Reference: Traits (dyn compatibility). https://doc.rust-lang.org/reference/items/traits.html
- 오류 코드 E0364, E0116, E0117. https://doc.rust-lang.org/error_codes/E0364.html , https://doc.rust-lang.org/error_codes/E0116.html , https://doc.rust-lang.org/error_codes/E0117.html
- Nomicon: Splitting Borrows. *The Rustonomicon*. https://doc.rust-lang.org/nomicon/borrow-splitting.html
- Nomicon: Working with Unsafe. https://doc.rust-lang.org/nomicon/working-with-unsafe.html
- std::cell: Rust 표준 라이브러리 문서, `std::cell`. https://doc.rust-lang.org/std/cell/index.html
- Edition Guide 2018: "Path and module system changes". https://doc.rust-lang.org/edition-guide/rust-2018/path-changes.html
- Cargo Book: SemVer: "SemVer Compatibility". https://doc.rust-lang.org/cargo/reference/semver.html
- Cargo Book: Resolver: "Dependency Resolution", dev-dependency cycles. https://doc.rust-lang.org/cargo/reference/resolver.html#dev-dependency-cycles
- Cargo Book: Manifest: `[lints]` 절(1.74 부터). https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section
- RELEASES.md: Rust 릴리스 노트, 1.99.1(2026-10-15)까지. https://github.com/rust-lang/rust/blob/main/RELEASES.md
- rustc 린트 문서: *The rustc book*, "Allowed-by-default lints", "Warn-by-default lints". https://doc.rust-lang.org/rustc/lints/listing/allowed-by-default.html , https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html
- rustc 소스: `rustc_lint_defs/src/builtin.rs`, `rustc_resolve/src/check_unused.rs`, `rustc_passes/src/dead.rs`. https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_lint_defs/src/builtin.rs , https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_resolve/src/check_unused.rs , https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_passes/src/dead.rs
- rustc partitioning.rs: `rustc_monomorphize/src/partitioning.rs` (master, 2026-10). https://raw.githubusercontent.com/rust-lang/rust/master/compiler/rustc_monomorphize/src/partitioning.rs
- rustc tidy `pal.rs`. https://github.com/rust-lang/rust/blob/HEAD/src/tools/tidy/src/pal.rs
- rustc-dev-guide: "High-level overview of the compiler source". https://github.com/rust-lang/rustc-dev-guide/blob/master/src/compiler-src.md
- API Guidelines: Rust library team, *Rust API Guidelines* (마지막 커밋 2025-07-08). About https://rust-lang.github.io/api-guidelines/about.html ; C-METHOD, C-CTOR https://rust-lang.github.io/api-guidelines/predictability.html#c-method ; C-SEALED, C-STRUCT-PRIVATE https://rust-lang.github.io/api-guidelines/future-proofing.html ; C-HIDDEN https://rust-lang.github.io/api-guidelines/documentation.html#c-hidden
- RFC 155 (2014), 고유 impl 을 타입과 같은 모듈에만. https://rust-lang.github.io/rfcs/0155-anonymous-impl-only-in-same-module.html
- RFC 445 (Turon 2014), "Extension trait conventions". https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html
- RFC 735 (2015), 고유 impl 을 크레이트 안 어디에나. https://rust-lang.github.io/rfcs/0735-allow-inherent-impls-anywhere.html
- RFC 1560 (Cameron 2016), "Name resolution". https://rust-lang.github.io/rfcs/1560-name-resolution.html
- RFC 2126 (Turon 2017), "Path clarity". https://rust-lang.github.io/rfcs/2126-path-clarity.html
- RFC 2145 (Petrochenkov 2017), "Type privacy". https://rust-lang.github.io/rfcs/2145-type-privacy.html
- RFC 3323 (jhpratt 2022), "Restrictions". 추적 이슈 #105077 미해결. https://rust-lang.github.io/rfcs/3323-restrictions.html , https://github.com/rust-lang/rust/issues/105077
- RFC 3373 (2022), 함수 안의 비지역 정의 회피(`non_local_definitions`). https://rust-lang.github.io/rfcs/3373-avoid-nonlocal-definitions-in-fns.html
- RFC 3458 (2023), "Unsafe fields". 추적 이슈 #132922, 2026-09-01 갱신 기준 미구현. https://rust-lang.github.io/rfcs/3458-unsafe-fields.html , https://api.github.com/repos/rust-lang/rust/issues/132922
- RFC 3516 (Page 2023), 공개·비공개 의존. Cargo 불안정 기능 `public-dependency`, 추적 이슈 #44663. https://doc.rust-lang.org/cargo/reference/unstable.html#public-dependency , https://github.com/rust-lang/rust/issues/44663
- Mandry, T. (2023). "Announcing `async fn` and return-position `impl Trait` in traits." Rust Blog, 2023-12-21. https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/
- Go spec: *The Go Programming Language Specification*, "Method declarations". https://go.dev/ref/spec
- GHC: GHC User's Guide, `-Worphans`. https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html
- SE-0364: Swift Evolution, 외부 타입의 사후 준수 경고(Swift 6.0 구현). https://raw.githubusercontent.com/swiftlang/swift-evolution/main/proposals/0364-retroactive-conformance-warning.md

린트와 도구
- Clippy README (master, 2026). https://github.com/rust-lang/rust-clippy/blob/HEAD/README.md
- Clippy CHANGELOG. https://github.com/rust-lang/rust-clippy/blob/HEAD/CHANGELOG.md
- Clippy 소스: `module_style.rs`(`mod_module_files`, `self_named_module_files`, `inline_modules`), `item_name_repetitions.rs`(`module_inception`), `pub_use.rs`, `redundant_pub_crate.rs`, `inherent_impl.rs`(`multiple_inherent_impl`). https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/module_style.rs , https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/item_name_repetitions.rs , https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/pub_use.rs , https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/redundant_pub_crate.rs , https://raw.githubusercontent.com/rust-lang/rust-clippy/master/clippy_lints/src/inherent_impl.rs
- cargo-modules (Esche, v0.27.0, 2026-08-03). https://github.com/regexident/cargo-modules
- cargo-public-api (Nordholts 외, v0.52.0, 2026-05). https://github.com/cargo-public-api/cargo-public-api
- cargo-semver-checks (Gruevski, v0.51.0, 2026-10-03). https://github.com/obi1kenobi/cargo-semver-checks
- cargo-check-external-types (AWS Labs, v0.5.0, 2026-06). https://github.com/awslabs/cargo-check-external-types
- cargo-pup (Datadog, 0.1.8, 2026-06). https://github.com/DataDog/cargo-pup
- arch-lint (ynishi, 0.9.0, 2026-10). https://github.com/ynishi/arch-lint
- crawk (0.7.1, 2026-10). https://github.com/BartoszCiesla/crawk

전문가와 실무 자료
- Anderson, B. (2020a). "The Rust Compilation Model Calamity." PingCAP, 2020-01-30. https://www.pingcap.com/blog/rust-compilation-model-calamity/
- Anderson, B. (2020b). "Rust's Huge Compilation Units." PingCAP, 2020-06-22. https://www.pingcap.com/blog/rust-huge-compilation-units/
- Bevy: Bevy Quick Start, "Plugins"; `bevy` 컨테이너 크레이트 `lib.rs`. https://bevy.org/learn/quick-start/getting-started/plugins/ , https://github.com/bevyengine/bevy/blob/main/src/lib.rs
- Drysdale, D. (2024). *Effective Rust*, Item 22 "Minimize visibility". O'Reilly. https://effective-rust.com/visibility.html
- Gruevski, P. (2023). "A definitive guide to sealed traits in Rust." predr.ag, 2023-04-05. https://predr.ag/blog/definitive-guide-to-sealed-traits-in-rust/
- Jewson, S. (2023). "Modular Errors in Rust." 2023-04-08. https://sabrinajewson.org/blog/errors
- Jung, R. (2016). "The Scope of Unsafe." ralfj.de, 2016-01-09. https://www.ralfj.de/blog/2016/01/09/the-scope-of-unsafe.html
- Kladov, A. (2021a). "ARCHITECTURE.md." matklad.github.io, 2021-02-06. https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html
- Kladov, A. (2021b). "Large Rust Workspaces." 2021-08-22. https://matklad.github.io/2021/08/22/large-rust-workspaces.html
- Kladov, A. (2021c). "Fast Rust Builds." 2021-09-04. https://matklad.github.io/2021/09/04/fast-rust-builds.html
- Kladov, A. (2021d). "Notes On Module System." 2021-11-27. https://matklad.github.io/2021/11/27/notes-on-module-system.html
- LogLog Games (2024). "Leaving Rust gamedev after 3 years." 2024-04-26. https://loglog.games/blog/leaving-rust-gamedev/
- Matsakis, N. (2018). "After NLL: Interprocedural conflicts." Baby Steps, 2018-11-01. https://smallcultfollowing.com/babysteps/blog/2018/11/01/after-nll-interprocedural-conflicts/
- Matsakis, N. (2021). "View types for Rust." Baby Steps, 2021-11-05. https://smallcultfollowing.com/babysteps/blog/2021/11/05/view-types/
- Palmieri, L. (2020). "Zero To Production #6: Domain Modelling." 2020-12. https://www.lpalmieri.com/posts/2020-12-11-zero-to-production-6-domain-modelling/
- Palmieri, L. (2021). "Error Handling In Rust - A Deep Dive." 2021-05. https://www.lpalmieri.com/posts/error-handling-rust/
- ripgrep `grep`: `crates/grep/src/lib.rs`(ripgrep 핵심 크레이트의 퍼사드). https://github.com/BurntSushi/ripgrep/blob/master/crates/grep/src/lib.rs
- Rust Design Patterns (rust-unofficial, 2026-10 열람): "Struct decomposition for independent borrowing" https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html ; "Prefer small crates" https://rust-unofficial.github.io/patterns/patterns/structural/small-crates.html ; "Contain unsafety in small modules" https://rust-unofficial.github.io/patterns/patterns/structural/unsafe-mods.html
- rust-analyzer architecture.md, style.md, tidy.rs (2026-10 열람). https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/architecture.md , https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/style.md , https://github.com/rust-lang/rust-analyzer/blob/HEAD/xtask/src/tidy.rs
- serde v1.0.220 릴리스(2025-09-13, serde_core 분리). https://github.com/serde-rs/serde/releases/tag/v1.0.220
- thiserror README (dtolnay, 2.0.21). https://raw.githubusercontent.com/dtolnay/thiserror/master/README.md
- Tokio (2019). "Announcing Tokio 0.2 and a Roadmap to 1.0." 2019-11-26. https://tokio.rs/blog/2019-11-tokio-0-2
- Tokio (2020). Lerche, C. "Announcing Tokio 1.0." 2020-12-23. https://tokio.rs/blog/2020-12-tokio-1-0
- tokio#3257: "Does tokio::prelude carry its weight?" (2020-12-11). https://github.com/tokio-rs/tokio/issues/3257
- West, C. (2018). "Using Rust For Game Development." RustConf 2018 폐막 기조연설 글, 2018-09-14. https://kyren.github.io/2018/09/14/rustconf-talk.html

학술 연구
- Astrauskas, V. et al. (2020). "How Do Programmers Use Unsafe Rust?" *PACMPL* 4 (OOPSLA), Art. 136. DOI 10.1145/3428204. https://2020.splashcon.org/details/splash-2020-oopsla/12/How-Do-Programmers-Use-Unsafe-Rust- [2차 출처: 검색 발췌와 서지 기록의 초록, 본문 미열람]
- Evans, A. N., Campbell, B. & Soffa, M. L. (2020). "Is Rust Used Safely by Software Developers?" *ICSE 2020*. DOI 10.1145/3377811.3380413. https://arxiv.org/abs/2007.00752 (초록만 확인)
- Jung, R., Jourdan, J.-H., Krebbers, R. & Dreyer, D. (2018). "RustBelt: Securing the Foundations of the Rust Programming Language." *POPL 2018*. https://plv.mpi-sws.org/rustbelt/popl18/ (초록만 확인)

로컬 실험
- 실험 R1: 이 조사에서 rustc·cargo 1.99.0, edition 2024 로 한 컴파일 실험(2026-10-18). 서로 `use` 하는 두 모듈(진단 없음), 다른 모듈의 고유 impl(컴파일됨), E0116, E0117, E0364, E0761, 서로 의존하는 두 path 패키지("cyclic package dependency"), dev-dependency 로만 닫힌 순환(빌드됨), `private_interfaces` 경고, `unnameable_types` 를 켠 봉인 트레이트 경고.
- 실험 R2: 이 조사에서 cargo 1.99.0, Clippy 0.1.99 로 ff-lntools `tests/fixtures/rust_clean` 사본에 린트를 적용한 실험(2026-10-18).
