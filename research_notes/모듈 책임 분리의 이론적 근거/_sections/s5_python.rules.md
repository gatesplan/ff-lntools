# 7장(Python) 보조 파일: 규칙 후보와 ln-structure 시사점

출처 키는 `s5_python.md` 의 "참고문헌 (7장)" 을 따른다. 그 목록에 없는 출처는 맨 끝 "추가 출처" 에 URL 과 함께 적었다. 표시: (추론) 은 노트나 이 파일의 추론, [미확인] 은 원문이나 지위를 확인하지 못한 것, [미시험] 은 도구 동작을 시험하지 않은 것, (d1)~(d4) 는 근거가 된 노트다.

## 규칙 후보

1. **공개 이름은 `__init__.py` 의 명시적 재노출과 정적으로 읽히는 `__all__`(리터럴 목록 등 spec 이 인정한 형태)로 선언한다.**
   - 근거: PEP 8 은 `__all__` 선언과 "a package's `__init__` module that exposes functionality from submodules" 를 공개 통로로 인정한다. typing spec 에서 `__all__` 은 모든 규칙에 우선하지만 정해진 관용만 정적으로 계산된다. mypy `--strict`, pyright 는 명시 재노출만 공개로 본다. `asyncio/__init__.py` 의 `__all__` 합산이 표준 라이브러리 선례다.
   - 출처: PEP 8; typing spec; mypy docs; pyright docs; CPython Lib.
   - 강도: 공식 + 도구 강제, 강.
   - 반론·한계: Google 은 이름 대신 모듈을 import 하라고 한다(`x.Obj` 의 출처 표시). 즉시 실행되는 재노출 `__init__.py` 는 하위 트리 전체를 로드한다(HHGP; Cinder Lazy Imports 의 약 12 배 차이).

2. **내부 모듈과 파일은 밑줄로 표시하거나, 표시하지 않는다면 도구로 내부성을 강제한다.**
   - 근거: PEP 8 은 `__all__` 이 있어도 내부 이름에 밑줄을 요구하고, 감싸는 이름공간이 내부면 그 안도 내부다. typing spec 은 `py.typed` 패키지의 밑줄 없는 파일을 모두 "the supported interface" 로 본다.
   - 출처: PEP 8; typing spec; pyright docs.
   - 강도: 공식 권고, 중 (typing spec 규칙은 `py.typed` 를 배포하는 패키지에만 해당).
   - 반론·한계: PEP 8 의 공개 기준은 문서화이므로 문서화되지 않은 파일은 밑줄 없이도 내부다. 밑줄 경로는 어색하다. import-linter `protected`, tach `expose` 처럼 도구로 대신할 수 있다.

3. **import 는 파일 맨 위에 두고 함수 안 import 를 쓰지 않는다.**
   - 근거: PEP 8 과 Programming FAQ(순환 회피, 초기화 비용일 때만 예외). PEP 810 은 함수 안 import 가 "obfuscates the full set of dependencies for a module" 라 한다. Ruff PLC0415 설명은 함수 안 import 가 대개 순환 회피용이라 본다. HHGP 는 이를 "fragile hacks" 라 부른다.
   - 출처: PEP 8; Python FAQ; PEP 810; Ruff; HHGP.
   - 강도: 공식 권고 + 도구(선택), 강.
   - 반론·한계: FAQ 는 예외를 인정한다. 표준 라이브러리 import 의 약 17% 가 지연용으로 함수 안에 있다(PEP 810, 방법 미상). 3.15 의 `lazy` 가 대안이다.

4. **모듈 사이의 import 순환을 금지하고 도구로 강제한다.**
   - 근거: 순환 import 는 부분 초기화 모듈을 본다(Python Reference). PEP 810: "The best practice is still to avoid circular imports in your code design". Seddon: "There's always, always a way to reorganize code so a cycle is avoided". Dropbox 의 엉킴(순환 안 파일 하나만 바뀌어도 mypy 가 순환 전체를 재처리), Atlas 의 수년에 걸친 순환 제거, Kraken 의 계약. pyright 는 순환이 "often hint at architectural layering issues" 라 쓴다.
   - 출처: Python Reference; PEP 810; Seddon 2025; Lehtosalo 2019; Sanguansin & Shah 2021; Seddon 2023; pyright docs.
   - 강도: 대규모 경험 + 전문가 의견, 강. 언어는 순환을 허용하고 공식 문서는 금지하지 않는다.
   - 반론·한계: FAQ 는 구조 변경을 세 처방 중 하나로만 둔다. PEP 810 은 타입 관련 순환을 "an intentional and desirable thing" 이라 부른다. pyright 와 tach 의 순환 검사는 기본으로 꺼져 있다.

5. **`if TYPE_CHECKING:` 안의 import 를 의존으로 셀지 명시적으로 정한다.**
   - 근거: 공식 문서는 정하지 않았다(d1). 도구 기본값이 갈린다: import-linter 는 센다(`exclude_type_checking_imports` 는 선택), tach 는 기본 무시(`ignore_type_checking_imports = true`), pylint 는 순환 검사에서 뺀다. 검사기는 가드 안 import 를 일반 import 처럼 해석한다.
   - 출처: import-linter docs; tach docs; pylint; typing spec.
   - 강도: 도구 동작, 중.
   - 반론·한계: 세면 타입 전용 순환이 위반이 되는데 공식 문서는 가드를 정당한 순환 해법으로 다룬다. 안 세면 의존을 가드 안에 숨길 수 있다(추론, d3).

6. **3.10–3.13 을 지원하면 가드 안 이름을 주석에 쓰는 방식(따옴표 또는 `from __future__ import annotations`)을 정한다.**
   - 근거: 주석은 3.14 부터 지연 평가된다(PEP 649/749). `__future__` import 는 PEP 649 이전 마지막 판(3.13 예상)의 지원 종료 뒤 deprecated, 최소 두 판 뒤 제거 예정이다(PEP 749). 그 전 판에서 가드 안 이름을 주석에 쓰려면 둘 중 하나가 필요하다(추론, d1).
   - 출처: PEP 649; PEP 749; typing docs.
   - 강도: 언어 규칙, 강.
   - 반론·한계: `__future__` 방식은 장기적으로 없어진다. 따옴표는 번거롭다. `TYPE_CHECKING` 내장화(PEP 781)는 Draft.

7. **import 시점 부수효과(등록, 몽키패치, I/O)를 금지하고, 레지스트리는 진입점이 부르는 명시적 함수로 채운다.**
   - 근거: PEP 810: "registries of objects should be constructed via explicit discovery processes (e.g. a well-known function to call)". Cinder strict modules 는 데코레이터 레지스트리를 금지한다("you cannot use a decorator to create a registry of functions"). Meta 의 지연 import 도입에서 암묵적 등록이 깨졌다("side effects failing to register classes, functions, and operations correctly"). Rhodes, Google(§2.5 전역 레지스트리, §2.17 import 시점 데코레이터 실패). PyPA entry point 는 선언과 `.load()` 를 분리한다. 3.15 의 `-X lazy_imports=all` 로 하류 응용이 라이브러리 import 를 지연시킬 수 있어 import 시점 등록은 조용히 깨질 수 있다(추론, d1).
   - 출처: PEP 810; Cinder Strict Modules; Cinder Lazy Imports; Méndez Bravo 2024; Rhodes 2018; Google pyguide; PyPA plugins; What's New 3.15.
   - 강도: 공식 권고 + 대규모 경험, 강.
   - 반론·한계: Flask 와 Django 는 여전히 import 로 등록한다(함정은 스스로 문서화). Seddon 은 시작 시점에 고정되는 레지스트리를 좋은 선택으로 본다. 진입점에서 채우면 두 입장은 양립한다.

8. **하위 모듈은 명시적으로 import 하고, 부모 패키지 속성으로 우연히 붙은 하위 모듈에 기대지 않는다.**
   - 근거: PEP 810: "Always import needed submodules explicitly". Meta 의 지연 import 함정에 "reliance on submodules being set as attributes on their imported parent module" 이 있다. strict modules 에서는 부모가 자식을 명시적으로 공개해야 한다.
   - 출처: PEP 810; Cinder Lazy Imports; Cinder Strict Modules.
   - 강도: 공식 권고 + 대규모 경험, 중.
   - 반론·한계: 일상 코드에서는 부모 속성 접근이 우연히 동작하므로 위반이 드러나지 않는다(PEP 810 의 "unreliably").

9. **지연 로드는 라이브러리 저자가 명시적으로 통제하고(PEP 562 `__getattr__`, 3.15+ `lazy`), 지연 import 도 의존으로 센다.**
   - 근거: PEP 562 의 동기가 하위 모듈 지연 import 다. SC 는 전역·암묵 지연(PEP 690)을 거부하고 명시적·국소적 지연(PEP 810)을 수락했다. 검사기는 `lazy` import 를 일반 import 로 해석해도 되고, grimp 3.16 은 `is_lazy` 로 기록한다.
   - 출처: PEP 562; SC 2022; SC 2025; PEP 810; grimp docs.
   - 강도: 언어 규칙 + 공식, 중.
   - 반론·한계: `.py` 파일의 모듈 `__getattr__` 로만 공급되는 이름에 대한 규칙은 spec 에 없다(d1). PEP 810 은 지연이 "visible at the import site itself" 이길 원한다.

10. **인터페이스는 Protocol 또는 ABC 로 적고, 정의 지점에서 검증받으려면 명시 상속하며, 재정의에 `@override` 를 붙인다.**
    - 근거: 명시 상속하면 검사기가 "statically verify that the class actually implements the protocol correctly". spec 은 "We still slightly prefer nominal subtyping". 상속되어야 하는 클래스는 ABC(typing guide). `@override` 전면 요구는 spec 이 지지하는 선택 모드다.
    - 출처: typing spec; typing guide; PEP 544; PEP 698.
    - 강도: 공식, 중. 런타임 검사는 없다.
    - 반론·한계: PEP 544 는 명시 표시 강요를 "unpythonic" 이라 하며, 구조적 타입은 라이브러리 깊숙이 숨은 타입 때문에 생겼다. APWP 는 ABC 를 운영 코드에서 지웠고 Schlawack 은 소비자 쪽 Protocol 을 권한다. 외부 타입에 상속을 요구하면 어댑터가 필요하다(추론, d1).

11. **입출력과 외부 도구(ORM, 웹 프레임워크) 의존은 위쪽(진입점, 접착 코드)에 두고 아래쪽은 순수 로직으로 둔다.**
    - 근거: Rhodes 의 hoisting I/O("To get rid of I/O, make it subordinate"), APWP 의 onion 구조("your ORM should import your model")와 Functional Core, Imperative Shell, Schlawack 의 "protect it from your tools", Sans-I/O.
    - 출처: Rhodes 2014; Rhodes 2015; Percival & Gregory 2020; Schlawack 2025; Sans-I/O.
    - 강도: 전문가 의견, 중.
    - 반론·한계: APWP 는 단순 CRUD 앱에는 필요 없다고 한다. 층마다 타입을 따로 두면 매핑 비용이 든다(Schlawack 2025).

12. **의존성 역전과 DI 는 필요할 때만 쓰고, 연결은 진입점의 조립 코드 한 곳에서 한다.**
    - 근거: APWP(DI 는 "regarded with suspicion in the Python world", bootstrap 이 조립 루트, 설정은 bootstrap 만 import), Seddon(`main` 에서 연결), Kraken(역전의 국소 복잡도는 감수할 만), Flask 앱 팩토리(테스트, 여러 인스턴스), Logging HOWTO(핸들러 설정은 응용의 몫).
    - 출처: Percival & Gregory 2020; Seddon 2019b; Seddon 2023; Flask app factories; Logging HOWTO.
    - 강도: 실무 관례, 중.
    - 반론·한계: APWP 공저자끼리도 과설계 논쟁이 있었다. 메시지 버스가 여전히 모듈 전역으로 남는 흠을 저자들도 인정한다.

13. **가변 전역 상태와 전역 레지스트리를 피하고, 라이브러리는 로깅 핸들러를 설정하지 않는다(`getLogger(__name__)`, `NullHandler` 만).**
    - 근거: Google §2.5 "Avoid mutable global state", Rhodes 의 모듈 전역 경고, Logging HOWTO.
    - 출처: Google pyguide; Rhodes 2018; Logging HOWTO.
    - 강도: 로깅은 공식 권고로 강, 전역 상태는 실무 관례로 중.
    - 반론·한계: Google 은 모듈 수준 상수를 권한다. `__name__` 로거는 관례상 모듈 수준 객체다(노트의 해석, d2).

14. **경계 규칙은 문서가 아니라 도구로 강제하고, 기존 위반은 줄어들기만 하는 예외 목록(래칫)으로 관리한다.**
    - 근거: Kraken "just talking about the layering was not enough", 무시한 import 수를 부채 지표로 줄임(몇 년 뒤 15 건). import-linter 는 맞지 않는 예외 항목을 기본으로 오류 처리하고 2.14 부터 예외 수를 출력한다. tach `sync`/`unchecked`/`deprecated`/`exact`, deply 의 신규·기존·해결 기준선. Dropbox 는 새 코드에 엄격도를 점진적으로 올렸고, Kraken 은 일부 린터를 바뀐 파일에만 돌린다. Layer Linter 의 동기: 분리해 둔 것이 "creeps inexorably together".
    - 출처: Seddon 2023; import-linter docs; tach docs; deply; Lehtosalo 2019; Jaeger 2024; Seddon 2018.
    - 강도: 대규모 경험 + 도구, 강 (통제된 비교 없음).
    - 반론·한계: 효과의 전후 자료가 없다. 예외는 몇 년이 지나도 남는다.

15. **같은 층 형제 사이 import 를 허용할지 명시적으로 정한다.**
    - 근거: import-linter 는 `|`(독립, 서로 금지)와 `:`(서로 허용, 2.0 추가)를 둘 다 두고, 층 패키지 안의 하위 모듈끼리는 제한하지 않는다. grimp API 는 여러 모듈 층을 기본으로 독립으로 본다. tach 는 같은 층 의존을 선언하면 허용한다.
    - 출처: import-linter docs; grimp docs; tach docs.
    - 강도: 도구 동작, 중.
    - 반론·한계: 완화형이 나중에 추가된 것은 수요가 있다는 뜻이다(추론, d3).

16. **동적 import(`importlib.import_module`, `__import__`, 문자열 경로)를 제한한다.**
    - 근거: AST 기반 도구는 이를 보지 못한다. tach FAQ: "dynamic imports (e.g. using a string path) and dynamic names ... are not supported". Ruff TID251: "can be circumvented via `eval` or `importlib`".
    - 출처: tach FAQ; Ruff.
    - 강도: 도구 한계, 중.
    - 반론·한계: entry point 의 `.load()` 같은 플러그인 로딩은 본래 동적이므로 진입점에서는 허용해야 한다(추론).

17. **상태 없는 함수는 모듈 수준 함수로 둔다 (Python 주류 관례).**
    - 근거: Programming FAQ("a far more straightforward way"), Google §2.17(금지), Eby, wemake WPS602, Ramalho [미확인], Ronacher 2025(에이전트에게도 함수 권장).
    - 출처: Python FAQ; Google pyguide; Eby 2004a; wemake; Ramalho 2022; Ronacher 2025.
    - 강도: 공식 권고(FAQ) + 실무 관례, 중~강.
    - 반론·한계: Hettinger(찾기 쉬움, 올바른 맥락) [미확인], Danjou(하위 클래스 재정의), Diederich(작은 이름공간으로서의 클래스) [미확인], `patch.object` 의 테스트 이점. pylint 는 이 판단을 "too opinionated" 로 보고 선택 검사로 돌렸다. 어느 쪽도 자료는 없다.

18. **관련 클래스와 함수는 한 모듈에 둘 수 있다 (파일당 클래스 하나는 요구되지 않는다).**
    - 근거: Google §3.16.2 "no need to limit yourself to one class per module", S.Lott "a module is the unit of reuse", HHGP 의 라비올리 코드, Diederich 의 평평한 이름공간 [미확인].
    - 출처: Google pyguide; SO 106896; HHGP; Diederich 2012.
    - 강도: 실무 관례, 중. 공식 문서는 침묵.
    - 반론·한계: Programming FAQ 는 모듈당 클래스 하나(또는 밀접한 계층 하나) 구조를 정상 선택지로 언급한다. SO 의 소수 답변은 큰 클래스와 탐색성을 이유로 파일 분리를 지지한다. JLS 가 든 근거(도구가 이름으로 파일을 찾음)는 도구와 에이전트 탐색에도 적용된다(추론, d4).

19. **src 레이아웃을 쓴다.**
    - 근거: PyPA(개발 중 사본의 우발적 import 방지, 편집 설치가 import 가능하도록 의도한 파일만 import), Schlawack(설치된 패키지로 테스트).
    - 출처: PyPA src layout; Schlawack 2015.
    - 강도: 공식 논의 문서 + 전문가 의견, 중.
    - 반론·한계: 실행하려면 설치가 필요하다. HHGP 의 2013 년 조언은 반대한다.

## ln-structure 시사점

### 뒷받침

1. **생성된 표면 파일과 `__all__`.** PEP 8 이 이름을 들어 인정하는 유일한 구조적 공개 통로가 "a package's `__init__` module that exposes functionality from submodules" 이고, typing spec 에서 `__all__` 은 모든 규칙에 우선한다. 모듈 표면의 `from .order import Order` 와 리터럴 `__all__` 은 spec 의 관용에 맞으므로 mypy `--strict` 와 pyright 에서도 공개로 보일 것이다(규칙상 추론, [미시험]). 비슷한 장치로 tach `expose`, Dropbox Atlas 의 비공개 디렉터리(Bazel 가시성), import-linter `protected` 가 있다. 출처: PEP 8; typing spec; mypy docs; pyright docs; CPython Lib; tach docs; Sanguansin & Shah 2021; import-linter docs.
2. **모듈 사이 순환 금지와 모듈 안 파일 순환 허용.** import-linter `acyclic_siblings` 와 grimp 의 "locally acyclic" 과 같은 모양이다. Dropbox 에서 순환 안 파일 하나가 바뀌면 순환 전체를 다시 처리해야 했는데, 순환을 한 모듈 안에 가두면 그 비용이 모듈 크기로 묶인다(추론, d3). SO 답변의 "circular imports force you to group things" 도 순환하는 것끼리 한 모듈에 묶는 처방과 맞는다. 출처: import-linter docs; grimp docs; Lehtosalo 2019; SO 106896; Seddon 2025; PEP 810; pyright docs.
3. **더 낮은 층으로만, 같은 층 금지.** import-linter 의 가장 엄격한 형태(`|` 로 묶은 독립 형제)와 Kraken 의 독립 계약에 해당한다. 모든 import 가 엄격히 아래로만 가면 같은 층 두 모듈 사이의 간접 경로도 생길 수 없으므로, `|` 형제의 간접 경로 검사 여부(d3 의 미확인 사항)는 문제가 되지 않는다(추론). 출처: import-linter docs; Seddon 2023.
4. **import 부수효과로 스스로 등록하는 방식 금지 (가장 강한 뒷받침).** PEP 810 의 명시적 발견 권고, Cinder strict modules 의 데코레이터 레지스트리 금지, Meta 지연 import 도입에서 암묵적 등록이 깨진 경험, Rhodes 와 Google 의 경고, Flask 와 Django 가 스스로 적은 함정, PyPA entry point(선언과 `.load()` 분리)가 모두 같은 방향이다. 3.15 의 전역 지연 모드는 import 시점 등록을 하류 설정 하나로 깨뜨릴 수 있어 이 규칙의 가치를 키운다(추론, d1). 출처: PEP 810; Cinder Strict Modules; Cinder Lazy Imports; Méndez Bravo 2024; Rhodes 2018; Google pyguide; Flask docs; Django docs; PyPA plugins; What's New 3.15.
5. **연결은 진입점에서만, 의존성 역전은 1:N 이나 패키지 밖 코드에만.** APWP(DI 는 의심받는다, bootstrap 이 조립 루트, 단순 CRUD 에는 불필요), Seddon(`main` 에서 연결, 시작 시점 레지스트리), Kraken(역전은 국소 복잡도를 늘린다), Flask 앱 팩토리, Logging HOWTO(핸들러 설정은 응용 몫). 역전을 아껴 쓰라는 데 출처들이 일치한다. 출처: Percival & Gregory 2020; Seddon 2019b; Seddon 2023; Flask app factories; Logging HOWTO.
6. **층·패키지 표면의 PEP 562 지연 로드.** 하위 모듈 지연 import 는 PEP 562 자신의 동기다. `from ..lX import Foo` 는 import 문에서 바로 `__getattr__` 을 부르므로 실패가 import 지점에서 드러나고, SC 가 PEP 690 에 대해 걱정한 "첫 사용 시점에 어디서나" 문제는 대부분 해당하지 않는다(추론, d1; Reference 의 from-import 이름 해석 절차). 지연을 라이브러리 저자가 통제하므로 PEP 810 의 "controlled" 와도 맞는다. 기계적 필요도 있다. 하위 모듈 하나를 불러도 감싸는 `__init__.py` 가 모두 실행되고(Python Reference; HHGP), Meta 는 지연으로 로드 모듈이 약 12 분의 1 이 되었다. 출처: PEP 562; Python Reference; SC 2022; PEP 810; HHGP; Cinder Lazy Imports.
7. **`TYPE_CHECKING` import 도 의존으로 센다.** import-linter 의 기본값과 같다. PEP 810 은 주석 전용 import 를 지연될 뿐인 실제 import 로 다루고(`lazy` 가 가드를 대신), 검사기는 가드 안 import 를 일반 import 처럼 해석한다. 세지 않으면 에이전트가 의존을 가드 안에 숨길 수 있다(추론, d3). 출처: import-linter docs; PEP 810; typing spec.
8. **1:1 상호 호출은 한 모듈 두 파일로, 순환은 `TYPE_CHECKING` 으로 끊는다.** PEP 484 가 기록한 가드의 쓰임("may also be useful to handle import cycles")이고 PEP 649 는 이를 지원되는 동작으로 둔다. 모델마다 파일 하나인 구조가 순환을 낳는다는 PEP 484 의 관찰에 대한 처방이기도 하다. 출처: PEP 484; PEP 649.
9. **인터페이스 명시 상속과 `@override`.** 명시 상속하면 검사기가 정의 지점에서 구현을 검증하고, spec 은 명목적 타입을 조금 더 선호하며, 상속 대상은 ABC 로 하라고 권하고, `@override` 전면 요구는 spec 이 지지하는 선택 모드다. APWP 가 ABC 를 지운 이유("unmaintained and, at worst, misleading")는 검사되지 않는 선언이 썩는다는 것이므로, lnt 가 선언을 검사하면 그 실패 원인을 막는다(추론, d2). 출처: typing spec; typing guide; PEP 698; Percival & Gregory 2020.
10. **패키지 안 상대 import(C5).** PEP 8 은 명시적 상대 import 를 "especially when dealing with complex package layouts" 받아들이고 프로젝트 지침이 우선한다고 한다. PEP 328 의 근거("rearrange the structure of large packages without having to edit sub-packages")는 모듈 폴더가 층 사이를 옮겨 다니는 구조와 맞는다. 옮긴 모듈 안의 상대 import 는 그대로 둘 수 있다(추론). 출처: PEP 8; PEP 328.
11. **모듈마다 한 줄 책임.** APWP 는 진흙공의 원인을 각 구성 요소의 책임을 분명히 하지 않은 데서 오는 균질성으로 진단한다. `utils` 처럼 목적 없는 이름의 모듈이 무너진다는 경험(Buczyński 2020, Go 블로그의 같은 조언)은 책임을 이름과 한 줄로 고정하는 규칙을 뒷받침한다. APWP 의 "Separate the what from the how" 는 추상화에 관한 휴리스틱이라 "무엇만 쓴다" 는 책임 문장 규칙과는 유비에 그친다. 출처: Percival & Gregory 2020; Buczyński 2020; Ajmani 2015.
12. **규칙을 기계로 강제하는 것.** Kraken "just talking about the layering was not enough", Layer Linter 의 "creeps inexorably together", Rhodes "Python itself will place little pressure upon your code to be decoupled", Seddon "Python has no formal way of declaring, and enforcing, a dependency flow". Kraken 엔지니어는 import-linter 가 "ensures a clear separation of responsibilities" 라 썼다. 코드를 에이전트가 쓰면 이 필요가 더 커진다(추론, d3). 출처: Seddon 2023; Seddon 2018; Rhodes 2015; Seddon 2019a; Jaeger 2024.
13. **중첩 모듈마다 자기 층.** import-linter 의 컨테이너(부모 패키지마다 같은 층 패턴)와 Kraken 의 영역별 층(`territories.jpn` 안의 층)이 대규모에서 작동하는 선례다. 출처: import-linter docs; Seddon 2023.
14. **src 레이아웃(ff-lntools 의 `src/lntools`).** PyPA 와 Schlawack 이 뒷받침한다. 출처: PyPA src layout; Schlawack 2015.

### 도전하거나 어긋나는 것

1. **함수를 정적 메서드로 두는 규칙.** Google §2.17("Never use `staticmethod` unless forced to ... Write a module-level function instead"), wemake WPS602, Programming FAQ("a far more straightforward way"), Eby, Ramalho [미확인], Ronacher 2025(에이전트에게도 함수를 권함)와 정면으로 어긋난다. 이런 자료로 학습한 리뷰어, 린터, 에이전트는 이를 "고치려" 할 것이다(추론, d4). 옹호 근거는 Hettinger 의 찾기 쉬움 [미확인], Danjou 의 재정의 가능성, Diederich 가 용인한 작은 이름공간 [미확인], `patch.object` 정도이고, 양쪽 모두 자료는 없다. 출처: Google pyguide; wemake; Python FAQ; Eby 2004a; Ramalho 2022; Ronacher 2025; Hettinger 2013; Danjou 2013; Diederich 2012; unittest.mock docs.
2. **상수를 클래스 속성으로 두는 규칙.** Eby("static final fields should translate to module-level constants")와 Google("Module-level constants are permitted and encouraged")에 어긋난다. 출처: Eby 2004a; Google pyguide.
3. **타입만 공개하는 규칙.** 이 규칙을 말하는 출처가 없다. 표준 라이브러리는 함수를 공개하고(`json.loads`, `namedtuple`), Guido 는 `len(x)` 를 함수로 둔 이유를 설명했다. PEP 544 에서는 모듈 객체도 프로토콜을 만족하므로 명시적이고 검사 가능한 인터페이스에 클래스가 꼭 필요하지는 않다. "타입만 공개하면 생성과 검사가 쉽다" 는 근거는 AST 에서 최상위 `def` 이름에도 똑같이 적용된다(추론, d4). Ronacher 2013 의 클래스 옹호는 확장성 이야기이지 정적 메서드 묶음 이야기가 아니다. 출처: CPython Lib; Python Design FAQ; PEP 544; Ronacher 2013.
4. **파일당 클래스 하나.** Google §3.16.2, S.Lott, HHGP 의 라비올리 코드, Diederich 의 평평한 이름공간 [미확인]과 어긋난다. `order/order.py` 같은 이름 반복은 생성된 표면만이 가려 준다. 공식 문서의 유일한 언급(FAQ 의 "one class (or tightly related class hierarchy)" 구조)은 권고가 아니다. 출처: Google pyguide; SO 106896; HHGP; Diederich 2012; Python FAQ.
5. **클래스 이름 import 와 상대 import.** Google §2.2("Use `import` statements for packages and modules only, not for individual types, classes, or functions"), §2.2.4("Do not use relative names in imports"), FAQ 에 실린 Guido 의 from-import 회피 권고(순환 맥락), PEP 8 의 절대 import 기본값과 어긋난다. APWP 원고에 보이는 import 도 모두 절대 경로였다(부분 관찰, d2). Ruff TID252 를 켠 프로젝트에서는 상대 import 가 지적된다(기본 범위 `parents`, 세부 동작은 노트에 없음). Google 이 든 이유("helps prevent unintentionally importing a package twice")는 원리가 설명되지 않았다. PEP 8 은 프로젝트 지침이 우선한다고 하므로 형식 위반은 아니다. 또 주 모듈은 절대 import 만 쓸 수 있으므로, 상대 import 를 쓰는 진입점은 `-m` 이나 console script 로 실행해야 한다. 출처: Google pyguide; Python FAQ; PEP 8; Percival & Gregory 2020; Ruff; Python Tutorial.
6. **밑줄 없는 내부 파일이 검사기에는 공개로 보인다.** typing spec 은 `py.typed` 패키지의 밑줄 없는 파일을 모두 "the supported interface" 로 본다. pyright 는 `__init__.py` 의 `from .A import X` 가 하위 모듈 이름 `A` 를 공개로 만든다고 적으므로, 모듈 표면의 `from .order import Order` 는 내부 파일 이름 `order` 를 공개 기호로 만든다. 그래서 `order/order.py` 나 `l0/` 아래 파일 같은 내부 경로가 IDE 자동 import 와 검사기에는 공개로 보이고, lnt 만이 이를 막는다. PEP 8 기준으로는 문서화되지 않았으니 이미 내부지만, PEP 8 은 그래도 밑줄을 요구한다. 이 문제는 `py.typed` 를 배포하는 패키지에서만 생긴다. 출처: typing spec; pyright docs; PEP 8.
7. **`Env: TypeAlias = _Env` 형태.** `typing.TypeAlias` 는 3.12 부터 deprecated(제거 계획 없음)이고 `type` 문으로 옮기라는 권고가 붙어 있다. 그러나 `type Env = _Env` 가 만드는 `TypeAliasType` 은 런타임에 클래스가 아니어서 클래스 대신 쓸 수 없다. typing spec 이 인정하는 같은 이름 재노출은 `from Y import X as X` 이고, `X: TypeAlias = Y` 는 재노출 형태가 아니라 새 이름의 정의다. d1 은 이렇게 내보낸 이름이 `__all__` 에 있어서만 공개라고 추론했지만, 인용된 규칙(밑줄 이름과 import 한 이름이 비공개)대로라면 import 하지 않은 밑줄 없는 이름 `Env` 는 기본으로 공개일 수 있어 그 추론은 근거가 약하다. 검사기 동작은 [미시험]이다. 린터나 에이전트가 deprecated 표시를 보고 `type` 문으로 "고치면" 런타임이 깨진다(추론). 출처: typing docs; typing spec.
8. **지연 표면의 정적 가시성.** 층·패키지 표면의 `__all__ = list(_EXPORTS)` 는 spec 이 인정하는 `__all__` 관용(리터럴 목록이나 튜플, `+=`, `.extend`, `.append`, `.remove`, `+= submodule.__all__`)에 없다. spec 은 "These restrictions allow type checkers to statically determine the value of `__all__`" 라 쓰므로 검사기가 이 `__all__` 을 계산하지 못할 수 있다. `.py` 파일에서 모듈 `__getattr__` 로만 공급되는 이름에 대한 규칙은 spec 에서 찾지 못했다(d1). mypy 와 pyright 가 이 이름과 타입을 보는지, `Any` 로 떨어지는지는 [미시험]이다(d4). 또 PEP 810 은 지연이 "visible at the import site itself, not hidden in global configuration or distant module-level declarations" 이길 원하는데, 생성된 `__getattr__` 표면은 그런 모듈 수준 선언이다(긴장은 약하다). 출처: typing spec; PEP 562; PEP 810.
9. **`TYPE_CHECKING` import 를 의존으로 세는 것은 공식 입장보다 엄격하다.** PEP 484, 563, 649, 781 은 가드를 정당한 순환 해법으로 다루고, PEP 810 은 지연이 허용하는 타입 관련 순환을 "an intentional and desirable thing" 이라 부른다. tach 는 기본으로 무시하고 pylint 는 순환 검사에서 뺀다. 공식 문서에서 도출되는 규칙이 아니라 설계 선택이다(뒷받침 7 의 이유와 함께 적어야 한다). 출처: PEP 484; PEP 563; PEP 649; PEP 781; PEP 810; tach docs; pylint.
10. **의존으로 계산한 층과 선언한 층.** 조사한 도구와 사례는 모두 의미 있는 층 순서를 선언한다(import-linter, tach, Kraken). Seddon 은 "I'd take a layered subpackage over merely an acyclic one any day" 라 한다. 계산된 층은 정해진 배치를 가진 DAG 와 같아서, 의도하지 않았지만 비순환인 의존은 import 하는 쪽을 한 층 올리는 것으로 받아들인다(추론, d3). APWP 는 "Depends on doesn't mean imports or calls, necessarily" 라 하고, 계산된 층만으로는 입출력이 위에 놓인다는 보장이 없다(순수 모듈도 입출력하는 낮은 모듈을 import 할 수 있다, d2). 계산된 층을 평가한 출처는 없다. 설계 의도는 한 줄 책임과 층 이동 검토가 떠맡아야 한다(d3). 출처: import-linter docs; tach docs; Seddon 2023; Seddon 2025; Percival & Gregory 2020.
11. **위로 밀리는 코드.** Kraken 에서 모두가 의존하는 core 는 "more costly and risky to make changes to" 해졌고 위층에 코드가 쌓였다. 계산된 층에서는 새 의존 하나가 모듈과 그 의존자를 한 층씩 위로 옮기므로 폴더 이름 변경이 잦을 것이다(추론, d3). 출처: Seddon 2023.
12. **같은 층 완화 요구.** import-linter 는 2.0 에서 `:` 형제를, tach 는 선언된 같은 층 의존을 허용한다. ln-structure 에서는 동료 모듈이 필요한 모듈이 한 층 위로 올라가야 한다. 출처: import-linter docs; tach docs.
13. **과분해와 깊은 경로.** APWP 의 "WTF factor", HHGP 의 라비올리 코드, PEP 20 의 "Flat is better than nested", Peters 의 평평함 선호, PEP 423(Deferred, 비핵심 저자, 권위 낮음)의 "two levels of nesting are preferred" 는 `pkg.l3.mod.l1.inner` 같은 깊은 경로와 어긋난다. 사용자가 보는 것은 맨 위 표면뿐이라는 점이 이를 누그러뜨린다(d1). 출처: Percival & Gregory 2020; HHGP; PEP 20; Peters 2015; PEP 423.
14. **모듈 안 파일 순환의 런타임 조건.** 허용되는 것과 실제로 동작하는 것은 다르다. 모듈을 묶는 `from . import sibling`, 호출 시점의 속성 접근, `TYPE_CHECKING` 가드 import 만 순환을 견디고, 순환 안의 최상위 `from .a import A` 는 `A` 가 아직 없으면 실패한다(Python FAQ; What's New 3.5·3.7, d1 의 추론). "순환은 TYPE_CHECKING 으로 끊는다" 는 처방은 이와 맞지만, lnt 가 이를 검사하지 않으면 런타임 오류가 남는다(추론). 출처: Python FAQ; Python Reference; What's New 3.5; What's New 3.7.
15. **패키지 밖 구현체의 명시 상속.** 구조적 타입은 라이브러리 깊숙이 숨은 타입 때문에 생겼다(PEP 544). 패키지 밖 코드에 명시 상속을 요구하면 어댑터 클래스가 필요하다(d1). APWP 와 Schlawack 은 소비자 쪽 구조적 포트를 선호한다. 출처: PEP 544; Percival & Gregory 2020; Schlawack 2021.
16. **동적 import 의 사각지대.** lnt 도 AST 로 import 를 읽는다면 tach 와 Ruff 가 인정한 한계(문자열 경로, `importlib`, `eval`)를 똑같이 가진다(추론). 출처: tach FAQ; Ruff.

### 열린 질문

1. **지연 표면을 검사기가 보게 하려면 무엇을 생성해야 하는가.** 후보: (a) `lnt doc` 이 `__all__` 을 `list(_EXPORTS)` 대신 리터럴 목록으로 내보낸다(spec 관용에 맞춤, 추론). (b) `if TYPE_CHECKING:` 블록에 `from .x import Name as Name` 재노출을 둔다(d4 의 제안). (c) `from .x import Name as Name` 과 `__lazy_modules__` 를 쓴다. 3.15 이상에서는 지연되고 3.10–3.14 에서는 즉시 import 되며 검사기에도 보인다. (c) 는 `__lazy_modules__` 가 상대 import 를 해석된 절대 이름으로 맞추는지에 달렸는데 이는 [미확인]이다(d1). PEP 810 본문이 언급한 `"none"` 전역 모드와 What's New 3.15 의 두 값(`all`, `normal`)의 관계도 정리되지 않았다. 출처: typing spec; PEP 810; What's New 3.15.
2. **`Env: TypeAlias = _Env` 대신 `from ..l0.env import Env as Env` 같은 재노출 형태로 충분한가.** 두 형태의 검사기 동작(공개 여부, 타입)은 [미시험]이다. 별칭 형태를 고른 이유가 표면 규칙이나 지연 로드와 관련 있다면 그것을 프로토콜에 적어야 한다. 출처: typing spec; typing docs.
3. **내부 파일과 층 폴더에 밑줄을 붙일 것인가.** PEP 8 과 `py.typed` 규칙에는 맞지만 경로가 어색해진다. 출처: PEP 8; typing spec.
4. **함수 안 import 와 `lazy` import 를 의존으로 셀 것인가.** PEP 810 은 함수 안 import 가 의존을 가린다고 하고, grimp 는 `is_lazy` 를 기록하며, 검사기는 `lazy` 를 일반 import 로 해석한다. 출처: PEP 810; grimp docs; Ruff.
5. **3.10–3.13 의 주석 전략을 프로토콜이 정해야 하는가.** 따옴표와 `from __future__ import annotations` 중 후자는 폐기 경로에 있다. 출처: PEP 749.
6. **`typing_extensions` 는 "외부 패키지를 쓰면 최소 l1" 규칙에서 외부 패키지인가.** `@override` 를 3.10–3.11 에서 쓰려면 필요하다(`typing.override` 는 3.12 부터). Google 은 import 규칙에서 `typing`, `collections.abc`, `typing_extensions` 를 예외로 둔다는 선례가 있다. 출처: PEP 698; Google pyguide.
7. **정적 메서드 규칙이 필요한가.** 찾은 근거는 찾기 쉬움(Hettinger [미확인])과 `patch.object` 의 작은 테스트 이점뿐이다. 에이전트에 대한 자료는 없고, 에이전트 실무 조언(Ronacher 2025)은 오히려 함수를 권한다. 출처: Hettinger 2013; unittest.mock docs; Ronacher 2025.
8. **기존 코드베이스 도입에 기준선(예외 목록)이 필요한가.** import-linter 식(맞지 않는 항목은 오류) 또는 deply 식 지문("stable violation fingerprints for agent integrations")이 후보다. 조사한 모든 이전 사례가 하나를 썼고, Kraken 은 몇 년 뒤에도 15 건이 남았다. 출처: import-linter docs; deply; Seddon 2023.
9. **에이전트용 수정 안내가 준수를 높이는가.** import-linter 의 `broken_contract_guidance`(2.14)와 순환을 끊을 의존 제안(Eades–Lin–Smyth 탐욕 휴리스틱, 최적 보장 없음), deply 의 지문이 예다. [미시험]. 출처: import-linter docs; deply.
10. **닫힌 층(바로 아래 층만)인가, 열린 층(아래 어느 층이든)인가.** grimp 의 `closed=True`, tach 의 closed layers, Rocky River 변형이 있지만 어느 쪽에도 근거는 없다. 출처: grimp docs; tach docs; Seddon 2018b.
11. **낮은 층 모듈이 입출력 라이브러리를 import 하면 경고해서 "입출력은 위로" 를 근사할 수 있는가(d2).** 출처: Rhodes 2015; Percival & Gregory 2020.
12. **소비자 쪽 Protocol 과 연결 지점의 선언으로 명시 상속 규칙을 대신할 수 있는가(d2).** 출처: Schlawack 2021; PEP 544.
13. **같은 층의 타입 이름 충돌은 책임 중복의 신호인가.** 표준 라이브러리는 `Queue`, `Lock`, `Event`, `loads` 를 책임이 다른 모듈에 일부러 되풀이한다. 다만 층 표면은 한 이름공간으로 합쳐지므로 충돌 자체는 막아야 하고, 이를 신호로 쓸 때는 자동 거부보다 사람 검토가 낫다(d4). 출처: CPython Lib.
14. **모듈 안 순환을 허용한다면 모듈은 얼마나 커도 되는가.** 자료가 없다(d3).
15. **모듈 수준 로거(`logging.getLogger(__name__)`) 같은 비공개 모듈 전역은 "상수는 클래스 속성으로" 규칙에서 어떻게 다루는가(d2).** 출처: Logging HOWTO; Google pyguide.

## 추가 출처 (7장 참고문헌에 없는 것)

- Schlawack 2015. Schlawack, H. Testing & Packaging (2015-10-19, 2021-01-04 갱신). https://hynek.me/articles/testing-packaging/
- Seddon 2018. Seddon, D. (2018-07-22). Meet Layer Linter (Import Linter 로 대체됨). https://seddonym.me/2018/07/22/introducing-layer-linter/
- Seddon 2018b. Seddon, D. (2018-09-16). Rocky River 패턴 글. https://seddonym.me/2018/09/16/rocky-river-pattern/
- Jaeger 2024. Jaeger, F. (2024-01-05). Kraken Engineering, 린팅과 포매팅 글. https://engineering.kraken.tech/news/2024/01/05/linting-and-formatting.html
- grimp docs. grimp 3.17 (2026-09-04) usage, CHANGELOG. https://github.com/python-grimp/grimp/blob/main/docs/usage.rst ; https://github.com/python-grimp/grimp/blob/main/CHANGELOG.rst
- deply. Vashkatsi/deply (클래스 단위 층, 기준선, 에이전트용 위반 지문). https://github.com/Vashkatsi/deply
- tach FAQ. https://github.com/tach-org/tach/blob/main/docs/usage/faq.md
- Flask app factories. Pallets. Application Factories. https://flask.palletsprojects.com/en/stable/patterns/appfactories/
- Sans-I/O. https://sans-io.readthedocs.io/
- Buczyński 2020. Buczyński (2020-04-13). `utils` 모듈 이름 비판 글, breadcrumbscollector.tech. https://breadcrumbscollector.tech/stop-naming-your-python-modules-utils/
- Ajmani 2015. Ajmani (2015-02-04). Go 블로그, 패키지 이름 글. https://go.dev/blog/package-names
- PEP 423. Deferred, 비핵심 저자, 배포·프로젝트 이름에 관한 문서. https://peps.python.org/pep-0423/
- What's New 3.5. https://docs.python.org/3/whatsnew/3.5.html
- What's New 3.7. https://docs.python.org/3/whatsnew/3.7.html
