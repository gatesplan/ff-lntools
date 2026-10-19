# 8장(Rust) 부속: 규칙 후보와 ln-structure 시사점

최종 작성자용 메모다. 출처 표기는 `s6_rust.md` 의 '참고문헌 (8장)'과 같고, 그 목록에 없는 출처는 맨 끝 '이 파일에만 나오는 출처'에 URL 과 함께 적었다. e1~e4 는 조사 노트(`e1_rust_official.md`, `e2_rust_practice.md`, `e3_rust_language_forces.md`, `e4_rust_lints_tools.md`)를 뜻하며, 'e3 추론'처럼 적은 것은 출처의 직접 진술이 아니라 노트 작성자의 추론이다. 강도는 종류(컴파일러 강제 / 공식 / 린트 / 실무 관례 / 전문가 의견)와 세기(강/중/약)로 적었다.

## 규칙 후보

1. **모듈 사이 의존은 한 방향 DAG 로 두고, 순환은 외부 검사기로 막는다.**
   - 근거: Cargo 는 패키지 순환을 거부하고(dev-dependency 만 예외) 패키지를 나눠 "strictly acyclic"하게 하라고 권한다. 서로 의존하는 모듈은 "cannot be trivially reduced further into separate crates"이므로, 모듈 그래프가 비순환이면 나중에 크레이트로 올리기 쉽다. "X 는 Y 를 모른다" 같은 부재 불변식은 방향 규칙으로 기계 검사할 수 있다.
   - 출처: Cargo Book: Resolver; 실험 R1; Anderson 2020b; Kladov 2021c; Kladov 2021a; rust-analyzer architecture.md.
   - 강도: 크레이트 단위는 Cargo 강제(강). 모듈 단위는 유추와 전문가 의견(중).
   - 반론과 한계: rustc 는 모듈 순환을 의도적으로 허용한다(RFC 1560, 진단 없음). Kladov(2021d)는 "crates (which form a DAG) and modules (which might be mutually dependent)"의 분리를 장점으로 꼽는다. cargo-modules 자신의 소스에도 모듈 순환이 있다. 공식 규칙도 린트도 없으므로 이것은 Rust 의 가치가 아니라 프로젝트의 규율이다.

2. **크레이트 밖에서 닿지 않는 항목의 공개 표기(`pub` 또는 `pub(crate)`)를 한 정책으로 통일하고, 그 정책과 맞는 린트만 켠다.**
   - 근거: 비공개 모듈 안의 `pub` 은 "tell you less than you might hope"(RFC 2126). rustc 는 `unreachable_pub` 문서에서 `pub(crate)` 를 권하고 이 린트가 "eventually" 기본 경고가 되기를 바란다. C-HIDDEN, Drysdale Item 22 도 `pub(crate)` 를 권한다. Kladov(2021d)는 `pub(crate)` 와 `-Dunreachable_pub` 조합을 제안한다.
   - 출처: RFC 2126; rustc 린트 문서; C-HIDDEN; Drysdale 2024; Kladov 2021d.
   - 강도: 린트(allow) + 공식 권고, 중.
   - 반론과 한계: `unreachable_pub` 와 Clippy nursery 의 `redundant_pub_crate` 는 함께 만족할 수 없다(실험 R2 에서 각각 31건, 9건). 비공개 모듈 안에서는 `pub` 과 `pub(crate)` 의 유효 공개 범위가 같아 표기는 의도 표시일 뿐이다(e4). Kladov 는 한 크레이트 안의 공개 범위 세분이 코드를 의미 있게 낫게 하지 않는다고 본다(확신도 0.5).

3. **공개 시그니처에 나오는 타입은 같은 표면에서 이름 붙일 수 있어야 한다. 일부러 이름을 숨긴 항목은 표시한다.**
   - 근거: RFC 2145 가 기준을 유효 공개 범위로 바꿨다. `private_interfaces`(warn, 1.74): "Having something private in primary interface guarantees that the item will be unusable from outer modules". `unnameable_types`(allow, 1.79)의 처방: "reexport the type properly to make it nameable, or document that users are not supposed to be able to name it". Drysdale Item 24: API 에 나오는 의존의 타입은 다시 내보낸다.
   - 출처: RFC 2145; rustc 린트 문서; RELEASES.md; Drysdale 2024 Item 24.
   - 강도: 린트, 중~강(`private_interfaces` 는 기본 경고).
   - 반론과 한계: RFC 2145 는 'Voldemort' 패턴에 "legitimate uses"가 있다고 하며, 봉인 트레이트가 대표다(`unnameable_types` 가 이를 잡는다, 실험 R1). rustc 린트는 크레이트 경계에서만 작동하므로 모듈 표면 단위의 검사는 외부 도구 몫이다. `unnameable_types` 는 `dyn`, `impl Trait` 로 새는 트레이트도 본다(e4).

4. **표면의 다시 내보내기는 이름을 하나씩 적고, glob 다시 내보내기를 쓰지 않는다.**
   - 근거: glob import 는 상대가 항목을 더하기만 해도 깨질 수 있다(Cargo SemVer). RFC 1560 의 원칙 "Glob imports should be manually expandable". 1.94(모호한 glob 다시 내보내기가 다른 크레이트에서도 보임), 1.98(모호한 glob import 일부를 하드 오류로). Kladov(2021d): glob 다시 내보내기를 금지하면 모듈의 모든 이름이 적혀 "useful for tooling". Drysdale Item 23. Tokio 1.0 의 `tokio::prelude` 제거(IDE 자동 import 로 prelude 가 덜 필요해졌다는 의견).
   - 출처: Cargo Book: SemVer; RFC 1560; RELEASES.md; Kladov 2021d; Drysdale 2024 Item 23; tokio#3257.
   - 강도: 공식 권고 + 일부 컴파일러 강제, 중~강.
   - 반론과 한계: Drysdale 은 "`mod thing; pub use thing::*;`"(모듈을 코드 나누기로만 쓰는 크레이트)와 잘 고른 prelude 를 예외로 둔다. Bevy 는 `use bevy::prelude::*;` 를 권한다. RFC 445 는 확장 트레이트가 늘린 import 를 glob prelude 로 덜도록 했다. Clippy `wildcard_imports`(pedantic)는 `pub use` 를 통한 glob 을 기본으로 예외 처리한다.

5. **내부 구조와 다른 공개 구조는 생성된 `pub use` 표면으로만 만들고, 표면에 이름을 더하는 일은 의존을 더하는 일처럼 검토한다.**
   - 근거: Book 7.4, 14.2("expose a different structure", "decouples that internal structure from what you present to your users"). Reference 의 비공개 '도우미 모듈' 관용구. std::iter::adapters 와 `pub(in crate::iter)`(Drysdale Item 22). 공개 항목 이동은 major 이고 `pub use` 가 완화책이다. E0364 덕분에 `pub(crate)` 항목은 다시 내보내도 새지 않는다. rust-analyzer 는 "Scale of Changes"에서 다른 크레이트 항목의 `pub use` 추가를 `[dependencies]` 줄 추가와 같은 '새 의존' 등급으로 보고 "adding an innocent-looking `pub use` is a very simple way to break encapsulation"이라 경고한다.
   - 출처: Book 7.4; Book 14.2; Reference: Visibility; Drysdale 2024; Cargo Book: SemVer; 실험 R1; rust-analyzer style.md.
   - 강도: 공식 권고, 중.
   - 반론과 한계: rust-analyzer 는 라이브러리가 아닌 코드에서 다시 내보내기를 기본적으로 피한다("two ways to use something"). Clippy `pub_use`(restriction)는 다시 내보내기 자체를 막는다(실험 R2 에서 20건).

6. **impl 블록은 타입을 정의한 모듈에 둔다(트레이트 impl 은 타입이나 트레이트의 모듈). 다른 모듈에서 메서드를 더해야 하면 `FooExt` 확장 트레이트를 아껴 쓴다.**
   - 근거: 고유 메서드는 import 없이, 트레이트 메서드는 트레이트만 있으면 호출되므로 impl 이 놓인 모듈은 `use` 에 드러나지 않는다(Reference 의 메서드 조회; e3 의 '숨은 간선'). RFC 155(2014)가 같은 규칙을 두었고 목적에 "to enforce consistency in code layout"을 넣었다. 이를 되돌린 RFC 735 도 "Consistency and ease of finding method definitions by looking at the module the type is defined in"을 잃는다고 인정했다. Go(수신자 타입과 같은 패키지), GHC `-Worphans`(모듈 단위 고아 인스턴스), Swift SE-0364(사후 준수 경고, `@retroactive`), rustc `non_local_definitions`(RFC 3373, "can create discrepancies in tooling"), Clippy `multiple_inherent_impl` 의 module/file 범위("Splitting the implementation of a type makes the code harder to navigate")가 같은 계열이다. 이름은 RFC 445 의 `FooExt`.
   - 출처: Reference: Method-call expressions; RFC 155; RFC 735; RFC 445; Go spec; GHC; SE-0364; RFC 3373; Clippy 소스(inherent_impl.rs).
   - 강도: 컴파일러는 크레이트 단위만 강제한다. 모듈 단위는 선례와 전문가 의견, 중.
   - 반론과 한계: Rust 는 이 규칙을 1년도 안 되어 되돌렸다. 원래 동기가 'fake modules'라는 구현 세부였고 그것이 사라졌다는 점, 규칙이 "non-DRY single use extension traits, the worst offender being `AstBuilder` in libsyntax"를 낳는다는 점이 이유였다. 확장 트레이트는 import 를 늘리고(RFC 445 의 "extension traits tend to require additional imports"), RFC 445 자신이 "should be used sparingly"라 한다. 제네릭 impl 에서는 '정의한 모듈'이 정해지지 않는다(아래 시사점). RFC 155 가 실제로 얼마나 구현되었는지는 [미확인]. `non_local_definitions` 가 기본 경고가 된 판도 [미확인].

7. **수신자가 분명한 연산은 메서드로, 생성자는 연관 함수 `new` 로 둔다.**
   - 근거: C-METHOD "Functions with a clear receiver are methods", 대상은 "any operation that is clearly associated with a particular type". 메서드는 import 가 필요 없고 "what can I do with a value of type `T`"에 답하기 쉽다. C-CTOR "Constructors are static (no `self`) inherent methods". Book 12.3 은 `Config::new` 가 "more idiomatic"이라 한다. Rust Design Patterns 의 생성자 관용 "the convention is to use an associated function `new`".
   - 출처: API Guidelines C-METHOD, C-CTOR; Book 12.3; Rust Design Patterns(ctor).
   - 강도: 공식 권고, 강(조건부).
   - 반론과 한계: 수신자가 없는 함수는 자유 함수가 관용이다. Book 7.4 는 부모 모듈을 import 해 `hosting::add_to_waitlist()` 로 부르는 것을 관용이라 하며 "There's no strong reason behind this idiom"이라 한다. std(`mem::swap`, `fs::read_to_string`, `thread::spawn`)와 C-NEWTYPE-HIDE 의 예(`pub fn my_transform`)도 자유 함수다. rust-analyzer 는 "Avoid creating 'doer' objects"라며 `do_thing(arg1, arg2)` 를 GOOD 으로, `ThingDoer::do(arg1, arg2)` 는 수고를 덜 때만 쓰는 "middle ground"로 둔다. 이름 공간용 타입을 옹호하는 Rust 자료는 찾지 못했다(e2).

8. **모듈 파일 방식(`mod.rs` 또는 `name.rs`)을 하나로 정해 Clippy 린트로 고정하고, 인라인 모듈도 린트로 막는다.**
   - 근거: RFC 2126 은 `mod.rs` 를 폐기하지 않으면서 "It is expected that tooling like Clippy will push for at least style consistency"라 했다. Clippy 는 `mod_module_files`("bans `mod.rs` files")와 `self_named_module_files`("uses only `mod.rs` files")를 둘 다 restriction 으로 둔다(1.57). `inline_modules`(restriction, 1.97, 2026-07)는 `#[cfg(test)]` 모듈을 뺀 인라인 모듈을 막는다. Kladov(2021d)는 엄격한 스타일 관리가 없는 큰 프로젝트가 결국 두 방식을 섞는다고 한다.
   - 출처: RFC 2126; Clippy 소스(module_style.rs); CHANGELOG; Kladov 2021d.
   - 강도: 린트(restriction), 중.
   - 반론과 한계: 공식 문서는 `name.rs` 를 권한다(Reference: Modules 의 note, Book 7.5 의 "older style", Edition Guide 2018). 근거는 "many files named `mod.rs`"라는 탐색 비용이다. Clippy 배치 린트의 근거는 일관성뿐이다("Having multiple module layout styles in a project can be confusing").

9. **`unsafe` 와 그 불변식은 그것을 지킬 수 있는 가장 작은 모듈에 가두고, 관련 필드의 공개 범위를 넓히지 않는다.**
   - 근거: Nomicon "pollutes a whole *module*", "the only bullet-proof way to limit the scope of unsafe code is at the module boundary with privacy". Jung 2016 "the scope of `unsafe` ends at the next abstraction boundary". RustBelt(초록만 확인)의 라이브러리별 검증 조건. Rust Design Patterns "create the smallest possible module that can uphold the needed invariants". Rust 2024 는 `unsafe_op_in_unsafe_fn` 을 기본 경고로 바꿨다.
   - 출처: Nomicon: Working with Unsafe; Jung 2016; Jung et al. 2018; Rust Design Patterns(unsafe-mods); Edition Guide 2024(unsafe_op_in_unsafe_fn).
   - 강도: 공식 문서 + 형식 논증, 강.
   - 반론과 한계: 알맞은 인터페이스를 찾기 어렵고 비효율이 생길 수 있다(Patterns). 공개 범위로 막는 우회는 "may be untenable when split borrows are required"(RFC 3458). 실증은 부분적이다(Evans et al. 2020 초록, Astrauskas et al. 2020 [2차 출처]: 대부분 잘 감싸져 있으나 상호 운용에 널리 쓰임). 필드 단위 경계인 unsafe 필드(RFC 3458)는 2026-09 기준 미구현.

10. **불변식은 그것을 가진 타입이 비공개 필드와 생성자로 지킨다(검증 함수보다 타입).**
    - 근거: 비공개 필드면 모듈 밖에서 인스턴스를 만들 수 없으므로 "*any* instance of `SubscriberName` will satisfy all our validation constraints", 반면 `is_valid_name` 같은 함수는 "a false sense of safety"(Palmieri 2020). C-STRUCT-PRIVATE: 필드 공개는 "a strong commitment". Clippy `partial_pub_fields` 는 타입이 불변식을 지키는 추상 자료형이거나 불변식 없는 데이터여야 한다고 본다. King(2019)의 "Parse, don't validate"(예시는 Haskell).
    - 출처: Palmieri 2020; API Guidelines C-STRUCT-PRIVATE; Clippy partial_pub_fields; King 2019.
    - 강도: 공식 권고 + 전문가 의견, 중~강.
    - 반론과 한계: 비공개 필드는 바깥 호출자의 독립 빌림을 막는다(Matsakis 2021). 타입 상태(typestate)는 상태마다 타입을 늘리고 봉인 트레이트에 기댄다(Biffle 2019). 결함률에 대한 실증은 없다(e3).

11. **공개 타입에 내부 가변성(`RefCell`, `Rc<RefCell<_>>`)을 쓰는 일은 최후 수단으로 보고 드러낸다.**
    - 근거: std::cell "inherited mutability is preferred, and interior mutability is something of a last resort". 내부 가변성은 빌림 충돌을 없애지 않고 실행 시 패닉으로 옮긴다(West 2018 의 "a RefCell panic", LogLog 2024 의 `RefCell` 충돌 사례).
    - 출처: std::cell; West 2018; LogLog Games 2024.
    - 강도: 공식 문서, 중(검사 규칙으로서는 약).
    - 반론과 한계: std 도 정당한 쓰임 세 가지를 든다(불변 값 '안쪽'의 가변성, 논리적으로 불변인 메서드의 구현 세부, `Clone` 의 변경 구현). 정적 의존 분석으로는 보이지 않는 문제다(e3).

12. **오류 타입은 실패 단위나 호출자가 구별해야 하는 것에 맞추고, 상위 오류가 하위 오류를 `source` 로 감싼다. 아래 층에 크레이트 전체 오류 enum 을 두지 않는다.**
    - 근거: Jewson(2023): 크레이트 전체 enum 은 "by far the most *common* way"지만 "non-modular"이고, 비공개로 두려던 의존을 오류 타입으로 공개 API 에 새게 할 위험이 있으며, 오류 타입은 "near to their unit of fallibility"에 둔다. Palmieri(2021): 호출자가 반응해야 하면 enum, 보고만 하면 불투명 오류. Gallant: 라이브러리가 고유한 오류를 알려야 하면 자기 오류 타입을 정의한다. 층 구조에서 아래 층의 전체 enum 은 위층의 실패를 이름 지어야 하므로 지식이 위로 흐른다(e3 추론).
    - 출처: Jewson 2023; Palmieri 2021; Gallant.
    - 강도: 전문가 의견, 중.
    - 반론과 한계: 크레이트 전체 enum 이 가장 흔하고 편하다. 연산마다 타입을 만들면 코드가 크게 는다(Jewson 도 "definitely a valid criticism"이라 인정). thiserror 를 두고 의견이 갈린다(thiserror README 는 전용 오류 타입에 권하고, Jewson 은 라이브러리에는 쓰지 않겠다고 함). 오류 설계 전략을 비교한 실증은 없다.

13. **경계와 주입 자리에는 `dyn` 을 기본으로 쓰고 제네릭은 성능이 필요할 때만 쓴다. 비동기 트레이트는 dyn 호환성과 `Send` 결정을 명시한다.**
    - 근거: 제네릭은 쓰는 쪽에서 단형화되어 정의한 크레이트는 타입 검사만 하므로 비용이 소비자로 옮겨진다(Kladov 2021c "accidentally-quadratic compilation times", Anderson 2020a 의 코드 팽창). Kladov 의 규칙: "do not put generic code at the boundaries between the crates", "prefer `&dyn Fn()` over `impl Fn()`", "generic, inline hotpath; concrete, outline coldpath". Endler: 제네릭 함수 안의 비제네릭 안쪽 함수. rustc 는 모듈마다 비제네릭(stable)과 단형화(volatile) 코드 생성 단위를 나눈다.
    - 출처: Kladov 2021c; Anderson 2020a; Endler 2026; rustc partitioning.rs; Reference: Traits; Mandry 2023.
    - 강도: 빌드 근거는 전문가 의견, 중. dyn 호환성 조건 자체는 컴파일러 강제.
    - 반론과 한계: dyn 호환성은 제네릭 메서드, `async fn`, `impl Trait` 반환, 연관 상수를 막아 트레이트 설계를 제약한다. 트레이트 안 `async fn`(1.75)은 dyn 호환이 아니고 `Send` 여부는 "you as a trait author need to make a choice". 이후의 dyn async 지원과 `trait-variant` 의 dyn 지원은 [미확인]. Kladov 의 근거는 크레이트 경계이며, 한 크레이트 안 모듈 경계에서의 빌드 효과는 잰 적이 없다. Kladov 스스로 빌드 시간 작업을 "in some sense busy-work"라 한다.

14. **구조 불변식(무엇이 무엇에 의존하지 않는가)과 모듈의 책임은 '무엇'으로 짧게 적고, 기계로 검사할 수 있는 것은 검사한다.**
    - 근거: Kladov 2021a: 코드맵은 "what does the thing that I am looking at do?"에 답하되 "Avoid going into details of how each module works", "only specify things that are unlikely to frequently change", "Explicitly call-out architectural invariants. Often, important invariants are expressed as an absence of something". rust-analyzer architecture.md 의 'Architecture Invariant' 약 25개("`syntax` crate ... knows nothing about salsa or LSP"). Book 7.2 "name why they're related". 크레이트 안 배치 규칙의 기계 검사 사례: rustc tidy `pal.rs`.
    - 출처: Kladov 2021a; rust-analyzer architecture.md; Book 7.2; rustc tidy pal.rs.
    - 강도: 실무 관례, 중.
    - 반론과 한계: rust-analyzer 자신도 의존 방향을 기계로 검사하지 않는다(tidy.rs 에 그런 검사 없음, e4). "good boundaries have measure zero"(Kladov 2021a): 좋은 경계는 코드를 훑어서는 찾기 어렵다. 책임 문장의 내용을 판정하는 도구는 없다(`missing_docs` 류는 문서가 있는지만 본다). `pal.rs` 도 예외 목록을 두고 "Not sure yet how to deal with this in the long term"이라 적는다.

15. **경계가 단단해야 하거나 독립 빌드, 독립 버전, 독립 소비가 필요하면 크레이트로 올린다.**
    - 근거: 실무에서 강제되는 경계는 크레이트다(Kladov 2021b; rust-analyzer 는 2021년 `crates/` 아래 32개). 크레이트는 컴파일러가 보장하는 비순환, 별도 컴파일, 크레이트별 SemVer 와 API 도구를 준다(e4 추론). 크레이트 경계는 독립 소비(serde_core)나 안정성 약속(tokio-stream)이 필요한 자리에 생긴다. Book 14.3 도 커지면 여러 라이브러리 크레이트로 나누라 한다.
    - 출처: Kladov 2021b; Kladov 2021c; Book 14.3; Cargo Book: Resolver; serde v1.0.220; Tokio 2020.
    - 강도: 실무 관례, 중.
    - 반론과 한계: rustc 는 분할로 "related functionality gets scattered"라 하고 더 적고 응집된 크레이트를 이상으로 꼽는다. Tokio 0.2 는 하위 크레이트를 다시 합쳤고, rust-analyzer 는 "Don't use small 'helper' crates"라 한다. 의존마다 비용이 든다(Drysdale Item 25). 작은 크레이트는 의존 지옥과 최적화 손실을 낳는다(Rust Design Patterns). Kladov 는 분할이 그래프가 '넓을' 때만 이득이라 본다.

16. **공개 표면 항목의 이동, 이름 변경, 삭제는 깨는 변경으로 다룬다.**
    - 근거: Cargo SemVer 의 major 분류와 `pub use` 완화책. Rust 2024 의 RPIT 는 모든 수명 매개변수를 잡으므로 이것도 "a SemVer commitment". 고유 항목 추가는 possibly-breaking.
    - 출처: Cargo Book: SemVer; Edition Guide 2024(RPIT).
    - 강도: 공식 권고(패키지 단위), 모듈 표면에 적용하면 약.
    - 반론과 한계: SemVer 지위는 패키지에만 있다. 한 크레이트 안에서는 모든 호출자를 함께 고칠 수 있다(Kladov 2021d).

17. **조립(연결)은 진입점에서 명시적으로 한다.**
    - 근거: Bevy 는 기능을 모두 플러그인으로 만들지만 연결은 `App::new().add_plugins(DefaultPlugins)` 로 명시한다. Kladov(2021c): "a leaf crate to tie everything together", "keep serialization at the boundary of the system, in the leaf crates".
    - 출처: Bevy; Kladov 2021c.
    - 강도: 실무 관례, 약.
    - 반론과 한계: 링크 섹션 자기 등록(inventory, linkme 류)을 막을 Rust 수단은 크레이트 전체 단위(`disallowed_macros` 등)뿐이며 시험되지 않았다(e4).

## ln-structure 시사점

### 뒷받침

- **표면 파일과 표면 경유 import.** Book 7.4, 14.2 는 `pub use` 로 내부와 다른 구조를 드러내라고 하고, Reference 는 비공개 '도우미 모듈' 관용구를 든다. std 도 `std::iter::adapters` + `pub use` 를 쓴다. 바깥에서 깊은 경로로 들어오는 import 는 컴파일러가 막는다(E0603, e4). E0364 덕분에 생성된 `pub use` 는 `pub(crate)` 항목을 새게 할 수 없어 "`pub(crate)` 항목은 표면에 들어가지 않는다"는 규칙과 맞물린다. 공개 항목 이동이 major 이고 `pub use` 가 완화책이라는 Cargo SemVer 는 표면이 파일 이동으로부터 호출자를 지킨다는 근거가 된다.
  출처: Book 7.4; Book 14.2; Reference: Visibility; Drysdale 2024; 실험 R1; Cargo Book: SemVer.
- **`pub(crate)` 항목을 표면 밖에 두기.** C-HIDDEN("`pub(crate)` is another great tool for removing implementation details from the public API")과 `unreachable_pub` 문서.
  출처: API Guidelines C-HIDDEN; rustc 린트 문서.
- **숨은 타입 노출 검사(`lnt review`).** `private_interfaces`, `unnameable_types` 와 같은 생각을 크레이트 경계 대신 모듈 표면에 적용한 것이다. `unnameable_types` 의 처방 "reexport the type properly to make it nameable"은 "맨 위 층 모듈에서 꺼내 준다"는 처방과 같고, Drysdale Item 24 도 같은 논리다. 실험 R2 의 예제에서 `unnameable_types` 는 0건이었다.
  출처: RFC 2145; rustc 린트 문서; Drysdale 2024 Item 24; 실험 R2.
- **C6 의 선례.** RFC 155(2014)가 고유 impl 을 타입의 모듈에 두게 했고 목적이 "to enforce consistency in code layout"이었다. RFC 735 는 되돌리면서도 "ease of finding method definitions by looking at the module the type is defined in"을 잃는다고 인정했다. Go(패키지), GHC `-Worphans`(모듈), Swift SE-0364(사후 준수 경고와 `@retroactive`), rustc `non_local_definitions`(RFC 3373: 인간이 "may find themselves similarly baffled"), Clippy `multiple_inherent_impl` 의 module/file 범위가 같은 계열이다. C6 의 근거("메서드 호출에는 use 가 필요 없다")는 Reference 의 메서드 조회 규칙 그대로이고, 처방인 확장 트레이트는 RFC 445 의 `FooExt` 관례다. 일관성 규칙은 '구현이 하나'와 상류의 안전한 진화를, C6 는 '`use` 가 모든 의존을 드러냄'을 보장하므로 둘은 목적이 다르며 C6 가 더 엄격하다(모듈이 크레이트보다 작고 고유 impl 도 다룸; e3 추론).
  출처: RFC 155; RFC 735; Go spec; GHC; SE-0364; RFC 3373; Clippy 소스(inherent_impl.rs); Reference: Method-call expressions; RFC 445.
- **C6 의 부수 효과.** 비제네릭 impl 에 한해 C6 를 지키는 모듈은 일관성 규칙상 크레이트로 떼어 낼 수 있다(e3 추론).
- **순환 금지와 아래로만 의존.** Cargo 의 "strictly acyclic"을 한 단계 아래로 옮긴 것이다. 서로 의존하는 모듈은 크레이트로 쪼갤 수 없으므로(Anderson 2020b) 비순환 모듈은 크레이트 승격이 싸다. Kladov 2021c 의 '공통 어휘 크레이트, 독립 기능 여럿, 묶는 잎 크레이트' 모양은 '아래 층의 공유 타입, 같은 층의 독립 모듈 여럿, 얇은 맨 위 층'에 대응한다(e3 추론). rust-analyzer 의 부재 불변식은 방향 규칙으로 기계 검사할 수 있는 종류이고, Kladov 는 그런 불변식이 코드에서 "pretty hard to divine"하다고 한다. arch-lint 의 "upward deps are violations"도 같은 규칙이다.
  출처: Cargo Book: Resolver; Anderson 2020b; Kladov 2021c; Kladov 2021a; rust-analyzer architecture.md; arch-lint.
- **외부 크레이트를 층 계산에 넣기.** Kladov(2021c) "The most important property of a crate is which crates it doesn't (transitively) depend on", Drysdale Item 25 의 의존 비용, cargo-deny `wrappers`("특정 크레이트만 직접 의존") 같은 패키지 단위 규칙이 '외부 의존은 어디서 쓰는지가 드러나야 한다'는 방향을 뒷받침한다.
  출처: Kladov 2021c; Drysdale 2024 Item 25; cargo-deny.
- **계산된 층(의미 없는 번호).** "there are no perfect hierarchies", "tree structure tends to deteriorate over time, while flat structure doesn't need maintenance"(Kladov 2021b)는 설계된 트리보다 계산된 배치를 지지하고 'catch-all utils' 폴더를 피하게 한다. Clippy 가 `cognitive_complexity` 를 "The true Cognitive Complexity of a method is not something we can calculate using modern technology"라며 1.91 에 restriction 으로 내린 일은 의미를 주장하는 구조 지표의 위험을 보여 주며, 의미 없는 층 번호는 그 함정을 피한다(e4 추론).
  출처: Kladov 2021b; Clippy cognitive_complexity.rs; CHANGELOG.
- **한 줄 책임(무엇을 맡는지, 어떻게는 아님).** Book 7.2 "name why they're related". Kladov 2021a 의 코드맵("what does the thing that I am looking at do?", "Avoid going into details of how each module works", "unlikely to frequently change"). `lnt doc` 출력이 코드맵 노릇을 할 수 있다(e2). '무엇의 불변식을 소유한다'는 책임은 Rust 공개 범위가 강제하는 단위다(Nomicon; Jung 2016; Palmieri 2020).
- **이름을 하나씩 적는 표면.** RFC 1560 "manually expandable", Cargo SemVer 의 glob 위험, 1.94·1.98 강화, Kladov 2021d("useful for tooling"), Drysdale Item 23, Tokio 의 prelude 제거. Tokio 쪽 근거(IDE 자동 import 가 좋아져 prelude 가 덜 필요)는 AI 에이전트에 더 강하게 적용된다(e2 추론).
- **연관 함수 규칙 중 수신자와 생성자 부분.** C-METHOD, C-CTOR, Book 12.3, Rust Design Patterns 의 생성자 관용.
- **`Box<dyn Trait>` 기본.** Kladov 2021c("do not put generic code at the boundaries", "prefer `&dyn Fn()`"), Anderson 2020a(단형화에 따른 팽창과 컴파일 시간), rustc 의 모듈별 volatile 코드 생성 단위.
- **진입점에서만 연결.** Bevy 의 명시적 `add_plugins`, Kladov 2021c 의 잎 크레이트와 '직렬화는 잎에'.
- **현재 Rust 설정의 근거(실험 R2).** 생성된 그대로 경고 0건. `allow-private-module-inception`(1.72, "Whether to allow module inception if it's not public")은 비공개 `order/order.rs` 꼴에 맞고, `allow-exact-repetitions`(1.89, 기본 true)는 `order::Order` 를 받아들이며, `[lints]` 는 1.74 부터 안정이다. 층 표면의 `#![allow(unused_imports)]` 는 rustc 가 내보낸(`is_exported`) import 만 검사에서 빼기 때문에 필요하다(지우면 6건).
  출처: 실험 R2; Clippy 소스(item_name_repetitions.rs); rustc 소스(check_unused.rs); Cargo Book: Manifest.
- **바로 켤 수 있는 린트.** 실험 R2 에서 `self_named_module_files`, `inline_modules` 는 0건이었다(그 밖에 `module_name_repetitions`, `multiple_inherent_impl`, `wildcard_imports`, `absolute_paths` 도 0건). cargo-pup 의 예시 규칙 "All `mod.rs` files must be empty of anything other than sub-module definitions and use statements"는 생성된 표면과 같은 모양이다(cargo-pup 은 이를 "not at all _prescriptive guidance_"라 적는다).
  출처: 실험 R2; cargo-pup.
- **오류 타입.** 모듈별 오류가 하위 오류를 `source` 로 감싸면 의존이 아래로 향하고, `From<Lower>` impl 은 상위 오류 타입의 모듈에 놓이므로 C6 에 맞는다(e3 추론). 아래 층의 크레이트 전체 enum 은 Jewson 의 "non-modular" 비판이 구체화된 형태다.
  출처: Jewson 2023; e3.
- **unsafe.** 작은 하위 층 모듈이 unsafe 불변식을 소유하는 구조와 맞는다(Nomicon; Rust Design Patterns).

### 도전하거나 어긋나는 것

- **RFC 735 의 번복.** Rust 는 C6 와 같은 모듈 단위 규칙(RFC 155)을 1년이 안 되어 버렸다. 이유는 "non-DRY single use extension traits, the worst offender being `AstBuilder` in libsyntax"와, 원래 동기가 'fake modules'라는 사라진 구현 세부였다는 점이다. C6 의 처방인 확장 트레이트는 import 를 늘리고, RFC 445 가 정한 관례적 해법(glob 으로 가져오는 prelude)은 이름을 하나씩 적는 표면, 표면 경유 import 와 부딪힌다. RFC 445 는 확장 트레이트를 "sparingly" 쓰라 하고, 1.0 에서 `IteratorExt` 같은 다수가 본 트레이트로 합쳐졌다. C6 를 지키려면 '늘어난 import 는 비용이 아니라 드러난 의존 간선'이라는 ln 자신의 목표로 정당화해야 한다.
  출처: RFC 735; RFC 155; RFC 445; RELEASES.md(1.0.0).
- **C6 의 제네릭 impl 미정의.** `impl Display for Wrapper<Local>` 에서 'T 를 정의한 모듈'이 `Wrapper` 의 모듈인지 `Local` 의 모듈인지 정해지지 않았다. 한 크레이트 안에서는 합법이지만, 모듈을 크레이트로 떼어 내면 `Wrapper` 가 fundamental 이 아닌 한 고아 impl 이 된다. RFC 2451(1.41)이 `impl<T> ForeignTrait<LocalType> for ForeignType<T>` 를 허용하도록 고아 규칙을 풀었다는 점도 '어느 모듈'의 판정을 복잡하게 한다.
  출처: e3 추론; Reference: Implementations; RFC 2451.
- **모듈 순환.** rustc 는 모듈 순환을 의도적으로 허용하고(RFC 1560 의 순서 무관 해석, 실험 R1 에서 진단 없음), Cargo 만 크레이트 순환을 막는다. Kladov(2021d)는 '크레이트는 DAG, 모듈은 상호 의존 가능'을 장점으로 꼽고, cargo-modules 자신의 소스에도 모듈 순환이 있다. ln-structure 의 모듈 비순환은 생태계 관례보다 엄격하며, 근거는 Rust 가 아니라 추적성과 크레이트 승격 가능성 같은 ln 의 목표에서 와야 한다.
  출처: RFC 1560; 실험 R1; Kladov 2021d; cargo-modules.
- **`pub(in path)` 는 조상만 가리킨다.** 공개 범위는 트리이고 층은 순서다. 형제끼리 `pub(crate)` 가 다 보이므로 "아래 층만 쓴다"는 rustc 로 표현할 수 없고, 모든 층 보장은 ff-lntools 에 기댄다. 모듈 단위 공개 범위에는 Rust 의 안정성 장치(`non_exhaustive`, 일관성, SemVer, 봉인)가 하나도 붙지 않는다(모두 크레이트 단위).
  출처: Reference: Visibility; Reference: Type system attributes; e1, e4 추론.
- **`unreachable_pub` 대 `redundant_pub_crate`(실험 R2 로 측정).** 생성 코드에서 `-W unreachable_pub` 은 31건, nursery `redundant_pub_crate` 는 9건("pub(crate) module inside private module")이었다. 비공개 모듈 안에서 크레이트 전체가 쓰는 항목은 `pub` 이면 앞의 것에, `pub(crate)` 면 뒤의 것에 걸려 둘을 함께 만족할 수 없다. rustc 가 `unreachable_pub` 를 "eventually" 기본 경고로 바꾸면 생성 코드가 31건을 경고한다. `redundant_pub_crate` 의 설명("not crate visible because they are inside a private module")은 크레이트 루트의 비공개 모듈에는 틀린데도 그 자리에서 발동했다. 같은 실험에서 `pub_use`(restriction)는 표면 다시 내보내기 자체에 반대해 20건, `mod_module_files` 는 15건(이 린트를 켠 호스트 프로젝트와 충돌), `missing_docs_in_private_items` 는 모든 `mod` 선언을 포함해 46건이었다. RFC 2126 은 애초에 비공개 모듈 안의 `pub` 패턴을 문제로 지적했었다.
  출처: 실험 R2; rustc 린트 문서; Clippy 소스(redundant_pub_crate.rs, pub_use.rs, module_style.rs); RFC 2126.
- **`mod.rs` 대 `name.rs`.** 공식 문서는 `name.rs` 를 권한다(Reference 의 "It is encouraged to use the new naming convention", Book 7.5 의 "older style", Edition Guide 2018 의 "a bunch of tabs named `mod.rs`"). ln-structure 가 모듈 폴더 안에 두는 `mod.rs` 표면은 RFC 2126 이 인정한 정당한 방식("a consistent story with `lib.rs`", 폐기 없음)이지만 공식 권장과 다르고, `mod_module_files` 를 켠 호스트와 충돌한다. Kladov(2021d)는 "lib.rs and main.rs still behave like mod.rs"라며 `_name.rs` 같은 대안을 냈다.
  출처: Reference: Modules; Book 7.5; Edition Guide 2018; RFC 2126; Clippy 소스(module_style.rs); Kladov 2021d.
- **자유 함수를 연관 함수로 바꾸는 규칙.** C-METHOD 는 "clearly associated with a particular type"인 연산에 한정된다. Book 7.4 는 자유 함수를 부모 모듈 경로로 부르는 것을 관용이라 하고, std 와 C-NEWTYPE-HIDE 의 예도 자유 함수다. rust-analyzer 는 "Avoid creating 'doer' objects"라며 `ThingDoer::do(arg1, arg2)` 를 "middle ground"로만 허용하고, 이 규칙이 바깥 API 에만 적용된다고 한다(안쪽의 비공개 문맥 구조체는 괜찮음). 이름 공간용 타입을 옹호하는 자료는 찾지 못했다. 그러므로 '타입만 공개' 규칙은 공식 권고를 넘어서며, 에이전트의 균일성 같은 ln 자신의 목표로 정당화해야 한다. 그 효과에 대한 증거는 어느 쪽으로도 없다.
  출처: API Guidelines C-METHOD, C-NEWTYPE-HIDE; Book 7.4; rust-analyzer style.md; e2.
- **비공개 필드 대 독립 빌림.** 비공개 필드를 가진 타입만 공개하면 바깥 호출자는 `&mut self` 메서드마다 값 전체를 빌린다(Matsakis 2018, 2021). 에이전트가 `RefCell` 이나 공개 필드로 도망갈 수 있는데, std 는 내부 가변성을 "something of a last resort"라 한다. 또 Rust 의 공개 범위 경계는 폴더가 아니라 파일 모듈이다. 파일 하나에 클래스 하나이고 `impl T` 를 T 의 모듈 폴더 안 다른 파일에 둔다면, 그 형제 파일에서는 T 의 비공개 필드가 보이지 않아 `pub(super)` 필드가 필요하고, 그만큼 unsafe 감사 범위가 넓어진다(Nomicon; e3). RFC 3458 도 공개 범위 우회가 분할 빌림과 부딪힌다고 적는다.
  출처: Matsakis 2018; Matsakis 2021; std::cell; Reference: Visibility; Nomicon: Working with Unsafe; RFC 3458; e3.
- **비동기 트레이트 대 `Box<dyn Trait>`.** 트레이트 안 `async fn` 은 dyn 호환이 아니고(1.75), `Send` 여부는 트레이트 작성자가 정해야 한다. 기본 주입 형태인 `Box<dyn Trait>` 는 박스된 future 를 돌려주게 설계하지 않으면 비동기 트레이트를 담지 못한다. dyn 호환성은 제네릭 메서드, `impl Trait` 반환, 연관 상수도 막아 주입 자리 트레이트의 모양을 제약한다. 2026-10 의 dyn async 지원은 [미확인]이고, API Guidelines 의 C-GENERIC, C-OBJECT 와의 관계는 노트가 깊이 보지 않았다.
  출처: Mandry 2023; Reference: Traits; API Guidelines(Checklist).
- **봉인 트레이트 대 숨은 타입 검사.** C-SEALED 는 바깥에서 이름 붙일 수 없는 `pub` 트레이트(`mod private { pub trait Sealed {} }`)를 필요로 하고, `unnameable_types` 는 이를 "trait `Sealed` is reachable but cannot be named"로 잡는다(실험 R1). RFC 2145 는 이런 패턴에 "legitimate uses"가 있다고 한다. 숨은 타입 검사는 의도된 예외를 표시할 방법이 필요하고, 생성된 표면은 `Sealed` 를 다시 내보내면 안 된다. 언어 차원의 대안(RFC 3323 `pub impl(crate) trait`)은 불안정이다. 타입 상태 패턴의 상태 트레이트도 같은 문제를 낳는다(Biffle 2019).
  출처: API Guidelines C-SEALED; Gruevski 2023; RFC 2145; 실험 R1; RFC 3323; Biffle 2019.
- **실무의 단단한 경계는 크레이트다.** Kladov(2021d)는 "CU doesn't have internal boundaries which can be reflected in visibilities"라 하고, 실무는 경계를 크레이트로 강제한다(rust-analyzer 는 2021년 `crates/` 아래 32개). 크레이트는 컴파일러가 보장하는 비순환, 별도 컴파일, 크레이트별 SemVer·API 도구를 주는데, ln-structure 는 이 중 비순환만 컴파일러 밖에서 다시 구현한다(e4). ln 은 아직 워크스페이스를 다루지 않는데, 1만 줄 이상에서 실무가 쓰는 주 도구가 워크스페이스다(e2). 빌드 이득에 대해서는 노트끼리 엇갈린다. e2 는 한 크레이트 안의 모듈 분할에 빌드 이득이 없다고 보지만, e3 은 rustc 가 모듈마다 코드 생성 단위를 나눠 증분 빌드가 모듈 경계의 영향을 받는다고 적는다(측정 자료는 없음).
  출처: Kladov 2021d; Kladov 2021b; rust-analyzer architecture.md; rustc partitioning.rs; e2; e3; e4.
- **과분할 위험.** 한 파일 한 타입, 한 모듈 한 책임을 지지하는 Rust 자료는 공식, 실무, 린트 어디에도 없다(e1, e2, e4). rustc 는 분할로 "related functionality gets scattered"라 하고, Tokio 는 다시 합쳤으며, 작은 구조체가 "not good abstractions"일 수 있고(Rust Design Patterns), 분해는 "definitely not always" 낫다(Matsakis 2018). 타입 상태는 상태마다 타입(곧 파일)을, 연산별 오류 타입은 타입 수를 늘린다.
  출처: rustc-dev-guide; Tokio 2019; Rust Design Patterns; Matsakis 2018; Biffle 2019; Jewson 2023.
- **의미 있는 층 대 계산된 층.** 실무 문서는 역할에 이름을 붙인다(rust-analyzer 의 "API Boundaries", hir-* 크레이트는 "not, and will never be, an api boundary", `ide` 는 공개 필드를 가진 POD 타입으로 된 API). 계산된 층 번호는 역할을 담지 않으므로 의도는 책임 문장에만 남는다.
  출처: rust-analyzer architecture.md; e2.
- **구조 규칙은 취향으로 취급된다.** Clippy 는 배치·구조 규칙을 restriction 에 두고("may lint against perfectly reasonable code") 근거로 일관성만 든다. 한 배치가 다른 배치보다 낫다는 증거는 없다.
  출처: Clippy README; Clippy 소스(module_style.rs).
- **의존성 역전 예외.** Bevy 는 렌더러 같은 내부 기능과 게임 자체까지 모든 것을 플러그인으로 만든다. ln 의 1:N 예외와 맞지만, 프레임워크에서는 역전이 주 구조가 될 수 있음을 보여 준다.
  출처: Bevy.
- **`impl Trait` 반환.** Rust 2024 에서 RPIT 는 모든 수명 매개변수를 잡아 SemVer 약속이 된다. C-NEWTYPE-HIDE 는 공개 API 에 뉴타입을 권하지만 그 `impl Trait` 서술은 1.26 시절이라 낡았다. `unnameable_types` 는 `impl Trait`, `dyn` 으로 새는 트레이트도 본다. 숨은 타입 검사가 `impl Trait` 반환을 어떻게 다룰지 정해야 한다.
  출처: Cargo Book: SemVer; Edition Guide 2024(RPIT); API Guidelines C-NEWTYPE-HIDE; rustc 린트 문서.
- **다시 내보내기 비판.** rust-analyzer 는 라이브러리가 아닌 코드에서 다시 내보내기가 "two ways to use something"을 만든다고 피한다. ln 은 정의 경로 import 를 막아(바깥에서는 E0603) 두 길 중 하나만 남긴다는 점에서 이 비판을 줄인다(e2, e4).
  출처: rust-analyzer style.md; Reference: Visibility.

### 열린 질문

1. 표면을 `x/mod.rs` 에서 공식 권장인 `x.rs` + `x/` 로 옮길 것인가. 그러면 표면 파일이 모듈 폴더 밖에 놓인다. 어느 쪽이든 `[lints]` 에 `self_named_module_files`(지금 0건) 또는 `mod_module_files` 를 켜서 고정할 것인가.
   출처: Reference: Modules; RFC 2126; 실험 R2.
2. 생성 코드의 공개 표기: `lib.rs` 에서 닿는 맨 위 층 표면만 `pub` 이고 나머지는 `pub(crate)` 인가, 지금처럼 `pub` 인가. `unreachable_pub` 와 `redundant_pub_crate` 중 어느 쪽을 allow 할 것이며, `private_interfaces` 와는 어떻게 맞물리는가.
   출처: rustc 린트 문서; 실험 R2; Kladov 2021d; e4.
3. 생성되는 `[lints]` 에 무엇을 켤 것인가. 후보: `self_named_module_files`, `inline_modules`(둘 다 0건), `multiple_inherent_impl`(블록 수만 세므로 C6 를 대신하지 못함), `missing_docs_in_private_items` 와 설정 `missing-docs-in-crate-items`(46건; 책임 문장의 존재는 강제하지만 내용은 못 봄), `unnameable_types`, 자기 등록 크레이트를 막는 `disallowed_macros`(시험 안 됨).
   출처: 실험 R2; Clippy 소스; e4.
4. C6 의 제네릭 impl 에서 '정의한 모듈'을 "이 모듈이 크레이트라면 고아 규칙을 만족하는가"로 정할 것인가(e3 제안). RFC 2451 이후의 고아 규칙을 그대로 옮길 것인가.
   출처: e3; Reference: Implementations; RFC 2451.
5. C6 를 모듈 폴더 안의 파일 단위로도 적용할 것인가(Clippy `multiple_inherent_impl` 의 `file` 범위에 해당).
   출처: Clippy 소스(inherent_impl.rs).
6. 분할 빌림과 형제 파일 impl 을 위해 모듈 폴더 안에서 `pub(super)` 필드를 허용할 것인가. 그때 unsafe 감사 범위를 어떻게 작게 유지하는가. 공개 타입에 내부 가변성이 나오면 알릴 것인가. 에이전트가 모듈 경계를 넘는 빌림 충돌에서 `Rc<RefCell<_>>` 로 물러서는지도 확인할 가치가 있다(e3).
   출처: Matsakis 2021; Nomicon; RFC 3458; std::cell; e3.
7. 의도된 Voldemort 항목(봉인 트레이트, 타입 상태의 상태 트레이트)을 어떻게 선언하게 할 것인가. RFC 3323 이 안정화되면 `impl(crate)` 로 바꿀 것인가. 중첩 모듈에서 아래 층 타입을 `pub type` 별칭으로 꺼내는 방식을 `unnameable_types` 가 '이름 붙일 수 있음'으로 보는지는 노트에서 시험하지 않았다.
   출처: RFC 2145; API Guidelines C-SEALED; RFC 3323; rustc 린트 문서.
8. 비동기 주입 자리의 표준 모양: 박스된 future 를 돌려주는 `Box<dyn Trait + Send + Sync>` 인가, 제네릭인가. `Send` 여부를 모듈 책임 문장에 적어야 하는가.
   출처: Mandry 2023; Reference: Traits.
9. 크레이트 SemVer 범주(이동·이름 변경·삭제는 깨짐, 고유 항목 추가는 깨질 수 있음)를 모듈 표면에 적용할 것인가. 에이전트가 코드를 자주 다시 만든다는 점에서 의미가 있는가.
   출처: Cargo Book: SemVer; e1.
10. 표면 시그니처에 `impl Trait` 를 허용할 것인가(2024 의 포획 규칙, C-NEWTYPE-HIDE).
    출처: Edition Guide 2024(RPIT); API Guidelines C-NEWTYPE-HIDE.
11. 워크스페이스: 층을 크레이트에 대응시킬 것인가. Kladov(2021b)의 방식은 평평한 `crates/`, 내부 크레이트 `version = "0.0.0"`, 게시용 크레이트를 `libs/` 로 나눠 "things in libs/ don't use things from crates/"를 검사하기 쉽게 하는 것이다. 언제 층이나 중첩 모듈을 크레이트로 올려야 하는가. 외부 크레이트 타입이 맨 위 층 시그니처에 나오면 그 크레이트를 다시 내보낼 것인가(Drysdale Item 24), cargo-check-external-types 같은 허용 목록이 필요한가.
    출처: Kladov 2021b; Drysdale 2024 Item 24; cargo-check-external-types.
12. tree-sitter 로 읽은 구문 간선을 이름 해석 그래프(cargo-modules `--acyclic`)와 대조해 검증할 것인가. 매크로, glob, `#[path]` 가 만드는 간선이 문제다(crawk 도 같은 한계를 밝힌다: "it does not compile or expand macros").
    출처: cargo-modules; crawk; e4.
13. `lnt doc` 이 Kladov 식 코드맵을 내고, 사람이 'API 경계' 모듈과 부재 불변식을 선언하게 할 것인가.
    출처: Kladov 2021a; rust-analyzer architecture.md; e2.
14. 오류 타입의 단위: 한 파일 한 클래스 아래에서 모듈당 하나인가, 연산당 하나인가.
    출처: Jewson 2023; Palmieri 2021; e3.
15. 연관 함수 규칙을 완화해 표면이 아닌 파일에서는 자유 함수를 허용할 것인가. 균일성이 에이전트에 도움이 된다는 증거는 어느 쪽으로도 없다(e2).
16. C5(Rust 경로 규칙)를 정할 재료: Book 7.4 의 관용(함수는 부모 모듈 경로로, 구조체와 enum 은 전체 경로로, "just the convention that has emerged"), rust-analyzer 의 "Qualify items from `hir` and `ast`"(이유: "makes the layer clear at a glance")와 "Grouping by crate allows spotting unwanted dependencies easier", Clippy `absolute_paths`(restriction, `absolute-paths-max-segments` 기본 2, 실험 R2 에서 0건), 스타일 가이드의 "Tools must not merge or un-merge imports by default", Kladov(2021d)의 "Imports should only introduce the name into module's namespace, and should be separate from intentional re-exports".
    출처: Book 7.4; rust-analyzer style.md; Clippy absolute_paths.rs; Style Guide; Kladov 2021d.
17. 모듈이 크레이트가 된다면 층 수가 빌드 임계 경로를 예측하는가. 검증되지 않은 가설이다(e3).
18. 근거의 수준: 이 장의 근거는 대부분 컴파일러 동작, 공식 문서, 전문가 의견, 프로젝트 경험이다. Tokio 의 노트북 한 대 측정 말고는 정량 자료가 없고, 층 규칙이나 이 린트들이 결함률이나 AI 에이전트의 결과에 주는 영향을 다룬 연구는 찾지 못했다(e2, e3, e4).

## 이 파일에만 나오는 출처

- Book 14.2: "Publishing a Crate to Crates.io". https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html
- API Guidelines C-NEWTYPE-HIDE(Future proofing): https://rust-lang.github.io/api-guidelines/future-proofing.html ; Checklist(C-GENERIC, C-OBJECT): https://rust-lang.github.io/api-guidelines/checklist.html
- Drysdale, D. (2024). *Effective Rust*. Item 23 "Avoid wildcard imports" https://effective-rust.com/wildcard.html ; Item 24 "Re-export dependencies whose types appear in your API" https://effective-rust.com/re-export.html ; Item 25 "Manage your dependency graph" https://effective-rust.com/dep-graph.html
- Edition Guide 2024: RPIT 수명 포획 https://doc.rust-lang.org/edition-guide/rust-2024/rpit-lifetime-capture.html ; `unsafe_op_in_unsafe_fn` https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-op-in-unsafe-fn.html
- Style Guide: "Items". https://doc.rust-lang.org/style-guide/items.html
- RFC 2451 (Griffin 2018), "Re-rebalancing coherence"(1.41 안정화). https://rust-lang.github.io/rfcs/2451-re-rebalancing-coherence.html
- Rust Design Patterns, "Constructors" 관용. https://rust-unofficial.github.io/patterns/idioms/ctor.html
- Clippy 소스: `partial_pub_fields.rs` https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/partial_pub_fields.rs ; `absolute_paths.rs` https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/absolute_paths.rs ; `cognitive_complexity.rs` https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/cognitive_complexity.rs ; `wildcard_imports.rs` https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/wildcard_imports.rs ; `missing_doc.rs` https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/missing_doc.rs ; 설정 키 `clippy_config/src/conf.rs` https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_config/src/conf.rs
- cargo-deny, `[bans]` 설정 문서(v0.20.2). https://github.com/EmbarkStudios/cargo-deny/blob/HEAD/docs/src/checks/bans/cfg.md
- Endler, M. (2026). "Tips For Faster Rust Compile Times." corrode.dev, 2024-01-12 게시, 2026-03-14 갱신. https://corrode.dev/blog/tips-for-faster-rust-compile-times/
- Gallant, A. (2015; 2018, 2020 갱신). "Error Handling in Rust." https://burntsushi.net/rust-error-handling/
- King, A. (2019). "Parse, don't validate." 2019-11-05. https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
- Biffle, C. L. (2019). "The Typestate Pattern in Rust." cliffle.com, 2019-06-05. https://cliffle.com/blog/rust-typestate/
- std 자유 함수 예: `std::mem::swap` https://doc.rust-lang.org/std/mem/fn.swap.html ; `std::thread::spawn` https://doc.rust-lang.org/std/thread/fn.spawn.html
