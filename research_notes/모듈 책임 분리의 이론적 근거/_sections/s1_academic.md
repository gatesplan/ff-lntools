## 2. 학술적 관점

학술 문헌은 모듈 경계를 긋는 기준으로 세 가지를 내놓았다. 바뀔 설계 결정을 하나씩 숨기는 정보 은닉, 순환 없는 사용 관계에서 계산되는 층, 모듈 안은 단단히 묶고 모듈 사이는 느슨히 잇는 결합도와 응집도다. 이후 연구는 이 기준을 의존 행렬과 변경 이력으로 재어 검증하려 했고, 어떤 단일 분해도 모든 관심사를 담지 못한다는 한계도 밝혔다. 고전의 근거는 대부분 사례와 형식 논증이고, 실증은 상관 연구이며 소수 연구 그룹과 Java·C·C++ 자료에 몰려 있다.

### 2.1 정보 은닉: 모듈은 처리 단계가 아니라 바뀔 결정 하나를 숨긴다

Parnas(1972)는 모듈을 실행 단위가 아닌 작업 배정으로 정의했다. "'module' is considered to be a responsibility assignment rather than a subprogram"(모듈은 서브프로그램이 아니라 책임 할당이다). 분해 기준은 정보 은닉(information hiding)이다. "begin with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others"(어렵거나 바뀔 만한 설계 결정의 목록에서 시작해, 모듈마다 그런 결정 하나를 다른 모듈로부터 숨기게 설계한다). KWIC 색인 예제에서 처리 단계(순서도)를 따른 분해와 정보 은닉 분해는 어셈블하면 같은 코드일 수도 있으니, **차이는 실행 코드가 아니라 작업 배정과 인터페이스에 있다.** 줄 저장 방식이 바뀌면 앞의 분해에서는 "changes in every module!"이 생기지만 뒤의 분해에서는 한 모듈만 바뀐다. 그래서 처리의 시간 순서를 분해 기준으로 쓰지 말고, 데이터 구조는 접근·수정 절차와 한 모듈에 두며, 문자 코드·정렬 순서·처리 순서도 숨기라고 한다. 근거는 장난감 예제에 대한 사고 실험과 프로젝트 경험이고(형식 논증·전문가 의견) 측정은 없으며, 바뀔 결정의 목록은 판단으로만 만든다.

Parnas, Clements & Weiss(1985)는 큰 시스템을 위해 모듈 안내서(module guide)를 더했다. 안내서는 "states only the secret of each module"(각 모듈의 비밀만 적는다). 비밀이 독립적으로 바뀔 수 있을 때만 모듈을 나누고, 나눠도 새 비밀은 생기지 않으며, 공유 비밀은 없어야 하고, 쉽게 교체될 만하면 멈춘다(Parnas 2009). A-7E 안내서는 책임을 변경 조건으로 적는다. 하드웨어 은닉 모듈은 "the procedures that need to be changed if any part of the hardware is replaced"(하드웨어 일부가 바뀌면 바뀌어야 하는 절차들)를 담고, 주 비밀(primary secret)은 하드웨어/소프트웨어 인터페이스, 그것을 숨기며 내린 구현 결정인 부 비밀(secondary secret)은 자료 구조와 알고리즘이다(Bass 외 2003; Bredereke 2002). 비밀의 트리는 누가 누구를 부를 수 있는지와 별개다. 근거는 한 시스템의 경험 보고이며, PCW 본문은 확인하지 못했다.

후기의 Parnas 는 원칙이 받아들여졌으나 잘 적용되지 않는다고 거듭 말한다. 사람들은 "'how to ....'" 형태의 비밀로 모듈마다 처리의 한 단계를 맡기고(Parnas 1994), 설계자에게 비밀을 물으면 대개 답하지 못하며, 검토하면 흩어진 비밀과 비밀 없는 모듈이 드러난다(Parnas 2009). 인터페이스는 시그니처가 아니라 가정이다. "B's interface to A is the weakest assumption about B that would allow you to prove that A is correct"(A 가 옳음을 증명하게 해 주는 B 에 대한 가장 약한 가정이 B 의 A 에 대한 인터페이스다). 명세 밖 사실에 기대는 A 는 작동하더라도 틀렸고, 서로 부르지 않아도 인터페이스는 생긴다. 인터페이스를 지킨 B 의 변경은 A 를 바꾸지 않는다는 "정보 은닉 정리"는 형식 논증이지만, 사람이 무엇을 숨길지 안다는 전제는 실증이 필요하다고 Parnas 스스로 적었고, 인터페이스 명세 없는 은닉은 "would be a disaster"라 했다. 추상 자료형(Liskov & Zilles 1974)은 표현을 비밀로 삼는 정보 은닉을 언어로 옮긴 것으로, 사용하는 모듈은 명세에만 의존한다(Liskov 2013).

Dijkstra(1974)의 관심사 분리(separation of concerns)는 단위가 다르다. 그것은 "study in depth an aspect of one's subject matter in isolation"(한 측면을 따로 깊이 연구하는 것)이되 그것이 여러 측면 중 하나임을 늘 아는 사고의 규율이고, 측면의 예는 정확성과 효율이다. 정보 은닉이 산출물의 부분을 나눈다면 관심사 분리는 생각의 측면을 나누며, 정확성처럼 모든 모듈을 가로지르는 관심사는 모듈 경계가 될 수 없다. **"관심사 하나에 모듈 하나"는 EWD447 에 없는 후대 해석이다.** 둘은 명세에서 만난다. Dijkstra 는 필요를 채우는 일을 성질을 진술하는 일과 그 성질을 보장하는 물건을 만드는 일로 나누고 명세를 둘 사이의 인터페이스로 본다.

### 2.2 층: 순환 없는 uses 관계에서 계산되지만 모듈과 같지 않다

Dijkstra(1968)의 THE 시스템은 각 층을 위층에서 무엇이 사라지는지로 정의하고 층마다 시험해 쌓았으나, 그 성과는 시험이 끝나기 전에 쓴 한 대학 프로젝트의 자가 보고다(경험 보고). Parnas(1978)는 층을 계산할 수 있는 개념으로 바꿨다. 사용(uses)은 "A uses B if correct execution of B may be necessary for A to complete the task described in its specification"(A 가 명세된 일을 마치는 데 B 의 올바른 실행이 필요할 수 있으면 A 는 B 를 사용한다)이며 호출과 다르다. B 를 부르기만 하면 명세를 채우는 A 는 B 를 사용하지 않고, 인터럽트 처리처럼 부르지 않으면서 사용할 수도 있다. 사용 그래프에 순환이 없으면 층이 정해진다. "Level 0 is the set of all programs that use no other program. Level i is the set of all programs that use at least one program on level i-1 and no program at a level higher than i-1"(0층은 다른 프로그램을 쓰지 않는 것들, i층은 i−1층의 것을 하나 이상 쓰고 그보다 높은 층은 쓰지 않는 것들). 그러면 층마다 시험하고 쓸 수 있는 부분 집합이 생기고, 제약이 없으면 "nothing works until everything works"가 된다. **순환 금지는 기계로 확인되지만 간선의 방향은 판단에 맡긴다.** A 가 B 덕에 본질적으로 단순해지고, B 가 A 를 못 써도 크게 복잡해지지 않으며, B 를 포함하고 A 는 필요 없는 유용한 부분 집합이 있고, A 를 포함하되 B 는 없는 유용한 부분 집합은 없을 때 A 가 B 를 쓰게 한다(ICSE 판. TSE 1979 판의 셋째 조건 문구는 [미확인]). 서로 쓰고 싶은 두 프로그램은 한쪽을 갈라 사이에 끼우는 샌드위치 기법(sandwiching)으로 푼다. 그는 이런 분할 대부분이 층을 곧 모듈로 여긴 데서 나왔다고 보고 "there is no correspondence between modules and levels"(모듈과 층 사이에는 대응이 없다)라 결론지었으며, "levels of abstraction"이라는 말도 대개 "an abuse of language"라 했다(정의와 형식 논증, 경험에 바탕한 의견). Habermann, Flon & Cooprider(1976)도 운영체제에서 "the concepts of module and level do not coincide"를 보였다. 메모리 관리자는 스케줄링이 필요해 두 층에 걸치지만, 두 조각이 가상 메모리 구현 지식을 공유하므로 한 모듈이다.

아키텍처 양식 문헌은 층을 설계자의 결정으로 본다. Views and Beyond(V&B)에서 층 사이 관계는 실제 사용이 아니라 허용 사용(allowed-to-use)이므로 "Layers cannot be derived by examining source code"(층은 소스 코드를 보고 도출할 수 없다). 같은 층 안의 사용은 대개 허용되고, 상위 처리기 이름을 데이터로 넘겨받는 콜백은 "upward invocation, but not uses"(위로의 호출이지 사용이 아니다)다(Bachmann 외 2000). 바로 아래 층만 쓰는 엄격한 층(strict layering)과 아래 어느 층이든 쓰는 느슨한 층(relaxed layering)은 관례의 선택이며, 느슨하면 결합이 늘어난다(Bachmann, Bass & Nord 2007). 문헌은 의미로 층을 정하는 진영(Garlan & Shaw 1993; Buschmann 외 1996; Bachmann 외 2000)과 의존 그래프에서 계산하는 진영(Parnas, Habermann 외, 2.4의 설계 규칙 위계)으로 갈린다. 앞 진영도 올바른 추상 수준을 찾기 어렵다고 인정하며(Garlan & Shaw 1993), **두 진영을 통제 비교한 연구는 없다.** 상향 호출과 층 건너뛰기를 재는 지표는 있으나(Sarkar 외 2009) 결함이나 변경 노력과 직접 연결한 연구는 찾지 못했다.

### 2.3 결합도·응집도와 1974년 한 문장 시험

Stevens, Myers & Constantine(1974)의 구조적 설계(Structured Design)는 두 척도를 세웠다. "Coupling is the measure of the strength of association established by a connection from one module to another"(결합도는 한 모듈에서 다른 모듈로의 연결이 만드는 연관의 세기다). 목적은 변경과 오류가 퍼지는 경로를 줄이는 것이다. 단일 지표 대신 인터페이스 복잡도, 연결 유형, 통신 유형을 요인으로 들고, **모듈 전체를 이름으로 가리키는 연결이 내부 요소를 가리키는 연결보다 결합이 낮다**고 한다. 공통 환경(전역, COMMON)은 공유자 모두를 서로 이어, 변수 25개를 공유하는 세 모듈에 전파 경로가 이미 150개다(계산에 의한 형식 논증). 응집은 결속(binding)이라 불렀다. "Binding is the measure of the cohesiveness of a module"(결속은 모듈의 응집 정도다)이며, 결속을 높여 결합을 줄이는 것이 목표다. 기능적 결속은 모든 원소가 "the performance of a single function"(단일 기능의 수행)에 관련된 상태이고, 기능은 "Compute Square Root"처럼 입력을 출력으로 바꾸는 변환이다. 결속은 원소 쌍마다 판정하고, 척도는 "not linear"하여 기능적 결속이 훨씬 강하다. 도출은 싣지 않았으므로 근거는 전문가 의견이다.

결속 척도는 판본마다 다르다.

| 출처 | 수준 수 | 높은 쪽부터 |
|---|---|---|
| Stevens 외 1974 | 6 | functional, sequential, communicational, temporal, logical, coincidental |
| Yourdon & Constantine 1979 (Bieman & Ott 1994 경유) | 7 | functional, sequential, communicational, procedural, temporal, logical, coincidental |
| Myers 1978 '모듈 강도(module strength)' (Card 외 1986b 경유) | 7 | functional, informational, communicational, procedural, classical, logical, coincidental |

흔히 가르치는 7단계는 Yourdon & Constantine 이 절차적(procedural) 수준을 더한 것이고, Myers 의 척도는 정보적(informational) 수준을 둔, 부분적으로 호환되지 않는 체계다. Yourdon & Constantine 에게 귀속되곤 하는 수치 가중치(0/1/3/5/7/9/10)는 [미확인]이며, 척도가 선형이 아니므로 어떤 수치화든 덧붙인 가정이다. 결합도의 이름 붙은 사다리(내용 > 공통 > 외부 > 제어 > 스탬프 > 자료)도 1974년 논문에는 없다(흔히 Myers 에게 귀속된다 [미확인]). 차이는 실질적이다. 정의대로라면 추상 자료형처럼 같은 데이터를 다루는 연산의 묶음은 Stevens 와 Yourdon & Constantine 척도에서 기능적보다 낮은 통신적(communicational) 결속이고, 이를 높이 치는 것은 Myers 의 정보적 수준뿐이다(정의 원문 [미확인]). 데이터 구조를 접근 절차와 함께 두라는 Parnas(1972)와 여기서 갈리고, 시간 순서로 묶지 말라는 점에서는 만난다.

**한 문장 시험은 1974년 논문에 이미 있다**(1999년 재수록판 p. 240). 기능적 결속인지 판단하는 유용한 기법은 "writing a sentence describing the function (purpose) of the module, and then examining the sentence"(모듈의 기능(목적)을 묘사하는 문장을 쓰고 그 문장을 살피는 것)이다. 시험은 넷이다.

| 시험 | 원문 | 뜻 | 판정 |
|---|---|---|---|
| 1 | "has to be a compound sentence, contain a comma, or contain more than one verb" | 복문이어야 하거나 쉼표나 동사가 둘 이상 필요하다 | 기능이 여럿, 순차 또는 통신적 결속 |
| 2 | "contains words relating to time, such as 'first', 'next', 'then', 'after', 'when', 'start'" | 시간을 나타내는 말이 있다 | 순차 또는 시간적 결속 |
| 3 | "the predicate of the sentence doesn't contain a single specific object following the verb" | 동사 뒤에 구체적 목적어 하나가 없다 | 논리적 결속. "Edit All Data"는 논리적, "Edit Source Statement"는 기능적일 수 있다 |
| 4 | "Words such as 'initialize', 'clean-up'" | 초기화·정리 같은 말이 있다 | 시간적 결속 |

판정마다 "probably"가 붙고 단서가 따른다. 기능적 모듈도 원소를 나열하면 언제나 복문으로 묘사되므로, "if the above language is unavoidable while still completely describing the module's function"(기능을 완전히 묘사하면서 위 표현을 피할 수 없을 때)에만 기능적이지 않을 가능성이 높다. 같은 논문의 설계 절차(p. 246)는 문장 대신 구를 쓴다. "Describe the function of each module with a short, concise, and specific phrase. Describe what transformations occur when that module is called, not how the module is implemented"(각 모듈의 기능을 짧고 간결하고 구체적인 구로 묘사하라. 어떻게 구현되는지가 아니라 불렸을 때 어떤 변환이 일어나는지를 묘사하라). 분할을 어디서 멈출지는 미해결이라 인정하면서, 따로 쓸모 있는 원소 부분 집합이 없고 구현 전체를 한 번에 파악할 만큼 작으면 충분하다고 했다. 결속이 낮은 초기화 모듈이 때로 가장 단순한 해법이라는 인정도 있다.

이 시험은 코드가 아니라 **설계자가 쓴 묘사의 문법을 읽는다.** 1과 2는 여러 단계를, 3은 일반 목적어를, 4는 생애 주기로 묶은 것을 잡는다. 그래서 단서의 "completely"가 하중을 진다. 묘사가 모듈 내용을 다 담는지 대조하지 않으면 깔끔한 단동사 문장은 그냥 통과한다. 시험의 평가자 간 신뢰도나 예측 타당도를 잰 연구는 찾지 못했다. NASA SEL 연구자들은 모듈의 기능 수를 묻지 않았는데, 그 수가 "depends on the level of decomposition recognized by the respondent"(응답자가 인식하는 분해 수준에 달려 있다)이기 때문이다(Card 외 1986b). 문구도 하나가 아니다. 1974년 논문 안에서 판정 대상이 문장(시험)과 구(설계 절차)로 다르고, 비슷한 단어 목록과 함께 가르쳐지는 Yourdon & Constantine(1979)의 재진술은 원문을 확인하지 못했다 [미확인].

실증은 결합도 쪽이 낫고 응집도 쪽은 약하다. NASA 비행 역학 FORTRAN 모듈 453개에서 강도 높은 모듈의 50%, 낮은 모듈의 18%가 무결함이었으나, 강도는 자가 평정이었고 프로그래머 성과를 통제하자 유의성이 사라졌으며, COMMON 결합은 결함률과 관계가 없었다(Card 외 1986a). 객체 지향 결합 지표(CBO, RFC; Chidamber & Kemerer 1994)는 결함 경향과 관련되나 효과 일부가 클래스 크기에 교란되고(El Emam 외 2001; 반론 Evanco 2003), 응집 지표 LCOM 은 "insignificant in all cases"였으며(Basili 외 1996) 체계적 검토에서도 결함을 잘 찾지 못했다(Radjenović 외 2013). **응집 지표끼리도 55%의 경우에 서로 어긋났다**(Ó Cinnéide 외 2017). 구조 응집 지표는 공유 속성과 호출을 세므로 1974년 용어로는 통신적 관련에 가깝고, 연결 요소가 k>1 개면 k 개로 나눌 가능성을 시사하는 정도다(Hitz & Montazeri 1995). 개발자는 구조상 무관한 두 클래스도 "implement very similar responsibilities"(매우 비슷한 책임을 구현한다)면 강하게 결합되었다고 보았고, 구조 결합보다 어휘 기반 의미 결합이 그 판단에 가까웠다(Bavota 외 2013). 어휘로 재는 응집(C3)을 더하면 결함 예측도 나아졌다(Marcus 외 2008). 응집의 합의된 정의는 아직 없고(Counsell 외 2006), 응집·결합의 균형이 개발자가 추구하는 것이라는 실증도 없다(Candela 외 2016).

### 2.4 설계 규칙과 DSM: 구조 지표는 정보 은닉을 인증하지 못한다

Baldwin & Clark(2000)은 설계를 의존으로 얽힌 매개변수, 곧 설계 구조 행렬(design structure matrix, DSM)로 보고, 바뀌지 않기로 약속한 보이는 매개변수인 설계 규칙(design rule)이 클러스터 사이 의존을 끊을 때 모듈이 생긴다고 설명한다. "a module that depends only on design rules is a hidden module"(설계 규칙에만 의존하는 모듈이 숨은 모듈이다)(Sullivan 외 2001). 분할(splitting)은 의존의 원인을 별도 매개변수로 만들어 값을 고정하는 일이고, 소프트웨어의 대표 사례는 추상 자료형 인터페이스다. 모듈성의 가치는 모듈마다 따로 실험하고 대체할 옵션의 묶음이다. 공통 요소를 새 모듈로 떼어 내는 역전(inversion)은 더 실험할 이득이 비용을 넘지 못할 때 쓰며 규모의 경제를 얻는 대신 구조를 경직시키고(Gamba & Fusari 2009), 의존을 알기 전에 정한 규칙은 "miss the 'high peaks of value'"(가치의 높은 봉우리를 놓친다). 원서는 확인하지 못했다(경제 모형과 산업사 예시).

Sullivan 외(2001)가 이 틀로 KWIC 를 다시 분석하자 기본 DSM 은 Parnas 의 처리 단계 분해도 모듈적이라고 평가했다. "Basic DSM's alone are thus insufficient to represent Parnas's idea"(기본 DSM 만으로는 Parnas 의 생각을 표현하지 못한다). 설계자가 통제하지 못하는 환경 매개변수(컴퓨터 구성, 말뭉치 성질, 사용자)를 더해야 차이가 보이며, **정보 은닉이란 설계 규칙이 "invariant with respect to changes in the environment"(환경 변화에 대해 불변)인 것이다.** Line Store 와 Input 을 나눈 이유도 둘을 움직이는 외부 힘(말뭉치 크기, 운영체제)이 달라서다. 순옵션가치 0.26 대 1.56 은 대략적 추정이고 저자들은 실무 사용을 권하지 않는다. 가치 지형을 알 때까지 모듈화를 미루는 데에도 가치가 있다고 하여, 일찍 모듈화하는 Parnas 의 방법과 긴장한다(형식 모형, 예시 하나).

구조 지표 연구는 방향은 일관되나 근거가 약하다. 한 파일이 직·간접 의존으로 닿는 파일의 평균 비율인 전파 비용(propagation cost)은 Mozilla 재설계에서 17.35%에서 2.78%로 내려갔지만, 두 제품만 본 탐색 연구이고 이점의 상당 부분은 배치보다 의존 수 감소에서 왔다(MacCormack 외 2006). 한 회사에서 가시성 팬인과 팬아웃이 모두 높은 핵심(core) 파일은 주변 파일보다 결함이 3.4배였다(Sturtevant 2013; 상관, 단일 회사). 설계 규칙 위계(design rule hierarchy, DRH)는 하위 층이 상위 층의 설계 규칙에만 의존하고 같은 층 모듈이 서로 독립이 되게 파일을 배치하며(Xiao 외 2014), 설계 규칙을 위에 두므로 번호 방향이 Parnas 의 층과 반대다. 같은 층 모듈의 개발자끼리는 소통이 적었다(Wong 외 2009; 한 프로젝트). 여기서 나온 분리 수준(Decoupling Level, DL)은 41개 프로젝트에서 커밋·커미터 겹침 대리 지표와 r = −0.61~−0.77 로 상관했다. 저자들은 DL 이 단일 책임과 관심사 분리를 정량화한다고 주장하면서도 높은 DL 이 늘 좋은 아키텍처를 뜻하지는 않는다고 적는다(Mo 외 2016). 결함 집중 패턴으로는 영향력 큰 파일이 자주 함께 바뀌는 불안정 인터페이스(Unstable Interface)와 모듈을 가로지르는 순환이 강했으나(Mo 외 2015), **패키지 순환은 여섯 반패턴 가운데 영향이 가장 작았고**(Mo 외 2021), 결과 지표가 좋아져도 DL 은 거의 움직이지 않은 사례가 있다(Nayebi 외 2019). 2010년 이후 근거는 거의 한 그룹(Cai, Kazman)이 자체 도구로 낸 상관 연구이고, 독립 재현을 찾지 못했으며, Python·Rust 자료는 없다.

### 2.5 변경 이력: import 가 보지 못하는 결합과 침식

진화적 결합(evolutionary coupling)은 함께 바뀌는 것을 결합으로 본다. 논리적 결합(logical coupling), 변경 결합(change coupling)이라고도 하며 2.3의 논리적 결속과는 무관하다. "two entities are coupled whenever a change in an entity A implies a change in another entity B"(A 의 변경이 B 의 변경을 함축할 때마다 둘은 결합되어 있다)(Zimmermann 외 2003). 이상은 모든 진화적 결합이 정적 결합으로 정당화되는 것이고 어긋나는 곳이 구조 개선 대상인데, 다섯 OSS 중 넷에서 디렉터리 경계를 넘는 공변경 쌍이 안쪽 쌍보다 많았다. 다만 모듈별로 커밋을 쪼개는 정책과 잡음, 파일 단위 측정이 결과를 흔들고, 이력은 새 코드의 변경을 예측하지 못한다(Zimmermann 외 2005). 정적 분석이 못 보는 결합은 문서·설정·다른 언어 구현과의 연결, 한 개념의 평행한 형제 구현, RPC·이벤트 같은 간접 연결, 공유 관례이며, 발행-구독 시스템에는 "no syntactically visible dependency would exist"(구문상 보이는 의존이 없다)(Cataldo 외 2009).

모듈성 위반(modularity violation)은 이를 경계 판정에 쓴다. "if two components consistently change together ..., but they belong to two separate modules that are supposed to evolve independently, we consider this as a modularity violation"(독립적으로 진화해야 할 두 모듈의 요소가 일관되게 함께 바뀌면 모듈성 위반이다)(Wong 외 2011). Clio 가 보고한 위반 가운데 개발자가 나중에 고치거나 인정한 비율은 Hadoop 66%(152/231), Eclipse JDT 40%(161/399)였고(하한 추정), 리팩터링보다 평균 5~6 릴리스 앞섰다. 확인된 위반은 JDT 에서 순환 의존(72건)이, Hadoop 에서 명시적 의존이 없거나 반대 방향으로만 있는 이름 없는 결합(unnamed coupling, 66건)이 가장 많았고, 클라이언트의 변경이 의존 방향을 거슬러 의존 대상을 바꾼 사례도 있다. 두 시스템과 저자 평가라는 한계가 있다.

**정적 의존과 공변경은 양방향으로 어긋난다.** 두 회사의 C/C++ 시스템에서 구문 의존의 74.3%와 97.3%는 함께 바뀐 적이 없었고, 결함 모형의 설명력은 구문 의존을 더해도 7.1%에서 7.5%였지만 논리 의존을 더하자 29.5%가 되었다(Cataldo 외 2009, 프로젝트 A; 인과 주장은 없다). 7개 Java 프로젝트에서 모듈 경계를 넘는 공변경은 모듈 안 공변경보다 결함과 더 상관했으나, 거친 최상위 패키지를 모듈로 삼으면 두 프로젝트에서 반대였다(Kouroshfar 외 2015). 133개 GitHub 프로젝트의 공변경 클러스터 1,802개 가운데 디렉터리 안에 머문 것은 약 38%, 한 디렉터리를 중심으로 다른 곳에 팔을 뻗은 것이 약 48%였다(Silva 외 2019; 원문 안에서 123개 시스템이라고도 적어 수가 어긋난다). 개발자들은 이 문어형을 캡슐화하기 어려운 정상 분포로 보았다(Silva 외 2015). 문제인지는 결국 책임으로 판정되었다. Lucene 에서 색인·분석·저장을 가로지르는 클러스터는 "the package fails to hide its main design decisions"의 신호였지만, 한 서비스의 하위 패키지들을 가로지르는 클러스터는 해가 적었다(Silva 외 2014).

시간이 쌓이면 침식이 된다. Perry & Wolf(1992)는 아키텍처 위반에서 오는 침식(erosion)과 아키텍처에 대한 무감각에서 오는 표류(drift)를 나눴다. 표류는 "a lack of coherence and clarity of form"(형태의 일관성과 명료성 상실)을 낳아 위반을 쉽게 만들고, 처방은 하중을 받는 부분과 장식을 구분하고 의존·일관성 분석을 하는 것이다. 73편을 지도화한 연구는 지식 증발, 이해, 조직 같은 비기술적 원인에도 기술적 원인만큼 주의가 필요하다고 하고, 탐지 연구의 약 56%가 아키텍처 적합성 검사를 쓴다고 보고한다(Li 외 2022). 그러나 대책을 검증한 연구는 드물고 설계 결함은 정적 분석으로 발견되지 않는 경우가 많다(Li 외 2021). 함께 바뀌는 것을 함께 두라는 공통 폐쇄 원칙(Common Closure Principle; Martin & Martin 2007)은 이 연구들의 간접 지지만 받으며, **모듈에 적힌 책임 문장을 공변경과 대조한 연구는 없다.** 가장 가까운 선례는 클러스터에 연결된 이슈 설명의 의미 유사도로 클러스터가 한 주제인지 보는 것이다(Silva 외 2014).

### 2.6 하나의 분해로는 모든 관심사를 담지 못한다: 횡단 관심사와 표현 문제

Tarr 외(1999)는 이를 지배적 분해의 횡포(tyranny of the dominant decomposition)라 불렀다. 기존 모듈화 수단은 "usually only a single 'dominant' one at a time"(대개 한 번에 하나의 지배적 분해만) 지원한다. 요구는 기능별로, 코드는 객체별로 나뉘면 한 요구가 여러 모듈에 퍼지는 산재(scattering)와 여러 요구가 한 모듈에 섞이는 뒤엉킴(tangling)이 생긴다. 그들은 겹치는 조각을 한 단계 위의 조합 규칙으로 묶자고 하면서도 "overseparation of concerns is as bad as underseparation"(지나친 분리는 모자란 분리만큼 나쁘다)이라 경고했다(형식 논증, 예제 하나). Kiczales 외(1997)는 동기화나 실패 처리처럼 절차나 객체로 깔끔하게 캡슐화되지 않는 성질을 측면(aspect)이라 하고 따로 작성해 엮자고 했으나(사례 하나), 보이지 않게 엮인 효과는 "the Go To statement is at least visible in the code, but advice is not"(goto 는 보이기라도 하지만 advice 는 보이지 않는다)이라는 비판을 받았고(Constantinides 외 2004), 학생 실험에서는 변경 편집이 줄어든 대신 이해가 느려졌다(Przybyłek 2018).

산재의 비용은 Eaddy 외(2008)가 쟀다. 세 Java 프로젝트에서 요구 사항 구현이 흩어질수록 버그가 많았지만(스피어만 0.29~0.74), 두 프로젝트에서는 크기가 더 강한 예측 변수였으므로 산재를 줄이며 크기를 키우는 리팩터링은 결함을 늘릴 수 있다. 저자들은 산재를 "the rule rather than the exception"(예외가 아니라 규칙)으로 보았고, Rhino 에서 가장 흩어지고 버그가 많은 관심사는 대부분의 메서드에 범위 매개변수를 넘기는 방식이었다(상관 연구, 주관적 관심사 대응, Java 한정).

표현 문제(expression problem)는 같은 한계를 형식으로 보인다. Wadler(1998)는 이를 경우로 정의한 자료형에 "add new cases to the datatype and new functions over the datatype, without recompiling existing code, and while retaining static type safety"(기존 코드를 재컴파일하지 않고 정적 타입 안전을 지키며 새 경우와 새 함수를 모두 더하는 것)의 문제로 정의했다. 함수형 언어는 함수를, 객체 지향 언어는 경우를 더하기 쉽다. Cook(2009)은 객체와 추상 자료형을 "the strengths of one are the weaknesses of the other"(한쪽의 강점이 다른 쪽의 약점)인 쌍대로 보고 행위를 표현 × 연산의 행렬로 정리한다. 행을 모듈로 삼으면 열이 흩어지고 열을 모듈로 삼으면 행이 흩어지므로, **'책임 하나'는 어느 축의 변화를 국소화할지 고르는 일과 함께 정해진다**(형식 논증). 두 기능이 함께 있을 때만 필요한 상호작용 코드도 어느 기능에도 속하지 않아 별도 모듈을 요구한다(Apel & Kästner 2009).

실무 문서는 숨은 엮기 대신 보이는 방식으로 수렴한다. 라이브러리는 기본 동작이 없는 얇은 API(Python logging 의 NullHandler, Rust log 퍼사드, OpenTelemetry API)에만 의존하고, 구현 선택과 설정은 애플리케이션 진입점이 맡으며, 요청 범위 맥락은 명시적으로 넘긴다(Python Logging HOWTO; Rust log 0.4.34; OpenTelemetry 문서; Go context 문서; Seemann 2011). 호출 지점은 흩어지되 보이고 조합은 한 단계 위에서 하니 Tarr 의 구도와 같다. util·common 같은 잡동사니 패키지는 권장되지 않는다(Ajmani 2015). 모두 전문가 의견이다.

### 2.7 정리: 합의되는 것과 갈라지는 것

문헌이 넓게 합의하는 것은 셋이다. 경계는 처리 순서가 아니라 함께 바뀌는 것을 기준으로 긋고(Parnas 1972; Parnas 1978; Wong 외 2011; Stevens 외 1974의 시간어 시험), 의존은 위로 거슬러 오르거나 순환하지 않게 하며(Parnas 1978; Bachmann 외 2000), 다른 모듈의 내부가 아니라 명세된 인터페이스에만 기댄다(Stevens 외 1974; Parnas 2009). 갈라지는 쟁점은 다음과 같다.

| 쟁점 | 한쪽 | 다른 쪽 |
|---|---|---|
| 책임의 단위 | 숨긴 설계 결정. 데이터와 접근 절차는 함께(Parnas 1972) | 입력을 출력으로 바꾸는 기능 하나. 같은 데이터를 다루는 묶음은 낮게 친다(Stevens 외 1974) |
| 층의 정체 | 의존 그래프에서 계산, 모듈과 무관(Parnas 1978; Habermann 외 1976) | 설계자가 정한 허용 사용 관계, 코드에서 도출 불가(Bachmann 외 2000) |
| 같은 층 사용 | 같은 층 모듈은 서로 독립(Xiao 외 2014) | 대개 허용(Bachmann 외 2000) |
| 나누기를 멈출 때 | 비밀이 독립적으로 바뀔 때만 나누고 과분리를 경계(Parnas 2009; Tarr 외 1999) | 작은 독립 모듈이 많을수록 점수가 오른다(Mo 외 2016) |
| 경계를 정할 때 | 바뀔 결정 목록으로 일찍(Parnas 1972) | 의존과 가치를 알 때까지 미룬다(Sullivan 외 2001) |
| 순환의 비용 | 모듈 간 순환과 핵심부가 결함과 상관(Mo 외 2015; Sturtevant 2013) | 패키지 순환은 영향이 가장 작고 모든 순환이 해롭지는 않다(Mo 외 2021; Xiao 외 2014) |

정의와 형식 논증(사용 관계와 계산된 층, 정보 은닉 정리, 표현 문제)은 견고하다. 그러나 무엇을 숨길지와 책임이 하나인지의 판정은 끝내 판단에 남고, 그 판단을 대신하려는 구조 지표의 실증은 약하다. 가장 일관된 실증은 모듈 경계를 넘는 변경과 핵심부의 순환이 결함과 함께 간다는 상관이다.

### 참고문헌 (2장)

표시가 없으면 원문(또는 저자 사본, 전사본)을 읽은 것이다. (초록만 확인)은 초록이나 저자 슬라이드만 본 것, [2차 출처]는 다른 문헌의 인용·요약으로만 확인한 것, [미확인]은 서지나 문구를 확인하지 못한 것이다. 노트에 제목이 없어 덧붙인 제목에는 [제목 미확인]을 붙였다.

- Ajmani (2015). "Package names." *The Go Blog*, 2015-02-04. https://go.dev/blog/package-names
- Apel & Kästner (2009). "An Overview of Feature-Oriented Software Development." *Journal of Object Technology* 8(5). https://www.jot.fm/issues/issue_2009_07/column5.pdf
- Bachmann, Bass, Carriere, Clements, Garlan, Ivers, Nord & Little (2000). *Software Architecture Documentation in Practice: Documenting Architectural Layers*. CMU/SEI-2000-SR-004. https://www.sei.cmu.edu/documents/5437/2000_003_001_13649.pdf (후속판 Clements 외, *Documenting Software Architectures: Views and Beyond*, 2판, Addison-Wesley 2010 에 흡수되었고, 2판은 앞부분과 색인만 확인)
- Bachmann, Bass & Nord (2007). *Modifiability Tactics*. CMU/SEI-2007-TR-002. https://www.sei.cmu.edu/documents/778/2007_005_001_14858.pdf
- Baldwin & Clark (2000). *Design Rules, Vol. 1: The Power of Modularity*. MIT Press. URL 없음. [2차 출처: Sullivan 외 2001, Gamba & Fusari 2009 경유. 원서 미열람]
- Basili, Briand & Melo (1996). "A Validation of Object-Oriented Design Metrics as Quality Indicators" [제목 미확인]. *IEEE TSE* 22(10):751–761. https://doi.org/10.1109/32.544352 (UMD 기술 보고서 CS-TR-3443, 1995 로 열람: https://www.cs.umd.edu/~basili/publications/technical/T102.pdf)
- Bass, Clements & Kazman (2003). *Software Architecture in Practice*, 2판, 3장(A-7E 모듈 구조 재수록). Addison-Wesley. 강의용 사본: https://people.ece.ubc.ca/matei/EECE417/BASS/ch03lev1sec3.html (PCW 내용에 대해서는 [2차 출처])
- Bavota, Dit, Oliveto, Di Penta, Poshyvanyk & De Lucia (2013). "An Empirical Study on the Developers' Perception of Software Coupling." *ICSE 2013*. https://people.lu.usi.ch/bavotg/papers/icse2013_Coupling.pdf
- Bieman & Ott (1994). "Measuring Functional Cohesion." *IEEE TSE* 20(8):644–657. https://doi.org/10.1109/32.310673
- Bredereke (2002). Bremen 대학 강의 노트 "lect-3_2toP232", 2002/03 겨울 학기. https://www.cs.uni-bremen.de/agbs/lehre/ws0203/scs4/lect-3_2toP232.pdf [PCW 내용의 2차 출처]
- Buschmann, Meunier, Rohnert, Sommerlad & Stal (1996). *Pattern-Oriented Software Architecture, Vol. 1: A System of Patterns*. Wiley. [2차 출처: Bachmann, Bass & Nord 2007 의 재수록과 arc42 요약 https://patterns.arc42.org/patterns/layer 경유]
- Candela, Bavota, Russo & Oliveto (2016). "Using Cohesion and Coupling for Software Remodularization: Is It Enough?" *ACM TOSEM* 25(3). https://doi.org/10.1145/2928268 (초록만 확인. 설문 인원은 초록 29명, 저자 연구실 페이지 34명으로 어긋난다)
- Card, Church & Agresti (1986a). "An Empirical Study of Software Design Practices" [제목 미확인]. *IEEE TSE* 12(2):264–271. https://doi.org/10.1109/TSE.1986.6312942 (NASA 사본: https://ntrs.nasa.gov/api/citations/19870015475/downloads/19870015475.pdf)
- Card 외 (1986b). *Measuring Software Design*. NASA Software Engineering Laboratory 보고서, 1986년 11월. https://ntrs.nasa.gov/api/citations/19870013756/downloads/19870013756.pdf
- Cataldo, Mockus, Roberts & Herbsleb (2009). "Software Dependencies, Work Dependencies, and Their Impact on Failures." *IEEE TSE* 35(6):864–878. https://doi.org/10.1109/TSE.2009.42 (저자 사본: https://mockus.org/papers/multicompany.pdf)
- Chidamber & Kemerer (1994). "A Metrics Suite for Object Oriented Design." *IEEE TSE* 20(6):476–493. https://doi.org/10.1109/32.295895 (초록만 확인. 지표 정의는 Hitz & Montazeri 1995, Basili 외 1996 의 인용으로 확인)
- Constantinides, Skotiniotis & Störzer (2004). "AOP Considered Harmful." 입장 논문, 2004-08-23. 제3자 사본: https://studfile.net/preview/429354 (게재처 EIWAS 2004 는 [미확인])
- Cook (2009). "On Understanding Data Abstraction, Revisited." *OOPSLA 2009 Onward! Essays*. https://www.cs.utexas.edu/~wcook/Drafts/2009/essay.pdf
- Counsell, Swift & Crampton (2006). "The Interpretation and Utility of Three Cohesion Metrics for Object-Oriented Design" [제목 미확인]. *ACM TOSEM* 15(2):123–149. https://doi.org/10.1145/1131421.1131422 (초록만 확인)
- Dijkstra (1968). "The Structure of the 'THE'-Multiprogramming System." *CACM* 11(5):341–346. https://doi.org/10.1145/363095.363143 (EWD196 전사본으로 열람, 인쇄본과 대조하지 않음: https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html)
- Dijkstra (1974). "On the role of scientific thought." EWD447, 1974-08-30. https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD447.html
- Eaddy, Zimmermann, Sherwood, Garg, Murphy, Nagappan & Aho (2008). "Do Crosscutting Concerns Cause Defects?" *IEEE TSE* 34(4):497–515. https://doi.org/10.1109/TSE.2008.36 (저자 사본: https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- El Emam, Benlarbi, Goel & Rai (2001). "The Confounding Effect of Class Size on the Validity of Object-Oriented Metrics." *IEEE TSE* 27(7):630–650. https://doi.org/10.1109/32.935855 (초록 일부만 확인. 후속 보고서 NRC ERB-1063, 1999: https://www.ehealthinformation.ca/web/default/files/wp-files/10631.pdf)
- Evanco (2003). "Comments on 'The Confounding Effect of Class Size on the Validity of Object-Oriented Metrics'" [제목 미확인]. *IEEE TSE*. https://doi.org/10.1109/TSE.2003.1214331 (초록만 확인)
- Gamba & Fusari (2009). "Valuing Modularity as a Real Option." 워킹 페이퍼, 2009년 2월. https://www.realoptions.org/papers2009/8.pdf
- Garlan & Shaw (1993). "An Introduction to Software Architecture." *Advances in Software Engineering and Knowledge Engineering*, Vol. I, World Scientific. CMU-CS-94-166 판으로 열람: https://www.cs.cmu.edu/afs/cs/project/able/ftp/intro_softarch/intro_softarch.pdf
- Go context 문서 (2026). "Package context." pkg.go.dev, go1.27.2. https://pkg.go.dev/context
- Habermann, Flon & Cooprider (1976). "Modularization and Hierarchy in a Family of Operating Systems." *CACM* 19(5):266–272. https://doi.org/10.1145/360051.360076 (스캔: https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Hitz & Montazeri (1995). "Measuring Coupling and Cohesion in Object-Oriented Systems." 게재처(ISACC'95)는 [미확인]. http://www.isys.uni-klu.ac.at/PDF/1995-0043-MHBM.pdf
- Kiczales, Lamping, Mendhekar, Maeda, Lopes, Loingtier & Irwin (1997). "Aspect-Oriented Programming." *ECOOP '97*, LNCS 1241. https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf
- Kouroshfar, Mirakhorli, Bagheri, Xiao, Malek & Cai (2015). "A Study on the Role of Software Architecture in the Evolution and Quality of Software." *MSR 2015*. http://www.cs.drexel.edu/~yfcai/papers/2015/msr2015.pdf
- Li, Liang, Soliman & Avgeriou (2021). "Understanding Architecture Erosion: The Practitioners' Perceptive." *ICPC 2021*. https://arxiv.org/abs/2103.11392
- Li, Liang, Soliman & Avgeriou (2022). "Understanding Software Architecture Erosion: A Systematic Mapping Study." *Journal of Software: Evolution and Process* e2423. https://doi.org/10.1002/smr.2423 (https://arxiv.org/abs/2112.10934)
- Liskov (2013). "The Power of Abstraction." QCon London 2013 기조연설 슬라이드. https://qconlondon.com/ln2018/london-2013/qconlondon.com/dl/qcon-london-2013/slides/BarbaraLiskov_KeynoteThePowerOfAbstraction.pdf
- Liskov & Zilles (1974). "Programming with Abstract Data Types." *SIGPLAN Notices* 9(4):50–59. https://doi.org/10.1145/800233.807045 [2차 출처: 원문 미열람. Colyer 블로그 https://blog.acolyer.org/2016/10/20/programming-with-abstract-data-types/ 와 Liskov 슬라이드 경유]
- MacCormack, Rusnak & Baldwin (2006). "Exploring the Structure of Complex Software Designs: An Empirical Study of Open Source and Proprietary Code" [제목 미확인]. *Management Science* 52(7):1015–1030. https://doi.org/10.1287/mnsc.1060.0552 (2004년 HBS 워킹 페이퍼 05-016 으로 열람, 게재본 수치와 대조하지 않음: https://www.hbs.edu/ris/Publication%20Files/05-016.pdf)
- Marcus, Poshyvanyk & Ferenc (2008). "Using the Conceptual Cohesion of Classes for Fault Prediction in Object-Oriented Systems" [제목 미확인]. *IEEE TSE* 34(2):287–300. https://doi.org/10.1109/TSE.2007.70768 (초록만 확인)
- Martin & Martin (2007). *Agile Principles, Patterns, and Practices in C#*. Prentice Hall. URL 없음. [2차 출처: Kouroshfar 외 2015 의 요약. 원 문구 미확인]
- Mo, Cai, Kazman & Xiao (2015). "Hotspot Patterns." *WICSA 2015*, pp. 51–60. https://www.cs.drexel.edu/~yc349/papers/2015/wicsa2015.pdf
- Mo, Cai, Kazman, Xiao & Feng (2016). "Decoupling Level: A New Metric for Architectural Maintenance Complexity." *ICSE 2016*, pp. 499–510. https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf
- Mo 외 (2021). "Architecture Anti-patterns." *IEEE TSE* 47(5):1008–1028 (2019 조기 공개, Mo 외 2015 를 대체). https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf
- Myers (1978). *Composite/Structured Design*. Van Nostrand Reinhold (앞선 판 *Reliable Software Through Composite Design*, 1975). URL 없음. [2차 출처: Card 외 1986b 경유]
- Nayebi 외 (2019). "A Longitudinal Study of Identifying and Paying Down Architecture Debt" [제목 미확인]. *ICSE-SEIP 2019*. https://arxiv.org/abs/1811.12904
- Ó Cinnéide, Hemati Moghadam, Harman, Counsell & Tratt (2017). "An Experimental Search-Based Approach to Cohesion Metric Evaluation" [제목 미확인]. *Empirical Software Engineering* 22(1):292–329. https://doi.org/10.1007/s10664-016-9427-7 (초록만 확인)
- OpenTelemetry 문서 (연도 미상). "Instrumenting libraries." https://opentelemetry.io/docs/concepts/instrumentation/libraries/
- Parnas (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *CACM* 15(12):1053–1058. https://doi.org/10.1145/361598.361623 (https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf)
- Parnas (1978). "Designing Software for Ease of Extension and Contraction." *Proc. 3rd ICSE*, pp. 264–277. OCR 스캔: https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf (이를 대체하는 저널판 *IEEE TSE* SE-5(2):128–138, 1979, https://doi.org/10.1109/TSE.1979.234169 는 미열람)
- Parnas (1994). "Software Aging." *ICSE 16*, pp. 279–287. https://doi.org/10.1109/ICSE.1994.296790 (https://www.eecs.yorku.ca/course_archive/2007-08/F/6431/Parnas.pdf)
- Parnas (2009). "Making Information Hiding Work." 강연 슬라이드, 홍콩침례대학교, 2009-09-01. https://www.comp.hkbu.edu.hk/~pgday/2009/10th_PPT/HOSEI%20Making%20Information%20Hiding%20Work%20slides.pdf
- Parnas, Clements & Weiss (1985). "The Modular Structure of Complex Systems." *IEEE TSE* SE-11(3):259–266. https://doi.org/10.1109/TSE.1985.232209 (학회판 *ICSE 7*, 1984). 초록만 확인, 내용은 [2차 출처: Parnas 2009, Bass 외 2003, Bredereke 2002 경유]
- Perry & Wolf (1992). "Foundations for the Study of Software Architecture." *ACM SIGSOFT Software Engineering Notes* 17(4). https://users.ece.utexas.edu/~perry/work/papers/swa-sen.pdf
- Przybyłek (2018). "An Empirical Study on the Impact of AspectJ on Software Evolvability." *Empirical Software Engineering*. https://doi.org/10.1007/s10664-017-9580-7 [2차 출처: 검색 요약에 실린 초록]
- Python Logging HOWTO (2026). Python 3.15 문서, 2026년 10월 갱신. https://docs.python.org/3/howto/logging.html
- Radjenović 외 (2013). "Software Fault Prediction Metrics: A Systematic Literature Review" [제목 미확인]. *Information and Software Technology* 55(8):1397–1418. 저자 사본: https://gup.ub.gu.se/file/127150
- Rust log 0.4.34 (연도 미상). log 크레이트 문서. https://docs.rs/log/latest/log/
- Sarkar, Maskeri & Ramachandran (2009). "Discovery of Architectural Layers and Measurement of Layering Violations in Source Code." *Journal of Systems and Software* 82(11):1891–1905. URL 없음. [2차 출처: Thakare & Kiwelekar, "Redefining measures of Layered Architecture", arXiv:2106.03079, 2021 경유 https://arxiv.org/pdf/2106.03079]
- Seemann (2011). "Composition Root." 2011-07-28. https://blog.ploeh.dk/2011/07/28/CompositionRoot/
- Silva, Valente & Maia (2014). "Assessing Modularity using Co-Change Clusters." *MODULARITY '14*, pp. 49–60. https://doi.org/10.1145/2577080.2577086 (https://homepages.dcc.ufmg.br/~mtov/pub/2014_modularity.pdf)
- Silva, Valente, Maia & Anquetil (2015). "Developers' Perception of Co-Change Patterns: An Empirical Study." *ICSME 2015*, pp. 21–30. URL 없음. [2차 출처: Silva 외 2019 의 요약]
- Silva, Valente & Maia (2019). "Co-Change Patterns: A Large Scale Empirical Study." *Journal of Systems and Software* (2019-03-15 사전 인쇄본, 게재 권호 미확인). https://homepages.dcc.ufmg.br/~mtov/pub/2019-jss.pdf
- Stevens, Myers & Constantine (1974). "Structured Design." *IBM Systems Journal* 13(2):115–139. https://doi.org/10.1147/sj.132.0115 (1999년 재수록판 *IBM Systems Journal* 38(2&3)의 비공식 스캔으로 열람, 본문의 쪽 번호는 재수록판 기준: https://scrapbox.io/files/607d58d8fb61eb001eee7175.pdf)
- Sturtevant (2013). *System Design and the Cost of Architectural Complexity*. MIT 박사 학위 논문. https://dspace.mit.edu/handle/1721.1/79551 (본문은 제3자 사본으로 열람)
- Sullivan, Griswold, Cai & Hallen (2001). "The Structure and Value of Modularity in Software Design." *ESEC/FSE 2001*, pp. 99–108. https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf
- Tarr, Ossher, Harrison & Sutton (1999). "N Degrees of Separation: Multi-Dimensional Separation of Concerns." *ICSE 1999*, pp. 107–119. https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf
- Wadler (1998). "The Expression Problem." java-genericity 메일링 리스트, 1998-11-12. https://homepages.inf.ed.ac.uk/wadler/papers/expression/expression.txt
- Wong 외 (2009). "Design Rule Hierarchies and Parallelism in Software Development Tasks." *ASE 2009*. https://www.cs.drexel.edu/~yc349/papers/2009/ASE2009_drh.pdf
- Wong, Cai, Kim & Dalton (2011). "Detecting Software Modularity Violations." *ICSE 2011*, pp. 411–420. http://www.cs.drexel.edu/~yfcai/papers/2011/ICSE2011.pdf
- Xiao, Cai & Kazman (2014). "Design Rule Spaces: A New Form of Architecture Insight." *ICSE 2014*, pp. 967–977. https://www.cs.drexel.edu/~yc349/papers/2014/icse2014.pdf
- Yourdon & Constantine (1979). *Structured Design*. Prentice-Hall. URL 없음. [2차 출처: Verhoeff 의 인용 모음 https://wstomv.win.tue.nl/quotes/structured-design.html 과 Bieman & Ott 1994 경유. 1975·1978 년 Yourdon Press 판의 연도는 미확인]
- Zimmermann, Diehl & Zeller (2003). "How History Justifies System Architecture (or not)." *IWPSE 2003*. https://thomas-zimmermann.com/publications/files/zimmermann-iwpse-2003.pdf
- Zimmermann, Weißgerber, Diehl & Zeller (2005). "Mining Version Histories to Guide Software Changes." *IEEE TSE* 31(6):429–445. https://thomas-zimmermann.com/publications/files/zimmermann-tse-2005.pdf
