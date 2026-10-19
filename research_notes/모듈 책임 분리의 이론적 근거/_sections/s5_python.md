## 7. Python 에서 따로 요구되거나 권장되는 것

Python 의 공식 문서는 모듈에 무엇을 넣고 책임을 어떻게 나눌지에 대해 거의 말하지 않는다. 대신 무엇이 공개인지, import 가 실행 시점에 어떻게 동작하는지, 타입 전용 의존과 인터페이스를 어떻게 적는지를 정한다. 모듈 경계 자체는 실무 지침, 경계 강제 도구, 몇몇 대규모 조직의 경험이 채우며, 일부 Python 관용은 클래스 중심 규칙과 정면으로 부딪친다. 근거는 공식 문서, 도구 문서, 전문가 의견, 단일 조직의 경험 보고이고 통제된 실증 연구는 없다.

### 7.1 공식 문서가 정한 것: 공개와 내부 인터페이스, import, 패키지

**공개는 문서화된 약속이다.** PEP 8(Process, Active)은 표준 라이브러리용 규약이며, 충돌하면 "project-specific guides take precedence"(프로젝트 지침이 우선한다)고 스스로 범위를 좁힌다. 공개 인터페이스(public interface)는 문서화와 하위 호환 약속으로 정한다: "All undocumented interfaces should be assumed to be internal"(문서화되지 않은 것은 모두 내부로 본다). `__all__` 로 공개 이름을 선언하고도 내부 이름에는 밑줄을 붙이며, 감싸는 패키지·모듈·클래스가 내부면 그 안도 내부다. import 한 이름은 구현 세부이고, 예외는 "a package's `__init__` module that exposes functionality from submodules"(하위 모듈 기능을 드러내는 패키지 `__init__`)처럼 문서화된 경우다(PEP 8). PEP 8 이 이름을 들어 인정하는 구조적 공개 통로는 이것 하나다.

**import 는 맨 위에, 기본은 절대 경로.** import 는 파일 맨 위에 두고(PEP 8), 함수 안 import 는 순환 회피나 초기화 시간 단축이 필요할 때로 한정한다(Python FAQ). 절대 import(absolute import)가 "recommended"(권장)이고 명시적 상대 import(explicit relative import)는 "an acceptable alternative ... especially when dealing with complex package layouts"(복잡한 패키지 구조에서 특히 받아들일 만한 대안)다(PEP 8). PEP 328(Final)은 상대 import 의 핵심 용도를 "rearrange the structure of large packages without having to edit sub-packages"(하위 패키지를 고치지 않고 큰 패키지 구조를 바꾸기)로 들었다. 주 모듈(main module)은 절대 import 만 쓸 수 있다(Python Tutorial). Google 지침은 "Do not use relative names in imports"(import 에 상대 이름을 쓰지 말라)로 금지하며 패키지를 두 번 import 하는 일을 막는다는 이유를 들지만, 그 원리는 설명하지 않는다(Google pyguide).

**타입 검사기가 보는 공개 집합.** typing spec(Typing Council 관리)에서 `py.typed` 패키지의 밑줄 없는 모듈 파일은 모두 "the supported interface"(지원되는 인터페이스)이고, "Imported symbols are considered private by default"(import 한 이름은 기본 비공개)다. 재노출(re-export)은 `import X as X`, `from Y import X as X`, `from Y import *` 와 `__all__` 로만 되며, `__all__` 은 리터럴 목록이나 `+=` 같은 정해진 관용으로 써야 검사기가 정적으로 계산한다(typing spec). pyright(1.1.414) 문서는 `from . import A` 도 재노출로 보고, `__init__.py` 의 `from .A import X` 는 하위 모듈 이름 `A` 를 공개로, `X` 는 비공개로 둔다(pyright docs). 예전 spec 에도 이 형태가 있었는지는 [미확인]이다. mypy 는 `--no-implicit-reexport`(`--strict` 에 포함)를 켜야 이 규칙을 따른다(mypy docs). 두 문서 모두 밖으로 보이는 것만 정하고 내부 모듈 사이의 import 방향은 정하지 않는다.

**별칭, 세분도, 배치.** `typing.TypeAlias` 는 3.12 부터 deprecated 이며 "Removal ... is not currently planned, but users are encouraged to migrate to `type` statements"(제거 계획은 없지만 `type` 문으로 옮기길 권한다)(typing docs). 그런데 `type X = C` 가 만드는 `TypeAliasType` 은 런타임에 클래스가 아니어서 클래스 재노출을 대신하지 못한다. 모듈 크기, 모듈당 클래스 수, 책임별 분할을 정한 공식 규칙은 없고, 튜토리얼이 드는 모듈의 이유는 유지보수, 재사용, 이름공간(namespace) 격리다(Python Tutorial). 노트 사이에 차이가 있다. 한 노트의 전문 검색에서 "one class per" 는 0 건이었지만, 다른 노트가 찾은 Programming FAQ 문장은 모듈마다 "one class (or tightly related class hierarchy)"(클래스 하나 또는 밀접한 계층 하나)를 두는 구조를 전제한다. 권고는 아니다(Python FAQ). "Flat is better than nested"(평평함이 중첩보다 낫다)는 짧은 import 경로라는 뜻으로 쓰인다(PEP 20; Peters 2015). src 레이아웃은 PyPA 가 의무 아닌 논의 문서로 이점과 비용(실행에 설치 필요)을 함께 적고(PyPA src layout), Hitchhiker's Guide 의 2013 년 조언은 반대한다(HHGP).

### 7.2 순환 import, 타입 전용 의존, 지연 로드

**실행 시점의 사실.** 일반 패키지를 import 하면 `__init__.py` 가 "implicitly executed"(암묵적으로 실행)되므로, 하위 모듈 하나를 불러도 감싸는 모든 `__init__.py` 가 먼저 돈다(Python Reference; HHGP). 모듈은 본문 실행 전에 `sys.modules` 에 들어가므로 순환 import(circular import)는 부분 초기화된 모듈(partially initialized module)을 본다(Python Reference). FAQ 의 경험칙으로는 두 모듈이 모듈째 import 하면 "Circular imports are fine"(순환도 괜찮고), 최상위에서 상대 모듈의 이름을 꺼내면 실패한다. FAQ 는 from-import 회피, import 순서 조정, 구조 변경을 "not mutually exclusive"(서로 배타적이지 않은) 처방으로 나란히 둔다(Python FAQ). 공식 문서는 순환을 금지하지 않고 런타임 위험으로 다룬다. PEP 810 은 "The best practice is still to avoid circular imports in your code design"(설계에서 순환을 피하는 것이 여전히 모범이다)이라 하면서도, 지연 import 가 견디게 하는 순환을 "an intentional and desirable thing (especially for typing-related imports)"(특히 타입 관련 import 에서는 의도적이고 바람직한 것)이라 부른다. 한 문서 안의 긴장이다.

**타입 전용 의존.** PEP 484(Final, 3.5)는 Django 처럼 "each model is in a separate file"(모델마다 파일 하나)인 구조에서 순환 때문에 모델을 직접 import 하지 못하는 경우가 많다고 기록하고, `if TYPE_CHECKING:` 가드가 "may also be useful to handle import cycles"(순환 처리에도 쓸모 있다)고 쓴다. 가드 안 import 는 검사기만 보고 런타임은 건너뛰는 타입 전용 의존(type-only dependency)이 된다(typing spec). 주석은 3.14 부터 지연 평가된다(PEP 649/749, Final). PEP 563 은 Superseded 이고, `from __future__ import annotations` 는 PEP 649 이전 마지막 판(3.13 예상)의 지원 종료 뒤 deprecated, 다시 최소 두 판 뒤 제거될 예정이다(PEP 749). 그래서 3.10–3.13 을 지원하는 코드는 가드 안 이름을 주석에 쓸 때 따옴표나 이 import 가 여전히 필요하다. `TYPE_CHECKING` 을 내장 상수로 만드는 PEP 781 은 Draft 로 남았다. 타입 전용 의존을 구조상 의존으로 셀지는 어떤 공식 문서도 정하지 않았다.

**지연 로드는 명시적이고 국소적으로.** 모듈 `__getattr__`(PEP 562, Final, 3.7)은 "lazy submodule imports"(하위 모듈 지연 import)를 주요 용도로 든다. 전역·암묵 지연 import(PEP 690)는 2022-12-02 운영위원회(Steering Council, SC)가 "a split in the community over how imports work"(import 동작을 두고 공동체가 갈라짐)와 첫 사용 시점에 어디서나 터질 수 있는 import 예외를 이유로 거부했다(SC 2022). 명시적 `lazy` 키워드(PEP 810)는 2025-11-03 만장일치로 수락되어 2026-10-09 출시된 3.15 에 들어갔다(SC 2025; PEP 790). 원칙은 "local, explicit, controlled, and granular"(국소적, 명시적, 통제된, 세밀한)이다. 모듈 범위에서만 쓰고 상대 `lazy from .m import X` 도 되며, 검사기는 이를 일반 import 처럼 해석해도 된다(Python Reference; PEP 810). 3.15 이전 판은 `__lazy_modules__` 선언을 무시하고 즉시 import 한다. 응용은 `-X lazy_imports=all` 로 모든 import 를 지연시킬 수도 있다(What's New 3.15). PEP 810 은 함수 안 import 가 "obfuscates the full set of dependencies for a module"(모듈의 의존 전체를 가린다)고 비판하고, 지연이 순환을 자동으로 풀지는 않는다고 적는다. 등록에 대해서는 "registries of objects should be constructed via explicit discovery processes (e.g. a well-known function to call)"(레지스트리는 잘 알려진 함수 호출 같은 명시적 발견 과정으로 만들어야 한다)고 권하고, 하위 모듈은 부모 속성에 기대지 말고 명시적으로 import 하라고 한다(PEP 810). 근거는 SC 결정과 설계 논증이며, 시작 시간 50–70%·메모리 30–40% 절감이라는 수치는 설정과 표본이 보고되지 않아 약하다.

### 7.3 인터페이스: ABC, Protocol, 명시 상속, override

공식 문서는 명목적 부분 타입(nominal subtyping)과 구조적 부분 타입(structural subtyping)을 모두 두지만 고르는 기준은 주지 않는다. 추상 기반 클래스(abstract base class, ABC; PEP 3119, Final)는 상속이나 `register` 로 표시한다. Protocol(PEP 544, Final, 3.8)은 명시 표시를 강요하는 것이 "unpythonic"(파이썬답지 않다)하다며 도입되었지만 "complement normal classes"(일반 클래스를 보완한다)고 밝히고, 프로토콜은 "describe an interface, not an implementation"(구현이 아니라 인터페이스를 기술한다)하며 모듈 객체도 프로토콜을 만족할 수 있다고 한다(PEP 544). typing spec 은 명시 상속이 "not necessary"(필요 없다)지만, 하면 검사기가 "statically verify that the class actually implements the protocol correctly"(구현이 맞는지 정적으로 검증)한다고 쓰고, "We still slightly prefer nominal subtyping"(여전히 명목적 부분 타입을 조금 더 선호한다)이라 덧붙인다(typing spec). 라이브러리 지침은 상속되어야 하는 클래스는 `ABC` 에서 파생하라고 권한다(typing guide). `@override`(PEP 698, Final, 3.12; 3.10–3.11 은 `typing_extensions`)는 리팩터링이 재정의 관계를 깨는 것을 잡는다. 모든 재정의에 요구하는 엄격 모드는 "Strict enforcement should be opt-in"(선택 사항이어야 한다)이고 런타임 검사는 없다(typing spec; PEP 698). 명시 상속한 프로토콜은 조상 클래스라 그 구현에 `@override` 를 붙일 수 있지만, 구조적으로만 맞춘 구현에는 붙일 곳이 없다.

실무는 구조적 쪽으로 기운다. Percival & Gregory 는 ABC 가 "unmaintained and, at worst, misleading"(관리되지 않고 최악에는 오해를 부르는) 상태가 되어 지운 적이 있으며 "In practice we often just rely on Python's duck typing"(실제로는 대개 덕 타이핑에 기댄다)고 쓴다(Percival & Gregory 2020). Schlawack 는 "the smaller an interface, the better"(인터페이스는 작을수록 좋다)며 Protocol 이 정의를 소비자 곁에 두게 한다고 본다(Schlawack 2021). spec 의 약한 명목 선호와 실무의 구조 선호가 맞서지만 양쪽 다 의견이고 측정은 없다. 정적 검사기가 `ABC.register()` 를 따르는지는 확인되지 않았다.

### 7.4 실무 지침: 층과 의존성 역전, 입출력 분리, 전역 상태와 등록, 로깅

**층과 의존성 역전은 값을 치르고 쓴다.** Percival & Gregory 는 진흙공(Big Ball of Mud)의 특징을 "homogeneity: every part of the system looks the same, because we haven't been clear about the responsibilities of each component"(책임을 분명히 하지 않아 모든 부분이 똑같아 보이는 균질성)로 진단하고 층과 의존성 역전(dependency inversion)을 처방하되, "Depends on doesn't mean imports or calls, necessarily"(의존이 꼭 import 나 호출을 뜻하지는 않는다)고 단서를 단다. 도메인은 상태 있는 의존을 갖지 않으며 "your ORM should import your model, and not the other way around"(ORM 이 모델을 import 해야지 반대가 아니다). 비용도 적는다. 층 하나는 "does add complexity locally"(국소적으로 복잡도를 더한다), 단순 CRUD 앱에는 필요 없다, 의존성 주입(dependency injection, DI)은 "regarded with suspicion in the Python world"(파이썬 세계에서 의심받는다). 연결은 진입점이 부르는 조립 루트(composition root), 곧 bootstrap 스크립트에서 수동으로 하고 설정도 import 시점 상수 대신 함수로 읽는다. 공저자끼리도 과설계 여부로 다투었다(Percival & Gregory 2020). Seddon 도 연결을 `main` 에 두며 "Registries are a good choice if the dependency can be fixed at start up time"(의존이 시작 시점에 고정되면 레지스트리가 좋은 선택이다)이라 한다(Seddon 2019b).

**입출력은 위로 끌어올린다.** Rhodes 는 입출력을 최상위 접착 코드로 끌어올리고(hoisting I/O) 아래는 순수 함수로 두라고 한다: "To get rid of I/O, make it subordinate"(입출력을 없애려면 종속시켜라). 테스트의 `patch()` 는 강한 결합의 신호이며 "Python itself will place little pressure upon your code to be decoupled"(Python 자체는 분리 압력을 거의 주지 않는다)(Rhodes 2014; Rhodes 2015). Schlawack 의 "your business code is sacred"(업무 코드는 신성하다)도 같은 방향이다(Schlawack 2025). 모두 슬라이드와 저서의 전문가 의견이다.

**전역 상태, 등록, 로깅.** Rhodes 는 "mutable global objects can wind up coupling distant code"(가변 전역 객체가 먼 코드를 결합한다)며 핸들러·플러그인 레지스트리를 예로 들고, "Errors at import time are far more serious than errors at runtime"(import 시점 오류는 런타임 오류보다 훨씬 심각하다)고 본다(Rhodes 2018). Google 지침(2026-10 판)은 "Avoid mutable global state"(가변 전역 상태를 피하라)에 "Similar problems easily arise with global registries"(전역 레지스트리도 마찬가지다)를 덧붙이고 모듈 수준 상수는 권한다(Google pyguide). Flask 와 Django 는 import 로 등록하면서 순환 import 와 `ready()` 중복 호출 같은 함정을 스스로 문서화하고(Flask docs; Django docs), PyPA 는 플러그인을 entry point 메타데이터로 import 없이 선언하고 `.load()` 로 따로 부르는 방식을 든다(PyPA plugins). 라이브러리 로깅은 공식 권고가 분명하다. `__name__` 로거를 쓰고 "do not add any handlers other than NullHandler"(NullHandler 외의 핸들러를 달지 말라), 핸들러 설정은 "the prerogative of the application developer"(응용 개발자의 몫)다(Logging HOWTO).

### 7.5 경계 강제 도구와 대규모 경험

**도구가 필요한 이유.** Seddon 은 "Python has no formal way of declaring, and enforcing, a dependency flow"(Python 에는 의존 흐름을 선언하고 강제할 공식 수단이 없다)에서 출발했다(Seddon 2019a). 아래 도구 문서는 동작을 정의할 뿐 효과의 증거는 아니다.

**import-linter 와 tach.** import-linter(2.15, 2026-09-04)의 층 계약(contract)은 "higher layers may depend on lower layers, but not the other way around"(위층은 아래층에 의존해도 되나 반대는 안 된다)이고 간접 import 도 센다. 같은 층 형제는 `|` 로 묶으면 서로 import 할 수 없고 2.0(2024-01)부터는 `:` 로 묶어 허용할 수도 있으며, 층으로 지정한 패키지 안의 하위 모듈끼리는 제한하지 않는다. `acyclic_siblings`(2.6, 2025-11)는 층 순서 없이 형제 사이 순환을 세대마다 금지하고, 실패하면 패키지를 "locally acyclic"(국소적으로 비순환)하게 만들 의존을 탐욕 휴리스틱으로 제안한다. 예외 목록(`ignore_imports`)의 낡은 항목은 기본적으로 오류다(import-linter docs). tach(v0.35.3)는 모듈마다 `depends_on` 허용 목록과 `expose` 인터페이스를 두고 같은 층 의존은 선언하면 허용하며, 순환 금지는 기본 꺼짐이다. 2025 년 개발사가 손을 뗀 뒤 tach-org 가 관리한다(tach docs).

**일반 린터와 타입 검사기.** Ruff(0.17.1)에는 순환 규칙이 없고 상대 import 금지(TID252)와 함수 안 import 지적(PLC0415)이 있으며, pylint(4.1.3) R0401 은 한 번 실행에 든 모듈의 순환만 본다(Ruff; pylint). pyright 의 `reportImportCycles` 는 모든 프리셋에서 꺼져 있지만 문서는 순환이 "often hint at architectural layering issues"(층 구조 문제를 시사하는 일이 많다)고 쓴다(pyright docs). `TYPE_CHECKING` 안의 import 는 import-linter 가 기본으로 세고, tach 는 기본으로 무시하며, pylint 는 순환 검사에서 뺀다. Seddon 은 "Python packages are best kept acyclic"(패키지는 비순환이 최선)이라면서도 "I'd take a layered subpackage over merely an acyclic one any day"(단지 비순환인 것보다 층이 있는 하위 패키지를 택하겠다)고 쓴다(Seddon 2025).

**대규모 사례.** Kraken 은 27,637 개 모듈, 약 400 명 개발자의 단일 코드베이스를 `clients` > `territories` > `core` 층 계약과 독립 계약으로 유지한다. 규칙은 "A component is not allowed to depend on any components higher up the stack"(어떤 구성 요소도 더 위의 구성 요소에 의존할 수 없다)이다. 무시한 import 수를 부채 지표로 줄여 왔지만 몇 년 뒤에도 15 건이 남았다. 교훈은 "just talking about the layering was not enough"(층을 말로만 해서는 부족했다)와, 역전의 국소 복잡도는 감수할 만하나 모두가 의존하는 core 는 바꾸기 비싸져 위층에 코드가 쌓인다는 것이다(Seddon 2023). 계약 40 여 개를 PR 마다 돌린다는 내용은 [2차 출처]다. Dropbox 에서는 수백 개 모듈이 얽힌 "the infamous 'tangle'"(악명 높은 엉킴) 때문에 파일 하나만 바뀌어도 mypy 가 순환 전체를 다시 처리했고, 풀 자원이 없어 mypy 를 빠르게 만드는 쪽을 택했다(Lehtosalo 2019). 300 만 줄이 넘는 Metaserver 에서는 기능을 내려고 순환을 넣는 일이 있었고, 대부분을 끊는 데 몇 년이 걸렸지만 그것이 "probably the most strategically effective part of the project"(아마 프로젝트에서 전략적으로 가장 효과적인 부분)였다(Sanguansin & Shah 2021). Meta 의 Cinder strict modules 는 import 시점 부수효과를 막아 "you cannot use a decorator to create a registry of functions"(데코레이터로 함수 레지스트리를 만들 수 없다)고 정한다(Cinder Strict Modules, 현재 지위 [미확인]). Instagram 서버에 지연 import 를 적용하자 P50 재로드 시간이 약 70% 줄고 로드 모듈이 약 12 분의 1 이 되었지만, 암묵적 등록과 부모 속성으로 붙는 하위 모듈에 기댄 코드가 깨졌다(Cinder Lazy Imports; Méndez Bravo 2024). 이 수치는 PEP 690·810 의 수치와 저자가 겹쳐 독립된 재현이 아니고 방법도 공개되지 않았다. 세 조직 모두 순환을 중심 문제로 보았으나 수단은 정적 계약, 빌드 시스템 가시성, 런타임 의미론으로 달랐고 통제된 비교는 없다.

### 7.6 Python 관용과 클래스 중심 규칙의 충돌

**정적 메서드보다 모듈 함수.** 반대 쪽이 많고 성문화되어 있다. Programming FAQ 는 정적 메서드 효과를 내는 "a far more straightforward way"(훨씬 간단한 방법)가 모듈 수준 함수(module-level function)라 하고(Python FAQ), Google 지침은 "Never use `staticmethod` unless forced to ... Write a module-level function instead"(기존 라이브러리 API 때문이 아니면 쓰지 말고 모듈 수준 함수를 써라)로 금지한다(Google pyguide). 원조는 Eby 의 "The idiomatic translation of a Java static method is usually a module-level function"(자바 정적 메서드의 관용적 번역은 대개 모듈 수준 함수)이며 그는 상수도 모듈 수준으로 옮기라 했다(Eby 2004a). wemake 의 WPS602 와 Ramalho 도 같은 쪽이다(wemake; Ramalho 2022 [미확인]). Ronacher 는 에이전트용 조언에서 "Prefer functions ... over classes"(클래스보다 함수를 택하라)고 쓴다(Ronacher 2025). 옹호 쪽에서 Hettinger 는 정적 메서드가 함수의 "findability"(찾기 쉬움)와 올바른 맥락의 사용을 돕는다고 했고(Hettinger 2013 [미확인]), Danjou 는 하위 클래스에서 재정의할 수 있다는 점을 든다(Danjou 2013). Diederich 는 불필요한 클래스를 비판하면서도 상수와 "a small bag of functions"(작은 함수 묶음)를 담는 작은 이름공간으로서의 클래스는 괜찮다고 했다(Diederich 2012 [미확인]). `patch.object(Cls, "f")` 가 `Cls.f` 를 쓰는 모든 호출자에 닿는다는 점도 작은 근거다(unittest.mock docs). pylint 는 이를 가르는 `no-self-use` 검사를 "too opinionated"(지나치게 주관적)라며 선택으로 돌렸고(pylint), Guido 가 staticmethod 를 실수라 했다는 인용은 원문이 확인되지 않았다[미확인].

**파일당 클래스 하나.** Google 지침은 "Unlike Java, there is no need to limit yourself to one class per module"(자바와 달리 모듈당 클래스 하나로 제한할 필요가 없다)이라 하고(Google pyguide), Stack Overflow 채택 답변(2008)은 "a module is the unit of reuse"(모듈이 재사용 단위다)라 한다(SO 106896). Hitchhiker's Guide 는 구조 없이 흩어진 작은 조각을 라비올리 코드(ravioli code)라 부른다(HHGP). 같은 질문에는 크고 복잡한 클래스는 파일 하나씩 두라는 답도 있다. 규칙의 원래 근거는 자바 명세의 "makes it easy for a Java compiler to find a named class"(컴파일러가 이름으로 클래스를 쉽게 찾는다), 곧 도구가 이름에서 파일을 찾게 하려는 것이다(JLS SE21). Python 공동체는 이를 이식된 관습으로 읽고, `pkg.order.order.Order` 같은 이름 반복은 재노출 표면이 있어야 가려진다. 모델마다 파일 하나인 구조가 순환을 낳는다는 PEP 484 의 기록(7.2)도 Python 고유의 비용이다.

**타입만 공개하기와 이름 재사용.** 공개 이름을 타입으로 한정하라는 출처는 없다. 표준 라이브러리는 `json.__all__` 에 `loads` 같은 함수를, `collections.__all__` 에 `namedtuple` 을 두고(CPython Lib), Guido 는 `len(x)` 가 `x.len()` 보다 읽는 이에게 덜 전제한다며 일부 연산을 함수로 두었다(Python Design FAQ). Google 은 이름 대신 모듈을 import 하라며 "`x.Obj` says that object `Obj` is defined in module `x`"(`x.Obj` 는 `Obj` 가 어디 정의되었는지 보여 준다)를 이유로 든다(Google pyguide). Ronacher 는 2013 년에 함수만 있는 API 는 확장 지점이 없다며 클래스를 옹호했지만 관심사는 라이브러리 확장성이었다(Ronacher 2013). 명시적 표면 자체는 주류여서 `asyncio/__init__.py` 는 17 개 하위 모듈의 `__all__` 을 합치고, 표준 라이브러리는 `queue.Queue`, `asyncio.Queue` 처럼 같은 이름을 책임이 다른 모듈에 두고 이름공간으로 구분한다(CPython Lib). 정적 메서드 이름공간이나 파일당 클래스 하나를 에이전트나 검사기 관점에서 평가한 2023–2026 년 자료는 없고, 세 쟁점의 찬반은 의견과 몇 가지 형식적 성질에 기댈 뿐이다.

### 7.7 정리: Python 에서 특별히 요구되거나 권장되는 것

종류는 언어 규칙(언어 명세와 typing spec), 공식 권고(PEP, 공식 문서, PyPA), 도구가 강제(켜면 검사기가 막는 것), 실무 관례(스타일 지침, 전문가와 조직의 경험)로 나눈다.

| 요구·권장 | 종류 | 출처 |
|---|---|---|
| `__all__` 과 밑줄로 공개와 내부를 표시하고, import 한 이름은 구현 세부로 본다(패키지 `__init__` 재노출은 예외) | 공식 권고 | PEP 8 |
| `py.typed` 패키지의 밑줄 없는 파일은 공개, 재노출은 `X as X`·`*`·정적 `__all__` 로만 | 언어 규칙, 도구가 강제(mypy `--strict`, pyright) | typing spec; mypy docs; pyright docs |
| import 는 맨 위, 기본은 절대 경로, 복잡한 구조에서는 명시적 상대 import 허용 | 공식 권고 (Google 은 상대 import 금지) | PEP 8; PEP 328; Google pyguide |
| 순환은 언어상 허용되나 최상위 이름 import 에서 깨지므로 설계에서 피한다 | 언어 규칙, 공식 권고 | Python Reference; Python FAQ; PEP 810 |
| 타입 전용 import 는 `TYPE_CHECKING` 가드 (3.14 부터 주석 지연 평가, `__future__` import 는 폐기 예정) | 언어 규칙 | PEP 484; PEP 749 |
| 지연 로드는 라이브러리가 명시적으로 (`__getattr__` 3.7, `lazy` 3.15, 전역 암묵 지연은 거부됨) | 언어 규칙 | PEP 562; PEP 810; SC 2022 |
| import 부수효과 등록 대신 명시적 발견 함수, 하위 모듈은 명시 import, 플러그인은 entry point | 공식 권고, 대규모 경험 | PEP 810; PyPA plugins; Cinder Lazy Imports |
| 인터페이스는 Protocol 또는 ABC, 명시 상속은 선택이지만 정적 검증을 준다 | 언어 규칙, 공식 권고 | PEP 544; typing spec; typing guide |
| 재정의에 `@override` (3.12 부터, 전면 요구는 검사기의 선택 모드) | 언어 규칙, 도구가 강제 | PEP 698 |
| `TypeAlias` 는 deprecated(제거 계획 없음), `type` 문은 클래스를 대신하지 못함 | 언어 규칙 | typing docs |
| 층과 역전은 비용을 따져 쓰고, 연결은 진입점에서, 입출력은 위로 | 실무 관례 | Percival & Gregory 2020; Seddon 2019b; Rhodes 2015 |
| 가변 전역 상태와 레지스트리를 피하고, 라이브러리 로깅은 `NullHandler` 만 | 실무 관례, 공식 권고 | Google pyguide; Logging HOWTO |
| src 레이아웃 | 공식 권고(논의 문서), 실무 관례 (상충) | PyPA src layout; HHGP |
| 층·비순환 규칙은 도구로 강제하고 예외 목록은 줄이기만 | 도구가 강제, 대규모 경험 | import-linter docs; tach docs; Seddon 2023 |
| 정적 메서드 대신 모듈 수준 함수 (반론 있음) | 공식 권고(FAQ), 실무 관례(Google 금지) | Python FAQ; Google pyguide; Hettinger 2013 |
| 파일당 클래스 하나는 요구되지 않는다 (공식 문서는 침묵) | 실무 관례 | Google pyguide; SO 106896 |

이 항목들이 ln-structure 의 규칙과 판단 기준에 주는 시사점은 별도 장에서 다룬다.

### 참고문헌 (7장)

모든 출처는 2026-10-18 에 조회했다. 상태는 2026-10 기준이다. [미확인]은 원문 문구나 현재 지위를 확인하지 못한 것, [2차 출처]는 요약을 거쳐서만 확인한 것이다.

**공식 문서와 명세**

- PEP 8. van Rossum, G., Warsaw, B., Coghlan, A. (2001, 2013 개정). Style Guide for Python Code. Process, Active. https://peps.python.org/pep-0008/
- PEP 20. Peters, T. (2004). The Zen of Python. Informational, Active. https://peps.python.org/pep-0020/
- PEP 328. Aahz (2003). Imports: Multi-Line and Absolute/Relative. Final. https://peps.python.org/pep-0328/
- PEP 484. van Rossum, G., Lehtosalo, J., Langa, Ł. (2014). Type Hints. Final (3.5). https://peps.python.org/pep-0484/
- PEP 544. Levkivskyi, I., Lehtosalo, J., Langa, Ł. (2017). Protocols: Structural subtyping (static duck typing). Final (3.8). https://peps.python.org/pep-0544/
- PEP 562. Levkivskyi, I. (2017). Module `__getattr__` and `__dir__`. Final (3.7). https://peps.python.org/pep-0562/
- PEP 563. Langa, Ł. (2017). Postponed Evaluation of Annotations. Superseded. https://peps.python.org/pep-0563/
- PEP 649. Hastings, L. (2021). Deferred Evaluation Of Annotations Using Descriptors. Final (3.14). https://peps.python.org/pep-0649/
- PEP 690. Méndez Bravo, G., Meyer, C. (2022). Lazy Imports. Rejected (2022-12-02). https://peps.python.org/pep-0690/
- PEP 698. Troxler, S. et al. (2022). Override Decorator for Static Typing. Final (3.12). https://peps.python.org/pep-0698/
- PEP 749. Zijlstra, J. (2024). Implementing PEP 649. Final (3.14). https://peps.python.org/pep-0749/
- PEP 781. Inada Naoki (2025). Make `TYPE_CHECKING` a built-in constant. Draft. https://peps.python.org/pep-0781/
- PEP 790. Python 3.15 출시 일정 (3.15.0 출시일 2026-10-09 기록). https://peps.python.org/pep-0790/
- PEP 810. Galindo Salgado, P. et al. (2025). Explicit lazy imports. Final (3.15). https://peps.python.org/pep-0810/
- PEP 3119. van Rossum, G., Talin (2007). Introducing Abstract Base Classes. Final (3.0). https://peps.python.org/pep-3119/
- SC 2022. Smith, G. P., Python Steering Council 대표 (2022-12-02). PEP 690 거부 결정. https://discuss.python.org/t/pep-690-lazy-imports-again/19661/26
- SC 2025. Warsaw, B., Python Steering Council 대표 (2025-11-03). PEP 810 수락 결정. https://discuss.python.org/t/pep-810-explicit-lazy-imports/104131/466
- Peters 2015. Peters, T. (2015-09-16). Re: PEP 504: Using the system RNG by default. python-ideas. https://mail.python.org/pipermail/python-ideas/2015-September/036254.html
- Python Reference. PSF. The Python Language Reference 3.15, "The import system" 와 "The import statement"(Lazy imports 포함). https://docs.python.org/3/reference/import.html ; https://docs.python.org/3/reference/simple_stmts.html#the-import-statement
- Python Tutorial. PSF. The Python Tutorial 3.15, §6 Modules. https://docs.python.org/3/tutorial/modules.html
- Python FAQ. PSF. Programming FAQ 3.15 (순환 import, import 위치, 정적 메서드 항목). https://docs.python.org/3/faq/programming.html
- Python Design FAQ. PSF. Design and History FAQ 3.15. https://docs.python.org/3/faq/design.html
- What's New 3.15. PSF. What's New In Python 3.15, Lazy imports. https://docs.python.org/3/whatsnew/3.15.html
- typing docs. PSF. `typing` 모듈 문서 3.15 (`TYPE_CHECKING`, `TypeAlias`, `override`). https://docs.python.org/3/library/typing.html
- typing spec. Python Typing Council. Specification for the Python type system (2026 스냅샷): Distributing type information, Protocols, Directives, Class compatibility. https://typing.python.org/en/latest/spec/distributing.html ; https://typing.python.org/en/latest/spec/protocol.html ; https://typing.python.org/en/latest/spec/directives.html ; https://typing.python.org/en/latest/spec/class-compat.html
- typing guide. Python Typing Council. Typing Python Libraries. https://typing.python.org/en/latest/guides/libraries.html
- unittest.mock docs. PSF. `unittest.mock`, "Where to patch". https://docs.python.org/3/library/unittest.mock.html#where-to-patch
- Logging HOWTO. PSF. Configuring Logging for a Library. https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
- PyPA src layout. PyPA. src layout vs flat layout (논의 문서, 의무 아님). https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- PyPA plugins. PyPA. Creating and discovering plugins. https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/

**실무 지침과 전문가 의견**

- Percival & Gregory 2020. Percival, H., Gregory, B. *Architecture Patterns with Python*. O'Reilly. 온라인판 원고(cosmicpython/book)에서 인용, 인쇄판과 문구가 조금 다를 수 있다. Introduction, 2·3·13 장, Appendix B, Epilogue. https://www.cosmicpython.com/book/introduction.html ; https://www.cosmicpython.com/book/chapter_02_repository.html ; https://www.cosmicpython.com/book/chapter_03_abstractions.html ; https://www.cosmicpython.com/book/chapter_13_dependency_injection.html ; https://www.cosmicpython.com/book/appendix_project_structure.html ; https://www.cosmicpython.com/book/epilogue_1_how_to_get_there_from_here.html
- Rhodes 2014. Rhodes, B. The Clean Architecture in Python. PyOhio 2014-07-27 (슬라이드만 읽음). https://rhodesmill.org/brandon/slides/2014-07-pyohio/clean-architecture/
- Rhodes 2015. Rhodes, B. Hoisting Your I/O. PyWaw Summit 2015-05-25 (슬라이드만 읽음). https://rhodesmill.org/brandon/slides/2015-05-pywaw/hoist/
- Rhodes 2018. Rhodes, B. The Global Object Pattern. python-patterns.guide (2018 작성, 2023 수정). https://python-patterns.guide/python/module-globals/
- Schlawack 2021. Schlawack, H. Subclassing in Python Redux (2021-06-22). https://hynek.me/articles/python-subclassing-redux/
- Schlawack 2025. Schlawack, H. Design Pressure. PyCon US 2025, EuroPython 2025 (SpeakerDeck 슬라이드 텍스트). https://speakerdeck.com/hynek/design-pressure ; https://hynek.me/talks/design-pressure/
- Google pyguide. Google Python Style Guide (살아 있는 문서, 2026-10-17 커밋 기준). https://google.github.io/styleguide/pyguide.html
- HHGP. Reitz, K., Real Python. The Hitchhiker's Guide to Python, "Structuring Your Project" (2021-02 마지막 수정, 배치 조언은 2013 년 것). https://docs.python-guide.org/writing/structure/
- Flask docs. Pallets. Large Applications as Packages. https://flask.palletsprojects.com/en/stable/patterns/packages/
- Django docs. Django. Signals; Applications. https://docs.djangoproject.com/en/dev/topics/signals/ ; https://docs.djangoproject.com/en/dev/ref/applications/
- Eby 2004a. Eby, P. J. (2004-12). Python Is Not Java. https://dirtsimple.org/2004/12/python-is-not-java.html
- Ramalho 2022. Ramalho, L. *Fluent Python* 2판 §11.5. O'Reilly. 저자의 포르투갈어 무료판에서 옮겨 영어 문구는 [미확인]. https://pythonfluente.com/2/
- wemake. wemake-python-styleguide 1.8.1, WPS602. https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/oop.html
- Hettinger 2013. Hettinger, R. Python's Class Development Toolkit. PyCon US 2013-03-16. 자동 자막 인용이라 문구 [미확인]. https://www.youtube.com/watch?v=HTLu2DFOdTg
- Danjou 2013. Danjou (2013-08-01). 정적·클래스·추상 메서드 안내 글. https://julien.danjou.info/blog/guide-python-static-class-abstract-methods
- Diederich 2012. Diederich, J. Stop Writing Classes. PyCon US 2012. 자동 자막 인용이라 문구 [미확인]. https://www.youtube.com/watch?v=o9pEzgHorH0
- Ronacher 2013. Ronacher, A. (2013-02-13). Start Writing More Classes. https://lucumr.pocoo.org/2013/2/13/moar-classes/
- Ronacher 2025. Ronacher, A. (2025-06-12). Agentic Coding Recommendations. https://lucumr.pocoo.org/2025/6/12/agentic-coding/
- SO 106896. Stack Overflow 질문 106896 (2008, 2013 종료), 채택 답변 S.Lott. https://stackoverflow.com/questions/106896
- JLS SE21. Oracle. The Java Language Specification, Java SE 21, §7.6. https://docs.oracle.com/javase/specs/jls/se21/html/jls-7.html#jls-7.6
- CPython Lib. python/cpython `Lib/` (main 브랜치). https://github.com/python/cpython/tree/main/Lib

**도구**

- Seddon 2019a. Seddon, D. (2019-05-20). Meet Import Linter. https://seddonym.me/2019/05/20/meet-import-linter/
- Seddon 2019b. Seddon, D. (2019-08-03). Three Techniques for Inverting Control, in Python. https://seddonym.me/2019/08/03/ioc-techniques/
- Seddon 2025. Seddon, D. (2025-11-12). Six lines of code to prevent Python spaghetti. https://seddonym.me/2025/11/12/six-lines-of-code/
- import-linter docs. Seddon, D. et al. Import Linter 2.15 (2026-09-04) 문서와 릴리스 노트. https://github.com/seddonym/import-linter/blob/main/docs/contract_types/layers.md ; https://github.com/seddonym/import-linter/blob/main/docs/contract_types/acyclic_siblings.md ; https://github.com/seddonym/import-linter/blob/main/docs/contract_types/index.md ; https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md
- tach docs. tach v0.35.3 (2026-10-06, tach-org). https://github.com/tach-org/tach ; https://github.com/tach-org/tach/blob/main/docs/usage/configuration.md ; https://github.com/tach-org/tach/blob/main/docs/usage/layers.md ; https://github.com/tach-org/tach/blob/main/docs/getting-started/why-tach.md ; https://github.com/tach-org/tach/issues/791#issuecomment-3509472391
- Ruff. Astral. Ruff 0.17.1 (2026-10-15) 규칙 소스. https://github.com/astral-sh/ruff/tree/main/crates/ruff_linter/src/rules/flake8_tidy_imports/rules ; https://github.com/astral-sh/ruff/blob/main/crates/ruff_linter/src/rules/pylint/rules/import_outside_top_level.rs
- pylint. pylint 4.1.3 (2026-10-11): imports 검사기, cyclic-import 설명, no-self-use 설명, 2.14 변경 요약. https://github.com/pylint-dev/pylint/blob/main/pylint/checkers/imports.py ; https://github.com/pylint-dev/pylint/blob/main/doc/data/messages/c/cyclic-import/details.rst ; https://github.com/pylint-dev/pylint/blob/main/doc/data/messages/n/no-self-use/details.rst ; https://github.com/pylint-dev/pylint/blob/main/doc/whatsnew/2/2.14/summary.rst
- mypy docs. mypy, `--no-implicit-reexport`. https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport
- pyright docs. Microsoft. pyright 1.1.414 (2026-09-09): configuration, typed-libraries. https://github.com/microsoft/pyright/blob/main/docs/configuration.md ; https://github.com/microsoft/pyright/blob/main/docs/typed-libraries.md

**대규모 사례**

- Seddon 2023. Seddon, D. (2023-07-11). Kraken Technologies: How we organise our very large Python monolith. EuroPython Society blog (조회 도구의 원문 추출로 인용, 미세한 전사 차이 가능). https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/
- Lehtosalo 2019. Lehtosalo, J. (2019-09-05). Our journey to type checking 4 million lines of Python. Dropbox Tech Blog. https://dropbox.tech/application/our-journey-to-type-checking-4-million-lines-of-python
- Sanguansin & Shah 2021. Sanguansin, N., Shah, U. (2021-03-04). Atlas: Our journey from a Python monolith to a managed platform. Dropbox Tech Blog. https://dropbox.tech/infrastructure/atlas--our-journey-from-a-python-monolith-to-a-managed-platform
- Cinder Strict Modules. Meta. Cinder 문서, Strict Modules (`cinder/3.10` 브랜치. `meta/3.14` 브랜치에는 없어 현재 지위 [미확인]). https://github.com/facebookincubator/cinder/tree/cinder/3.10/CinderDoc/strict_modules
- Cinder Lazy Imports. Meta. Cinder 문서, Lazy Imports (`cinder/3.10` 브랜치, 내부 측정이며 방법 미공개). https://github.com/facebookincubator/cinder/blob/cinder/3.10/CinderDoc/lazy_imports.md
- Méndez Bravo 2024. Méndez Bravo, G. (2024-01-18). "Lazy is the new fast…" (제목은 노트의 축약형). Engineering at Meta. https://engineering.fb.com/2024/01/18/developer-tools/lazy-imports-cinder-machine-learning-meta/
