## 4. 실무의 구조 설계와 대규모 경험

이 장은 실무자와 대규모 조직이 모듈 경계를 어디에 긋고 어떻게 지켜 왔는지 다룬다. 근거는 대부분 전문가 경험이고 실증은 상관 연구에 머물며, 분해 방식끼리 결과를 비교한 통제 연구는 찾지 못했다. ln-structure 에 대한 함의는 별도 장에서 다룬다.

### 4.1 무엇을 따라 나눌 것인가: 변동성, 도메인, 기능, 기술 역할

가장 강한 입장은 Löwy 의 변동성 기반 분해(volatility-based decomposition)다. "Decompose based on volatility"(변동성을 따라 분해하라), 곧 변경 가능성이 있는 영역을 서비스 안에 가두라는 것이다(Löwy 2019). 그는 기능 분해(functional decomposition)는 물론 도메인 분해도 "functional decomposition in disguise"(변장한 기능 분해)라며 거부하고, "There should never be direct mapping between the requirements and the design"(요구사항을 설계에 직접 대응시키지 말라)고 한다. 근거는 컨설팅 경험과 유추이며(근거: 전문가 의견), 그 자신도 "volatility is often not self-evident"(변동성은 흔히 자명하지 않다)고 인정한다.

Evans 는 도메인 개념을 축으로 삼아 "Choose modules that tell the story of the system and contain a cohesive set of concepts"(시스템의 이야기를 들려주는 응집된 개념 묶음을 모듈로 고르라)고 하고, 결합도와 응집도를 "mechanically"(기계적으로) 판정하는 것을 경계한다(Evans 2015). 그러면서도 리팩터링을 거듭하며 "axes of change and stability"(변경과 안정의 축)를 관찰해 개념 윤곽(Conceptual Contours)을 찾으라 하여 변경을 증거로 쓴다. 이름은 "without reference to the means"(수단을 언급하지 않고) 효과와 목적을 말해야 한다(근거: 전문가 의견).

패키지 구성 논쟁은 같은 질문을 코드 배치로 옮긴다. Bogard 의 수직 슬라이스(vertical slice)는 요청 단위로 묶어 "Minimize coupling between slices, and maximize coupling in a slice"(슬라이스 사이 결합은 줄이고 안의 결합은 키우라)를 따른다(Bogard 2018). Brown 의 컴포넌트별 패키지(package by component)는 한 개념의 업무 논리와 데이터 접근을 공개 인터페이스 뒤에 묶되, 요점은 강제다. "If you make all types public, architectural styles can be conceptually different, but syntactically identical"(모든 타입을 공개하면 구조 양식이 문법상 같아진다)이므로 공개 면적을 설계 의도에 맞추고 컴파일러로 강제하라는 것이다(Brown 2015; 2018). Knoernschild 는 "Classes changing at the same rate and typically reused together belong in the same module"(같은 속도로 변하고 함께 재사용되는 클래스는 한 모듈에)을 기준으로 두고, 재사용을 키울수록 쓰기 어려워지므로 잘게 나눈 모듈 위에 파사드(facade)를 둔다(Knoernschild 2012)(근거: 모두 전문가 의견).

이 입장들은 충돌하면서도 변경에서 만난다. Löwy 가 거부하는 도메인 분해를 Evans 는 권하고, Bogard 의 요청 단위 슬라이스는 요구사항을 설계에 대응시키지 말라는 Löwy 와 어긋난다. 그러나 Löwy, Evans, Knoernschild 모두 **변경을 경계의 판정 기준**으로 쓰고, 대부분 기술 역할을 묶음 기준에서는 내리되 의존 방향 제약으로는 남긴다. 같은 층 의존은 Löwy 의 방법이 Engine 끼리처럼 같은 역할끼리의 옆 호출을 깊이와 무관하게 막고(Raj 2025; SoByte 2021 [2차 출처], 두 요약은 금지 목록 한 항목에서 어긋난다) Evans 2003 은 허용하며[2차 출처] Knoernschild 는 수준이 다르면 허용한다. 패키지 방식을 비교한 연구는 없다. 가까운 것은 공변경(co-change) 클러스터 1,802개를 디렉터리와 대조한 연구로, 한 디렉터리에 감싸인 클러스터는 잘 정의된 관심사를 구현하는 경향이, 여러 디렉터리로 뻗은 문어형은 파급 효과와 유의한 관련이 있었다(Silva et al. 2019)(근거: 실증, GitHub 오픈소스, 상관). 다만 프로젝트 수가 초록(133)과 본문(123)에서 어긋나고 분해 축을 비교하지는 않는다.

### 4.2 판단과 입출력의 분리: 포트와 어댑터, 함수형 코어, Sans-I/O

두 번째 축은 결정하는 코드와 입출력하는 코드를 가르는 것이다. 포트와 어댑터(Ports and Adapters), 곧 육각형 구조(Hexagonal Architecture)는 애플리케이션을 실제 장치와 데이터베이스 없이 개발·시험하게 하려 한다(Cockburn 2005). "A port identifies a purposeful conversation"(포트는 목적 있는 대화를 가리킨다)이고, 구역은 안과 밖 둘뿐이며 안쪽 구조는 규정하지 않는다(Cockburn & Garrido de Paz 2024). 포트는 애플리케이션이 소유한다. 구동되는(driven) 포트는 애플리케이션이 요구하는 인터페이스라서 "database depends on the application"(데이터베이스가 애플리케이션에 의존하는) 구조가 되고, 포트마다 시험용을 포함해 어댑터를 둘 이상 두며, 고르는 일은 시작 시점에 구성자(configurator), 흔히 `main` 이 한다(Garrido de Paz 2018). 안쪽은 기술에서 자유로울 뿐 효과에서 자유롭지는 않아 예제 코어도 계산 도중 포트를 부른다. 인터페이스를 선언하지 않는 Ruby 예제에는 포트가 어디 있는지 보기 어렵다는 주석이 붙는다(Cockburn & Garrido de Paz 2024). 양파 구조(Onion Architecture)는 "all coupling is toward the center"(모든 결합은 중심을 향한다)를 공유하되 이름 붙은 동심원 층과 의존성 역전(dependency inversion)을 더한다(Palermo 2008; 2013)(근거: 전문가 의견).

함수형 코어, 명령형 셸(Functional Core, Imperative Shell)은 결정을 모두 순수한 코어에 넣고, 셸은 코어가 낸 값대로 입출력하는 얇은 접착층으로 두며, 구성 요소 사이 경계를 값으로 삼는다(Bernhardt 2012a; 2012b). Seemann 은 "a pure function can't invoke an impure activity"(순수 함수는 불순한 활동을 부를 수 없다)를 법칙으로 두고(Seemann 2018), 읽기, 순수 계산, 쓰기의 샌드위치(impureim sandwich)를 기본형으로 제시한다(Seemann 2020). 코어가 바깥을 부르지 않으니 구동되는 쪽 인터페이스가 필요 없고, 그는 이를 의존성 거부(dependency rejection)로 도달한 포트와 어댑터라 부른다(Seemann 2016; 2017). 다만 그는 이 방식이 언제나 가능하지는 않다고 밝히며, 읽을 것이 중간 결정에 달렸거나 데이터가 너무 커 미리 읽을 수 없으면 다른 구조로 간다(Seemann 2025)(근거: 형식 논증, 전문가 의견).

Sans-I/O 는 이 분리를 프로토콜 라이브러리 전체에 적용한다. 구현은 "contains no code that does any form of network I/O or any form of asynchronous flow control"(네트워크 입출력과 비동기 흐름 제어 코드를 담지 않는다)이고, 메모리 입출력은 실패하지 않으므로 시험이 결정적이다(Benfield 2016). Python 의 h11 이 이 방식이고(Smith 2025), Rust 의 quinn 은 입출력 없는 상태 기계 quinn-proto 를 아래, tokio 기반 API 를 위 크레이트로 둔다(quinn n.d.). Rust 실무는 시간도 입력으로 받는다("str0m never calls `Instant::now()` itself")(str0m n.d.). Firezone 은 그 덕에 CI 마다 수천 개의 결정적 시나리오를 돌리지만, 순차 흐름에 코드가 더 들고 의존 라이브러리가 몰래 시계를 읽어 부분적으로 불순했다고 보고한다(Eizinger 2024)(근거: 실무 보고, 비교군 없음). 반론은 상태 기계를 컴파일러에 맡기는 비동기의 이점을 호환성 때문에 버린다는 것이다(Munns & Wenger 2025).

이 접근들은 코어가 기술적인 것을 import 하지 않고, 코어와 입출력을 묶는 코드가 그 위에 있으며, 연결은 "As close as possible to the application's entry point"(진입점에 최대한 가깝게) 두는 조합 루트(Composition Root)에서 한다는 데 합의한다. 조합 루트는 애플리케이션에만 두고 라이브러리에는 두지 않는다(Seemann 2011). 갈리는 것은 인터페이스다. 육각형과 양파는 구동되는 협력자마다 코어가 소유한 인터페이스로 의존을 역전하고, 함수형 코어와 Sans-I/O 는 값을 돌려주어 역전 없이 경계를 짓는다. 비판은 격리보다 수단을 겨눈다. 시험을 위한 분리가 "needless indirection and conceptual overhead"(쓸데없는 간접화와 개념 부담)를 낳고(Heinemeier Hansson 2014), 모의 객체(mock)와 경직된 의존 규칙에 기댄다는 것이다(Bogard 2018). 잘 뒷받침되는 것은 **순수 코어를 입출력 없이 결정적으로 시험할 수 있다**는 것뿐이다. 유일한 실증은 단일 저자 사전 인쇄본의 예비 연구로, 엄격한 육각형 제약에서 구조 위반율이 GPT-5.1 은 0%, Llama 3 8B 는 80% 였다(Slater 2025, 표본 크기 미공개). 또 import 관계는 순수성을 드러내지 않는다. Haskell 밖에서는 순수성 확인에 고된 분석이 들고(Seemann 2018), 표준 라이브러리 소켓을 감싼 모듈은 순수 코어만큼 낮게 놓일 수 있다.

### 4.3 물리 설계와 수준화(levelization): 층은 의존에서 계산된다

Lakos 는 클래스와 그 관계를 다루는 논리 설계와, 파일·디렉터리·라이브러리 사이의 분할, 의존, 컴파일·링크 결합, 순환을 다루는 물리 설계를 나눈다(Lakos 1996 [2차 출처]). 물리 단위는 헤더, 구현, 테스트 드라이버로 된 컴포넌트(component)이고 의존은 `#include` 그래프에서 읽는다. 수준(level)은 계산된다. 외부 코드가 수준 0, 지역 의존이 없는 컴포넌트가 수준 1, 그 위는 의존 대상의 최고 수준에 1을 더한 값, 곧 외부까지의 최장 경로다(Lakos 1996 [2차 출처]). Bloomberg 의 BDE 표준은 순환 없는 계층을 "levelizable"(수준화 가능)이라 부른다(Bloomberg 2026). 정의에서 곧바로 따르듯(형식 논증) 의존 A→B 는 A 를 B 보다 적어도 한 수준 위에 두므로 **같은 수준끼리의 의존은 정의상 불가능**하고, 더 낮은 어느 수준으로든 건너뛸 수 있다. 실제 구속 조건은 비순환성이고 수준은 그 결과 붙는 이름표이며, BDE 는 수준을 이름이나 경로에 넣지 않는다(Bloomberg 2022). 그래서 같은 층 의존 금지는 계산된 수준에서는 비순환성 이상의 제약이 아니고, 배정된 개념 층에서만 별도 제약이 된다.

주장된 이점은 계층적 시험이다. 각 수준에서 더해진 가치만 시험하면 되고(Lakos 1996 [2차 출처]), BDE 는 이미 시험된 것에만 기대어 차례로 시험할 수 있도록 시험 코드의 include 도 순환을 만들지 못하게 한다(Bloomberg 2026). 결합은 누적 컴포넌트 의존도(CCD, Cumulative Component Dependency), 곧 각 컴포넌트를 시험하는 데 필요한 컴포넌트 수의 합으로 재며, 이 값은 깊은 사슬과 순환에서 커진다[2차 출처].

순환을 끊는 기법은 아홉이다. 올리기(Escalation), 내리기(Demotion), 불투명 포인터, 멍청한 데이터(Dumb Data), 중복(Redundancy), 콜백(Callbacks), 관리자 클래스, 인수분해(Factoring), 캡슐화 올리기다(Lakos 2016). 올리기는 "Moving mutually dependent functionality higher in the physical hierarchy"(서로 의존하는 기능을 위로 옮긴다)로, 상호 의존 부분만 새 상위 컴포넌트로 뽑아 원래 둘을 같은 수준에서 독립시킨다. 내리기는 공통 기능을 아래로 옮기고, 중복은 결합을 피하려 재사용을 포기한다. 1996년 판은 콜백의 필요가 "a symptom of a poor overall architecture"(나쁜 전체 구조의 증상)일 수 있다고 경고하면서도 프로토콜 클래스를 "a nearly perfect insulator"(거의 완벽한 절연체)라 부르고[2차 출처], 2016년 강연은 추상 인터페이스 콜백 예제에 "Extensible!"을 단다. 기법 사이 순위는 없다(근거: 전문가 의견, 예제).

규칙은 적고 단단하다. 필수 규칙은 "No Cyclic Physical Dependencies! No Long-Distance Friendships!"(물리적 순환 금지, 원거리 friend 금지)다(Lakos 2016). BDE 는 외부에 쓰이는 클래스마다 별도 컴포넌트를 두고 friend, 순환 회피, 단일 해법, 큰 것에 딸린 작은 것(flea on an elephant)일 때만 함께 두며, 패키지 이름공간에는 클래스, swap 함수, 연산자만 두고 나머지 함수는 `…Util` 클래스에 넣는다. 쓰는 헤더는 전이 포함에 기대지 않고 직접 포함한다. 패키지 안 의존은 include 에서 추론하되 패키지 사이에 허용된 의존은 메타데이터로 선언한다(Bloomberg 2026; Lakos 2016). 하위 헤더를 물리적으로 숨기는 방식은 구조와 배포를 뒤섞고 숨긴 컴포넌트의 재사용을 막는다며 거부한다(Lakos 2016).

Knoernschild 는 같은 번호 매기기를 Java 모듈에 옮기며 "a single layer may contain multiple module levels"(한 층에 여러 수준이 있을 수 있다)고 개념 층과 수준을 나누고, 바로 아래만 부르는 엄격한 방식은 "pragmatically difficult"(실무상 어렵다)며 위반은 빌드 실패로 막는다(Knoernschild 2012). Lakos 의 근거는 30년 넘는 경험과 그래프 논증이고(근거: 형식 논증, 전문가 의견), **수준화 자체의 이점을 시험한 실증은 찾지 못했다**. 가까운 상관 연구에서 순환 그래프 크기는 결함 경향과 일관되게 상관했고, 순환 사이를 오가는 컴포넌트는 결함 확률이 높았으며, 릴리스 사이 체계적 순환 제거는 없었다(Oyetoyan et al. 2013; 2014 [2차 출처])(근거: 실증, Eclipse·ActiveMQ 등, 상관). 링크·컴파일 시간이라는 정량적 동기는 C++ 고유이고, 의존 구조 행렬(DSM) 연구는 일부 일탈을 "conscious design tradeoffs"(의식적 설계 절충)로 인정한다(Sangal et al. 2005). Lakos 의 2019년 책도 층 구조의 "heaviness"(무거움)를 피하는 옆으로 펼친(lateral) 설계를 권하나 그 정의는 확인하지 못했다(Lakos 2019).

### 4.4 책임이 잘못 놓였다는 신호: 냄새와 검출

책임 배치의 오류는 냄새(smell)로 드러난다. 냄새는 "a surface indication that usually corresponds to a deeper problem in the system"(대개 더 깊은 문제에 대응하는 표면의 징후)이지만 그 자체로 나쁜 것은 아니다("smells aren't inherently bad on their own")(Fowler 2006). 책임과 직결되는 것은 한 모듈이 "changed in different ways for different reasons"(서로 다른 이유로 다르게 바뀌는) 발산 변경(Divergent Change)과, 변경 하나가 여러 모듈을 건드리는 산탄총 수술(Shotgun Surgery)이다(Fowler 2018 [2차 출처]). 앞의 것을 지나치게 고치면 뒤의 것이 되고(Refactoring.Guru n.d. [2차 출처]), 처방도 클래스 추출과 인라인, 위임 숨기기와 중개자 제거처럼 서로 역인 쌍이라(Fowler n.d.) 방향은 맥락이 정한다(근거: 전문가 의견). 설계 냄새 중에는 다면 추상화(Multifaceted Abstraction, "more than one responsibility assigned to it", 책임이 둘 이상), 멤버가 흩어진 깨진 모듈화, 순환·허브형 모듈화, 쓰이지 않는 추상화, 구현 세부가 공개 인터페이스로 새는 누수 캡슐화(Leaky Encapsulation)가 책임과 관련된다(Suryanarayana et al. 2014). 구조 냄새로는 한 관심사를 여러 컴포넌트가 나눠 맡으며 각자 다른 관심사도 맡는 흩어진 기생 기능, 범용 진입점 하나가 정적 의존 분석을 무력화하는 모호한 인터페이스(Ambiguous Interfaces)가 있다(Garcia et al. 2009).

무엇을 냄새로 볼지부터 갈린다. Garcia 등은 냄새를 늘 절충으로 보고 이력 없이 검출한다고 보지만, Mo 등(2021)은 예측력이 가장 큰 패턴에 변경 이력이 필요하다고 본다. 높은 진입·진출 차수에 공변경이 겹친 교차(Crossing)는 단일 책임 원칙을 따르지 않을 가능성이 높고 불안정 인터페이스와 함께 영향이 가장 컸으며, 패키지 순환은 영향이 작았다. 검출 도구는 정의가 비형식적이라 서로 결과가 다르고(Arcelli Fontana et al. 2012), 믿을 만한 추천기는 최종 판단을 설계자에게 맡긴다(Tsantalis & Chatzigeorgiou 2009). 개발자가 응집도·결합도의 최적 균형을 추구한다는 실증 근거도 없다(Candela et al. 2016). 대형 언어 모델(LLM)의 Move Method 제안은 날것 그대로면 최대 80% 가 환각이라 정적 분석으로 걸러야 했고(MM-assist 2025), 탐색 범위를 좁히자 ChatGPT 의 리팩터링 기회 식별률이 15.6% 에서 86.7% 로 올랐다(Liu et al. 2025). 에이전트 리팩터링 15,451건은 저수준 일관성 정리가 주였다(Horikawa et al. 2025)(근거: 실증, 주로 Java).

영향의 실증은 상관 연구이고 크기 교란을 두고 갈린다. 30개 프로젝트 395개 릴리스에서 냄새 있는 클래스는 변경과 결함에 더 취약했고(Palomba et al. 2018), 냄새는 대부분 코드가 처음 만들어질 때 들어와 약 80% 가 살아남았다(Tufano et al. 2015 [2차 출처]). 반면 크기로 정규화하면 God 클래스가 덜 바뀌고 결함도 적었고(Olbrich et al. 2010), 전문 개발자 6명의 유지보수에서 12개 냄새 어느 것도 파일 크기와 변경 수를 보정하면 노력 증가와 유의하게 관련되지 않았다(Sjøberg et al. 2013). 구조 수준에서는 Java 31개 시스템 커밋의 87% 가 냄새 있는 산출물을 더 많이 바꿨고(Sas et al. 2022a), 산업 C/C++ 9개 프로젝트에서 순환은 허브 같은 복잡한 구조의 촉매였으며 냄새 분석은 식별보다 감시에 유용했다(Sas et al. 2022b). 순환의 위치나 종류로는 해로운 순환을 가를 수 없었고(Oyetoyan et al. 2015), 대부분의 순환은 패키지 안에 머물러 치명적이지 않을 수 있다(Al-Mutawa et al. 2014).

| 필요한 정보 | 검출할 수 있는 냄새 |
|---|---|
| 모듈 import 그래프 | 순환, 허브, 불안정 의존, 쓰이지 않는 모듈, 층·API 우회 |
| 여기에 상속 간선·크기 | 건강하지 않은 상속 계층, God Component |
| 구문 트리·호출 그래프 | Feature Envy, Message Chains, Middle Man, 누수 캡슐화 |
| 의미 정보나 변경 이력 | 발산 변경, 다면 추상화, 관심사 분산, 산탄총 수술, 교차 |

이 표(Mo et al. 2021; Le et al. 2021 을 바탕으로 종합)대로라면 import 그래프 도구는 목록의 대략 3분의 1을 덮고, 단일 책임이 겨냥하는 **변경과 의미로 정의된 냄새는 보지 못한다**. 높은 차수나 모듈 안 클래스 군집 같은 구조 대용치는 증거일 뿐이며 사람의 판단과 대조해 검증된 적이 없다.

### 4.5 대규모 조직의 경계 강제: 구조를 지키지만 만들지는 못한다

Google 은 경계를 빌드 시스템으로 강제한다. 출발점은 Hyrum 의 법칙, 곧 사용자가 충분히 많으면 "all observable behaviors of your system will be depended on by somebody"(관찰 가능한 모든 동작에 누군가 의존한다)는 것이다(Winters et al. 2020, 1장). 그래서 "A visibility is essentially the opposite of a dependency"(가시성은 본질적으로 의존의 반대다)로 보고 가시성을 최소화하며, Bazel 의 기본 가시성은 비공개다(Winters et al. 2020, 18장; Bazel n.d.). 바깥 방향으로는 직접 선언하지 않은 의존의 기호를 참조하면 막는 엄격 의존(strict deps)과 C++ `layering_check` 가 있다(Bazel 2020). 도입 전에는 전이 의존이 공개 계약에 섞여 안전하게 바꿀 수 없었다. 선언은 "a one-time cost"(한 번의 비용)이지만 암묵적 전이 의존은 계속 문제를 낳는다고 보며, 디렉터리마다 BUILD 파일이 하나인 잘게 나눈 모듈의 관리 비용은 도구로 흡수한다(Winters et al. 2020, 18장)(근거: 전문가 의견, 결과 자료 비공개).

Shopify 의 기록은 강제가 빗나가는 방식을 보여 준다. 클래스를 주문, 배송, 재고 같은 현실 개념으로 나눠 컴포넌트마다 공개 API 와 데이터 소유를 주려 했으나(Westeinde 2019), 2020년 컴포넌트 37개 모두가 나머지 절반 이상에 의존했다. 처방은 책임을 그것에 의존하는 컴포넌트로 옮기거나 제어를 역전하는 것이었다. 그래프를 무시하고 만든 공개 인터페이스는 덧붙은 간접층일 뿐이었고, 규정된 패턴은 개발자가 "redefine their problem to fit the solution"(해법에 맞게 문제를 재정의)하게 했다(Müller 2020). 2024년 회고에 따르면 공개 API 만 부르게 한 비공개 검사(privacy check)는 도구를 "an API design tool"(API 설계 도구)로 바꿔 문서 없는 공개 코드를 늘렸고 3.0 에서 제거되었다. 의미 단서에 기대어 나눈 패키지는 실제 실행과 어긋났고 상수로 참조되지 않는 의존은 보이지 않았다. 무시 목록은 기능마다 커졌고 보고 속도가 고칠 수 있는 속도를 앞질렀으며 고침은 "unnatural and overly complicated"(부자연스럽고 지나치게 복잡)했다. 성공은 위반과 의존이 0인 기반 패키지 하나였다. 권고는 패키지 배치를 실제 의존에 맞추고 "running code, more than any metric"(어떤 지표보다 실행되는 코드)으로 진척을 재라는 것이다(McGibbon & Salzberg 2024)(근거: 실무 보고, 정량 자료 없음).

Microsoft 연구는 가장 정량적이지만 모두 Windows 의 상관 연구다. Windows Server 2003 에서는 바이너리 의존 그래프 지표가 복잡도 지표보다 결함을 잘 예측했고(재현율 10%포인트 차) 큰 클리크에 속할수록 결함이 많았으나, 저자들은 다른 제품에 일반화하지 않는다(Zimmermann & Nagappan 2008). Windows Vista 바이너리 3,404개에서는 조직 지표(정밀도 86.2%, 재현율 84.0%)가 층 정보를 포함한 의존 지표(74.4%, 69.9%)를 앞섰다(Nagappan, Murphy & Basili 2008). Windows 7 의 다년간 층 정비에서 규칙은 "modules at level n can depend only on the modules of level n− 1 and below only"(수준 n 은 n−1 이하에만 의존)였고 위반 커밋은 품질 관문(quality gate)이 막았으나 층 안의 무해한 순환은 따로 구분했다. 팀들은 API 계열마다 빈 헤더 모듈을 두고 구성 시점에 구현에 묶었다. 정비된 상위 5% 모듈의 모듈 간 의존은 0.85배로 줄었지만(나머지 1.10배, p = 0.000022) 결함 감소를 리팩터링 덕으로 돌릴 수 없었고 그 모듈들은 오히려 커졌다(Kim, Zimmermann & Nagappan 2014)(근거: 실증, 인터뷰 6건·설문 328명·버전 이력, 상관).

GitLab 은 주된 어려움이 "organizational, rather than technical"(기술이 아니라 조직)이고 "Data coupling is what actually blocks extraction"(분리를 막는 것은 데이터 결합)이라 진단하며(GitLab 2023), 너무 잘게 나눈 경계 맥락은 얕아지고 더 결합된다고 경고한다(GitLab n.d.). 찾은 산업용 층 검사기(Windows, packwerk-extensions, Nx)는 모두 배정된 층을 쓰고 같은 층 안의 의존을 허용한다(rubyatscale n.d.; Nx n.d.). 종합하면 기계적 강제는 고른 구조를 **보존**하는 데는 믿을 만하지만 좋은 책임 분리를 **만들어 낸다**는 것을 보인 출처는 없다. 의미로 그은 경계를 의존 방향보다 먼저 강제하자 간접층, 공개 코드 팽창, 줄지 않는 위반 목록이 나왔고, 좋은 분리 자체는 어디서도 측정되지 않았다.

### 참고문헌 (4장)

표시: 표시 없음은 원문 확인, [초록만 확인]은 공식 초록·서지만 확인, [2차 출처]는 요약이나 제3자 기록으로만 확인, [미확인]은 문구를 확인하지 못함. 제목이 노트에 없는 논문은 학회·권호·DOI 로 식별한다.

- Al-Mutawa et al. (2014). [제목 미기재]. ASWEC 2014. https://doi.org/10.1109/ASWEC.2014.15 [초록만 확인]
- Arcelli Fontana et al. (2012). [제목 미기재]. *Journal of Object Technology* 11(2). https://doi.org/10.5381/jot.2012.11.2.a5 [초록만 확인]
- Arcelli Fontana et al. (2019). [제목 미기재]. *Journal of Systems and Software* 154. https://doi.org/10.1016/j.jss.2019.04.066 [2차 출처: Sas, Avgeriou & Uyumaz 2022 경유]
- Bazel (n.d.). "Visibility". Bazel 문서. https://bazel.build/concepts/visibility
- Bazel (2020). 커밋 8b9f746, "Add layering check support to cc_configure on Linux with Clang". https://bazel.googlesource.com/bazel/+/8b9f74649512ee17ac52815468bf3d7e5e71c9fa
- Benfield, C. (2016). "Writing I/O-Free (Sans-I/O) Protocol Implementations". https://sans-io.readthedocs.io/how-to-sans-io.html (저자는 저장소 커밋 이력으로 확인)
- Bernhardt, G. (2012a). "Boundaries". SCNA 2012, RubyConf 2012 발표. https://www.destroyallsoftware.com/talks/boundaries (녹취록 https://www.rubyevents.org/talks/boundaries 은 구두점 없는 제3자 녹취로 영상과 대조하지 않음)
- Bernhardt, G. (2012b). "Functional Core, Imperative Shell". Destroy All Software 스크린캐스트. https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell [유료, 설명문만 확인]
- Bloomberg (2022). "BDE-Style Repository". BDE Build Tools 문서. https://bloomberg.github.io/bde-tools/bbs/reference/bde_repo_layout.html
- Bloomberg (2026). *BDE C++ Coding Standards* (2026-03-02 판). https://bloomberg.github.io/bde/knowledge_base/coding_standards.html
- Bogard, J. (2018). "Vertical Slice Architecture". https://www.jimmybogard.com/vertical-slice-architecture/
- Brown, S. (2015). "Package by component and architecturally-aligned testing". codingthearchitecture.com, DZone 재게시. https://dzone.com/articles/package-component-and
- Brown, S. (2018). "Modular Monoliths". GOTO Berlin 2018 발표 슬라이드. https://files.gotocon.com/uploads/slides/conference_12/515/original/gotoberlin2018-modular-monoliths.pdf
- Candela, Bavota, Russo & Oliveto (2016). "… Is It Enough?"(제목 일부). *ACM TOSEM* 25(3). https://doi.org/10.1145/2928268 [초록만 확인]
- Cockburn, A. (2005). "Hexagonal architecture"(Ports and Adapters). HaT Technical Report 2005.02. https://alistair.cockburn.us/hexagonal-architecture/
- Cockburn, A. & Garrido de Paz, J. M. (2024). *Hexagonal Architecture Explained*. Humans and Technology Press. ISBN 978-1-7375197-8-2. 부속 PDF: https://alistaircockburn.com/code%20hexarch%20book%20v0.9a.pdf , https://alistaircockburn.com/figs%20hexarch%20book.pdf [책 본문 미열람, 공식 부속 PDF 만 확인]
- Eizinger, T. (2024). "sans-IO: The secret to effective Rust for network services". Firezone blog. https://www.firezone.dev/blog/sans-io
- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley. ISBN 0-321-12521-5 [2차 출처: 본문 미열람, 같은 층 의존 허용 문구는 독자 하이라이트 https://www.goodreads.com/notes/18994167-domain-driven-design/126162962-ricardo/d7dfb14b-afe1-4a37-b5d4-a76fb46288ea 로만 확인]
- Evans, E. (2015). *Domain-Driven Design Reference: Definitions and Pattern Summaries*. Domain Language, Inc. https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
- Fowler, M. (2006). "CodeSmell". martinfowler.com bliki. https://martinfowler.com/bliki/CodeSmell.html
- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* 2판, 3장 "Bad Smells in Code"(K. Beck 공저). Addison-Wesley. https://www.oreilly.com/library/view/refactoring-improving-the/9780134757681/ch03.xhtml [2차 출처: 원문 열람 실패, 인용은 Iteration 팟캐스트 요약(2019) https://dev.to/iteration-podcast/bad-smells-in-code 경유. 산탄총 수술의 2판 문구는 미확인]
- Fowler, M. (n.d.). Refactoring catalog. https://refactoring.com/catalog/
- Garcia, Popescu, Edwards & Medvidovic (2009). [제목 미기재]. QoSA 2009, LNCS 5581, pp. 146–162. https://doi.org/10.1007/978-3-642-02351-4_10 (PDF https://jgarcia.ics.uci.edu/wp-content/uploads/10.1.1.183.9958.pdf)
- Garrido de Paz, J. M. (2018). "Hexagonal Architecture: Ports and Adapters Pattern". https://jmgarridopaz.github.io/content/hexagonalarchitecture.html
- GitLab (2023). "Rails Monolith Decomposition"(모듈식 모놀리스 설계 문서, 제안 상태). https://gitlab.com/gitlab-com/content-sites/handbook/-/raw/main/content/handbook/engineering/architecture/design-documents/modular_monolith/_index.md
- GitLab (n.d.). "Software design" 개발 문서. https://docs.gitlab.com/development/software_design/
- Heinemeier Hansson, D. (2014). "Test-induced design damage". https://dhh.dk/2014/test-induced-design-damage.html
- Horikawa et al. (2025). [제목 미기재, 에이전트 리팩터링 실증]. arXiv:2511.04824. https://arxiv.org/abs/2511.04824 [초록만 확인]
- Kim, M., Zimmermann, T. & Nagappan, N. (2014). "An Empirical Study of Refactoring Challenges and Benefits at Microsoft". *IEEE Transactions on Software Engineering*. https://thomas-zimmermann.com/publications/files/kim-tse-2014.pdf
- Knoernschild, K. (2012). *Java Application Architecture: Modularity Patterns with Examples Using OSGi*. Prentice Hall. 저자 요약: DZone Refcard #166 "Patterns of Modular Architecture", https://dzone.com/refcardz/patterns-modular-architecture [책 본문 미열람, 저자 요약 카드로 확인]
- Lakos, J. (1996). *Large-Scale C++ Software Design*. Addison-Wesley. ISBN 0-201-63362-0 [2차 출처: 원문 미열람. V. Huston 노트 http://www.vincehuston.org/cpp/largeScaleCpp.html , G. Zheng 노트 https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/ , D. Stotts 강의 페이지 https://www.cs.unc.edu/~stotts/COMP204/lakos/major.html 경유]
- Lakos, J. (2016). "Large-Scale C++: Advanced Levelization Techniques". CppCon 2016 발표 슬라이드. https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf
- Lakos, J. (2019). *Large-Scale C++ Volume I: Process and Architecture*. Addison-Wesley. ISBN 978-0-201-71706-8. https://www.informit.com/store/large-scale-c-plus-plus-process-and-architecture-volume-9780201717068 [목차와 출판사 설명만 확인]
- Le et al. (2021). [제목 미기재, 구조 냄새 11종과 이슈·변경 경향]. arXiv:2102.09835. https://arxiv.org/abs/2102.09835
- Liu et al. (2025). [제목 미기재, LLM 리팩터링 기회 식별]. *Automated Software Engineering* 32 (arXiv:2411.04444). https://arxiv.org/abs/2411.04444 [초록만 확인]
- Löwy, J. (2019). *Righting Software: A Method for System and Project Design*. Addison-Wesley. ISBN 978-0-13-652403-8. 2장 표본 "Software System Decomposition": https://www.informit.com/articles/article.aspx?p=2995357 [2장 표본만 원문 확인, 3장은 Raj 2025 와 SoByte 2021 경유]
- McGibbon, G. & Salzberg, C. (2024). "A Packwerk Retrospective". Rails at Scale. https://railsatscale.com/2024-01-26-a-packwerk-retrospective/
- MM-assist (2025). [저자·제목 미기재, LLM Move Method 추천]. ICSME 2025. https://doi.org/10.1109/ICSME64153.2025.00046 [초록만 확인]
- Mo, Cai, Kazman, Xiao & Feng (2021). [제목 미기재, 구조 반패턴과 오류·변경 경향]. *IEEE TSE* 47(5):1008–1028. https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf
- Müller, P. (2020). "Under Deconstruction: The State of Shopify's Monolith". Shopify Engineering. https://shopify.engineering/shopify-monolith
- Munns, J. & Wenger, A. (2025). "sans-io: meh". Self-Directed Research podcast. https://sdr-podcast.com/episodes/sans-io/
- Nagappan, N., Murphy, B. & Basili, V. (2008). "The Influence of Organizational Structure on Software Quality: An Empirical Case Study". ICSE 2008 (MSR-TR-2008-11). https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2008-11.pdf
- Nx (n.d.). "Enforce module boundaries". https://nx.dev/docs/features/enforce-module-boundaries
- Olbrich, Cruzes & Sjøberg (2010). [제목 미기재]. ICSM 2010. https://doi.org/10.1109/ICSM.2010.5609564 [초록만 확인]
- Oyetoyan, Cruzes & Conradi (2013). "Can Refactoring Cyclic Dependent Components Reduce Defect-Proneness?". ICSM 2013, pp. 420–423. https://doi.org/10.1109/ICSM.2013.62 [2차 출처: SINTEF 초록]
- Oyetoyan, Cruzes & Conradi (2014). "Transition and Defect Patterns of Components in Dependency Cycles during Software Evolution". CSMR-WCRE 2014, pp. 283–292. https://doi.org/10.1109/CSMR-WCRE.2014.6747180 [2차 출처: SINTEF 초록]
- Oyetoyan, Falleri, Dietrich & Ježek (2015). "Circular dependencies and change-proneness: An empirical study". SANER 2015. https://doi.org/10.1109/SANER.2015.7081834 [초록만 확인. 노트 하나는 검색 초록으로만 보고 학회명을 기억에 기댔으나, 다른 노트가 DOI 와 공식 초록으로 확인]
- Palermo, J. (2008). "The Onion Architecture: part 1". https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
- Palermo, J. (2013). "Onion Architecture: Part 4 - After Four Years". https://jeffreypalermo.com/2013/08/onion-architecture-part-4-after-four-years/
- Palomba et al. (2018). [제목 미기재]. *Empirical Software Engineering* 23(3):1188–1221. https://doi.org/10.1007/s10664-017-9535-z [초록만 확인]
- quinn (n.d.). quinn-rs/quinn README. https://github.com/quinn-rs/quinn
- Raj, U. (2025). The Method 해설 글 3편("Design don'ts", "Template" I·II). DEV Community. https://dev.to/ujjwall-r/design-donts-in-system-design-with-the-method-2jcf , https://dev.to/ujjwall-r/template-for-system-design-using-the-method-3ign , https://dev.to/ujjwall-r/template-for-system-design-using-the-method-part-ii-5d5b [2차 출처]
- Refactoring.Guru (n.d.). "Divergent Change", "Shotgun Surgery". https://refactoring.guru/smells/divergent-change , https://refactoring.guru/smells/shotgun-surgery [2차 출처]
- rubyatscale (n.d.). packwerk-extensions. https://github.com/rubyatscale/packwerk-extensions
- Sangal, Jordan, Sinha & Jackson (2005). "Using Dependency Models to Manage Complex Software Architecture". OOPSLA '05, ACM. https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf
- Sas, Avgeriou, Pigazzini & Arcelli Fontana (2022a). [제목 미기재]. JSEP 34(1). https://doi.org/10.1002/smr.2398 [초록만 확인]
- Sas, Avgeriou & Uyumaz (2022b). [제목 미기재, 산업 C/C++ 구조 냄새 혼합 연구]. arXiv:2203.08702. https://arxiv.org/abs/2203.08702
- Seemann, M. (2011). "Composition Root". https://blog.ploeh.dk/2011/07/28/CompositionRoot/
- Seemann, M. (2016). "Functional architecture is Ports and Adapters". https://blog.ploeh.dk/2016/03/18/functional-architecture-is-ports-and-adapters/
- Seemann, M. (2017). "Dependency rejection". https://blog.ploeh.dk/2017/02/02/dependency-rejection/
- Seemann, M. (2018). "Functional architecture: a definition". https://blog.ploeh.dk/2018/11/19/functional-architecture-a-definition/
- Seemann, M. (2020). "Impureim sandwich". https://blog.ploeh.dk/2020/03/02/impureim-sandwich/
- Seemann, M. (2025). "Song recommendations as a Haskell Impureim Sandwich". https://blog.ploeh.dk/2025/05/26/song-recommendations-as-a-haskell-impureim-sandwich/
- Silva, L. L., Valente, M. T. & Maia, M. A. (2019). "Co-change patterns: A large scale empirical study". *Journal of Systems and Software*. 사전 인쇄본 https://homepages.dcc.ufmg.br/~mtov/pub/2019-jss.pdf [초록·결과·위협 절만 확인, 권호·DOI 미확인]
- Sjøberg, Yamashita, Anda, Mockus & Dybå (2013). [제목 미기재]. *IEEE TSE* 39(8). https://doi.org/10.1109/TSE.2012.89 [초록만 확인]
- Slater, T. (2025). "Quantitative Analysis of Technical Debt and Pattern Violation in Large Language Model Architectures". arXiv:2512.04273 (JSS 심사 중). https://arxiv.org/abs/2512.04273 [초록만 확인]
- Smith, N. J. (2025). h11 문서 v0.16.0. https://h11.readthedocs.io/en/latest/
- SoByte (2021). *Righting Software* 독서 노트(익명). https://www.sobyte.net/post/2021-09/righting-software-notes/ [2차 출처]
- str0m (n.d.). algesten/str0m README. https://github.com/algesten/str0m
- Suryanarayana, Samarthyam & Sharma (2014). *Refactoring for Software Design Smells*. Morgan Kaufmann. 저자 포스터 https://www.slideshare.net/slideshow/design-smells-poster/60340507 [책 본문 미열람, 포스터로 확인]
- Tsantalis & Chatzigeorgiou (2009). [제목 미기재, JDeodorant Move Method]. *IEEE TSE* 35(3). https://doi.org/10.1109/TSE.2009.1 [초록만 확인]
- Tufano et al. (2015). [제목 미기재, 냄새 도입 시점]. ICSE 2015 (TSE 2017 확장). https://people.lu.usi.ch/bavotg/papers/icse2015_badSmells.pdf [2차 출처]
- Westeinde, K. (2019). "Deconstructing the Monolith: Designing Software that Maximizes Developer Productivity". Shopify Engineering. https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity
- Winters, T., Manshreck, T. & Wright, H. (편) (2020). *Software Engineering at Google*. O'Reilly. 1장(Winters) https://abseil.io/resources/swe-book/html/ch01.html , 18장 "Build Systems and Build Philosophy"(E. Kuefler) https://abseil.io/resources/swe-book/html/ch18.html
- Zimmermann, T. & Nagappan, N. (2008). "Predicting Defects using Network Analysis on Dependency Graphs". ICSE 2008. https://thomas-zimmermann.com/publications/files/zimmermann-icse-2008.pdf
