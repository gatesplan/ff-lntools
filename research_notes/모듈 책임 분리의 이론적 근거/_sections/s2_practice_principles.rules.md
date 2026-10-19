# 3장 부속: 규칙 후보와 ln-structure 시사점 (실무 전문가의 원칙)

입력 노트: b5(책임 주도 설계, CRC, GRASP), b1(Martin 의 SRP 와 컴포넌트 원칙), b2(Ousterhout), b3(Beck, Hunt & Thomas, Metz, 3의 규칙), b6(connascence, 균형 결합).
출처 표기는 3장 본문과 같다(저자 연도). 본문 참고문헌에 없는 출처는 맨 아래 '이 파일에만 나오는 출처'에 적었다.
[2차 출처] 는 요약, 독자 하이라이트, 초록 등으로만 확인한 출처다. [미확인] 은 확인하지 못한 세부다. '노트의 추론'은 노트 작성자가 출처에서 끌어낸 판단이고 출처의 문장이 아니다.
근거 강도는 형식 논증 / 실증 / 전문가 의견으로 나누고 강, 중, 약을 붙였다. 이 장의 출처에는 원칙 하나를 따로 검증한 통제 실험이 없으므로 '강'은 거의 없다.

## 규칙 후보

1. **모듈의 책임은 무엇을 맡는지(무엇을 알고, 하고, 정하는지)를 개별 연산보다 한 단계 높은 수준에서 적고, 어떻게 하는지는 적지 않는다.**
   - 근거: 구현 결정을 미루고 책임부터 정하면 캡슐화가 커진다. 잘 짜인 책임은 "a high-level statement of what an object knows or does"이고 속성이나 연산의 목록이 아니다. 책임은 "what, rather than how"를 적어 인터페이스와 구현을 가른다. 사용자 요구처럼 들리는 높은 수준의 호출이 구현 세부보다 낫다.
   - 출처: Wirfs-Brock & Wilkerson 1989; Wirfs-Brock & McKean 2003, pp.128–131; Biddle et al. 2002; Hunt & Thomas 2003; Stevens et al. 1974(일반 설계는 무엇, 상세 설계는 어떻게. 2장)
   - 근거 강도: 전문가 의견(서로 독립한 여러 저자의 합의) + 형식 논증(캡슐화). 중
   - 반론과 한계: 너무 일반적으로 쓰면 'managing resources', 'doing the work' 같은 막연한 문장이 되고, 그때는 문제 진술로 보고 쪼개야 한다(Wirfs-Brock & McKean 2003, p.138). 짧은 책임 목록은 맥락 없이 이해되지 않았다(Beck & Cunningham 1989). 통제된 검증은 없다.

2. **'하나'의 단위는 책임 문장 하나가 아니라 응집된 역할(목적) 하나다. 한 역할은 짧은 책임 진술 몇 개로 이루어질 수 있다.**
   - 근거: RDD 의 역할은 "a set of related responsibilities"이고, 잘 짜인 객체의 시험은 책임들이 "form a cohesive unit"인가다. CRC 는 책임을 "a handful of short verb phrases"로 적는다. 1990년 서브시스템 카드는 한 줄 설명 아래 여러 계약을 두고 계약마다 안쪽 클래스에 위임했다.
   - 출처: Wirfs-Brock & McKean 2003, pp.3, 146; Beck & Cunningham 1989; Wirfs-Brock et al. 1990 [2차 출처]; Booch 의 '클래스마다 책임 3–5개'(Henney 2012 에서 재인용); Dunn 2021 [2차 출처]
   - 근거 강도: 정의 + 전문가 의견. 중
   - 반론과 한계: Martin 은 '하나'를 행위자 하나로 정의해 개념이 하나여도 행위자가 여럿이면 나누라고 한다(Martin 2014; Martin 2017 [2차 출처]). 몇 개까지 한 역할로 볼지의 기준은 어느 출처에도 없다.

3. **한 모듈에 변경을 요구하는 주체(행위자, 서로 다른 목적의 클라이언트 종류)가 둘 이상이면 분리 후보로 본다.**
   - 근거: SRP 최종형 "A module should be responsible to one, and only one, actor". 급여 계산, 근무 시간 보고, 저장을 한 클래스에 두면 CFO, COO, CTO 가 같은 클래스를 바꾼다. RDD 도 객체가 "two different types of clients for different purposes"를 섬기면 두 역할일 가능성이 크다고 본다.
   - 출처: Martin 2014; Martin 2017 [2차 출처]; Wirfs-Brock & McKean 2003, p.5
   - 근거 강도: 전문가 의견. 약~중
   - 반론과 한계: '변경의 이유'는 모호하고 사후에야 보인다(North 2017; Cecconi 2014 [2차 출처]). 행위자는 조직 구조라 코드에서 보이지 않는다. 데이터의 내용과 형식처럼 함께 바뀌는 것을 가르면 인위적 이음매가 생긴다(North 2022). Martin 본인도 변경이 실제로 일어나기 전에 나누면 "Needless Complexity"라 했다(Martin & Martin 2006).

4. **같은 지식(함께 바뀌는 것)은 한 모듈에 모으고, 한 지식을 여러 모듈에 복제하거나 쪼개 두지 않는다(단일 진실 원천).**
   - 근거: CCP "Classes that change together, belong together". DRY "single, unambiguous, authoritative representation". 직교성은 한 지식을 여러 구성 요소에 쪼개지 말라는 쪽이다. RDD "Keep information about one thing in one place". Ousterhout 는 같은 파일 형식을 두 클래스가 알면 둘 다 고쳐야 하는 누출이라며 한 곳으로 모으라고 한다. Khononov 는 같은 업무 규칙의 중복 구현을 기능 결합의 극단으로 본다.
   - 출처: Martin 2000; Thomas & Hunt 2019 [2차 출처]; Wirfs-Brock & McKean 2003; Ousterhout 2018a [2차 출처]; Ousterhout 2018b; Khononov n.d.
   - 근거 강도: 전문가 의견(넓은 합의) + 간접 실증(클론의 비일관 변경이 잦고 결함을 낳음. Juergens et al. 2009 [2차 출처], 상용 C# 3, COBOL 1, 오픈소스 Java 1). 중~강
   - 반론과 한계: 같은 지식인지는 사람이 판단해야 하고 import 그래프로 보이지 않는다(Beck 2023 [2차 출처]; Liljas et al. 2026). 클론의 상당수는 의도적이고 유익하다(Kapser & Godfrey 2008 [2차 출처]). DRY 를 어긴 코드가 모두 알고리즘 공유 결합은 아니다(Brown 2011).

5. **강하게 얽힌 코드(실행 순서, 값의 의미, 알고리즘, 위치를 공유)는 같은 경계 안에 두고, 경계를 넘는 결합은 이름과 명시적 계약처럼 약하고 드러난 형태로 낮춘다.**
   - 근거: Page-Jones 의 규칙(경계 안의 connascence 를 최대화해 경계를 넘는 connascence 를 최소화). Weirich 의 국소성 규칙(멀수록 약해야 함). connascence.io: 강한 형태는 모듈 안에서 더 받아들일 만하다. Khononov 의 BALANCE(강한 결합은 가까이, 약한 결합은 멀리). Beck: 응집은 요소 안쪽의 결합이며 많을수록 좋다.
   - 출처: Page-Jones 1992 [2차 출처]; KN-86 docs n.d. [2차 출처]; connascence.io n.d.; Khononov n.d.; Khononov 2024; Beck 2022; Beck 2024
   - 근거 강도: 형식 논증 + 전문가 의견. 중. 직접 실증 없음
   - 반론과 한계: 세기의 순서가 출처마다 다르다(위치와 알고리즘의 순서, 값의 누락. Brown 2011; Khononov n.d.). Rutherford 는 connascence 가 지표도 방법론도 아니며 아홉 형태 목록을 규범으로 쓰면 안 된다고 한다(Rutherford 2022). 정적 검사가 보는 경계 넘는 결합은 대부분 이름과 타입뿐이다(connascence.io n.d., 노트의 추론).

6. **나누는 것도 비용이다. 나눈 결과 인터페이스가 구현만큼 복잡해지거나, 한쪽을 이해하려면 다른 쪽을 읽어야 하거나, 받은 호출을 넘기기만 하는 층이 생기면 합친다. 합칠 징후는 정보 공유, 양방향으로 함께 쓰임, 개념 겹침, 따로 이해할 수 없음이다.**
   - 근거: 클래스염(classitis), 결합된 메서드(conjoined methods), 그대로 넘기는 메서드와 추상이 비슷한 이웃 층(Ousterhout). 너무 작은 역할과 접착 객체(Wirfs-Brock). Needless Complexity(Martin). 단순 설계의 '요소 최소화'(Beck). 모듈을 순진하게 잘게 나누면 국소 복잡성을 위로 밀어 올릴 뿐(Olano 의 Khononov 요약). 메서드 하나짜리 클래스 양산(Cecconi). '함께 쓰임'은 양방향일 때만 합칠 근거다(해시 테이블과 디스크 블록 캐시는 나눈다).
   - 출처: Ousterhout 2018a [2차 출처]; Ousterhout 2018b; Ousterhout 2021; Wirfs-Brock & McKean 2003, pp.134, 137; Martin & Martin 2006; Fowler 2015; Olano 2025 [2차 출처]; Cecconi 2014 [2차 출처]
   - 근거 강도: 전문가 의견(서로 독립한 여러 출처). 중. 메서드 길이의 주변 실증은 24줄 미만 정도의 적당한 짧음을 지지할 뿐 엇갈린다(Chowdhury et al. 2022; Chin & Holmes 2026)
   - 반론과 한계: Martin 은 틀린다면 나누는 쪽을 택하고 나중에 인라인하면 된다고 본다(Ousterhout & Martin 2025). 멈출 지점의 합의된 기준이 없다. 깊이는 측정 방법이 없고 축척이 임의적이라는 비판이 있다(Normand 2021).

7. **범용 메커니즘과 특정 용도의 코드는 다른 모듈에 둔다. 특수화는 범용 인터페이스의 위(사용처)나 아래(장치 드라이버 같은 구현체)로 밀어낸다.**
   - 근거: "Special-purpose code associated with a general-purpose mechanism should normally go in a different module". 2판은 과도한 특수화가 복잡성의 가장 큰 원인일 수 있고 범용 인터페이스가 더 깊다고 한다. 장치 드라이버가 범용 인터페이스를 구현해 특수화를 아래로 내린다.
   - 출처: Ousterhout 2018a [2차 출처]; Ousterhout 2021, pp.39–49
   - 근거 강도: 전문가 의견(수업 산출물 관찰, 비통제). 약~중
   - 반론과 한계: 2판도 한 메커니즘의 특수 코드와 다른 메커니즘의 범용 코드를 합치는 것이 맞을 수 있다는 단서와 "don't get carried away"(지나치게 일반화하지 말라)는 경고를 단다(Ousterhout 2021). 투기적 일반화를 경계하는 Larman, Metz 와 긴장한다(Larman 2001; Metz 2016).

8. **시간 순서(먼저, 다음, 초기화, 정리)로 모듈을 나누지 않고, 각 작업에 필요한 지식으로 나눈다.**
   - 근거: 시간적 분해는 정보 누출과 얕은 모듈을 낳는다. 1974년 문장 시험도 시간어와 초기화, 정리 같은 말을 약한(시간적) 응집의 신호로 본다.
   - 출처: Ousterhout 2018a [2차 출처]; Stevens et al. 1974(2장)
   - 근거 강도: 전문가 의견 + 형식 논증. 중
   - 반론과 한계: 실증 없음. import 규칙으로는 감지되지 않는다(노트의 추론).

9. **책임 문장이 '그리고'나 '또는'으로 이어지거나, 시간어를 쓰거나, 약하고 막연한 동사나 특정 대상이 없는 술어를 쓰면 다시 쓰기나 분리 후보로 알린다. 넘치면 먼저 더 높은 수준으로 다시 쓰고, 그래도 복잡하면 나눈다.**
   - 근거: Metz 의 and/or 시험. 1974년 문법 시험(복문, 여러 동사, 시간어, 특정 대상 없는 술어). RDD 의 약한 동사(organize, record, find, process, maintain, list, accept)와 막연한 책임('managing resources'). Ousterhout 의 적신호 Hard to Describe, Hard to Pick Name, Vague Name. CRC 의 처방 순서(다시 쓰기, 그다음 나누기).
   - 출처: Metz 2012 [2차 출처]; Stevens et al. 1974; Wirfs-Brock & McKean 2003, pp.131, 138; Ousterhout 2018a [2차 출처: 요약 목록]; Beck & Cunningham 1989
   - 근거 강도: 전문가 의견. 약. 두 문법 시험 모두 실증 검증이 없다
   - 반론과 한계: 1974년 저자들이 응집된 모듈도 복문으로 설명될 수 있다고 적었다(오탐). 도메인에서 뜻이 분명한 약한 동사는 예외다('Listing a property'). "anything can be named"(Ousterhout & Martin 2025): 문장이 깔끔하다고 응집이 증명되지는 않는다(미탐). 그래서 판정이 아니라 경고여야 한다.

10. **책임 줄에는 짧은 맥락을 곁들이거나 맥락이 있는 곳을 둔다. 한 줄은 인터페이스 전체를 담지 못한다.**
    - 근거: CRC 카드만 받은 고객은 맥락 없이 이해하지 못했다. RDD 는 목적문(무엇이고 무엇이 아닌지)과 두 문단 이하의 설계 이야기를 함께 쓴다. Ousterhout 는 쓰는 사람이 알아야 하는 비형식적 지식도 인터페이스이며 주석으로만 적을 수 있다고 한다.
    - 출처: Beck & Cunningham 1989; Wirfs-Brock & McKean 2003, pp.80–81, 94–95; Ousterhout 2018a [2차 출처]; Ousterhout & Martin 2025
    - 근거 강도: 전문가 의견. 약~중
    - 반론과 한계: Martin 은 주석을 잠재적 오정보로 본다(Ousterhout & Martin 2025).

11. **공통 코드는 복사본들이 같은 지식을 담아 같은 이유로 바뀐다는 것이 드러났을 때 떼어 낸다(관례상 세 번째 사례). 우연히 닮은 코드는 중복을 허용한다.**
    - 근거: "duplication is far cheaper than the wrong abstraction", 잘못된 추상은 인라인으로 되돌린다(Metz). 3의 규칙, AHA. 1974년 논문의 "Eliminate duplicate functions but not duplicate code"와 GET CARD 예(우연히 묶인 공통 모듈은 한 호출자의 변경이 나머지를 깨뜨린다). DRY 는 코드가 아니라 지식의 중복에 관한 것이다.
    - 출처: Metz 2016; Fowler 1999 [2차 출처]; Dodds 2020; Stevens et al. 1974; Thomas & Hunt 2019 [2차 출처]; Brown 2011
    - 근거 강도: 전문가 의견 + 실증(양쪽으로 갈림: Juergens et al. 2009 [2차 출처], 5개 시스템; Kapser & Godfrey 2008 [2차 출처], 2개 시스템, 저자 분류). 중
    - 반론과 한계: 단순 설계는 중복 제거를 높은 순위에 두고 명료성을 위한 중복을 "papering over a problem"이라 본다(Fowler 2015). 기다리는 동안 복사본의 비일관 변경이 결함을 낳는다(Juergens et al. 2009 [2차 출처]). 3의 규칙이나 AHA 를 직접 시험한 연구는 없다.

12. **의존성 역전(추상 인터페이스)은 예측된 변동 지점, 구현이 여럿인 곳, 거리나 변동성이 큰 경계에만 둔다.**
    - 근거: PV 는 예측된 변동 지점에 쓰고 "pick your battles", 중급자는 쓰이지 않을 유연성에 기운다(Larman). 구현이 많을수록 인터페이스가 깊다(Ousterhout). 계약 결합은 거리나 변동성이 클 때 값을 한다(Khononov). 한 부류의 변경에 대한 분리는 다른 부류에 대한 결합을 키운다(Beck). 증상 없이 원칙을 적용하지 말라(Martin & Martin 2006).
    - 출처: Larman 2001; Ousterhout 2021 [2차 출처]; Khononov n.d.; Beck 2023 [2차 출처]; Metz 2016; Martin & Martin 2006
    - 근거 강도: 전문가 의견. 중
    - 반론과 한계: Martin 은 DIP 를 순환을 끊는 두 방법의 하나로 두고(1996년 글은 DIP 를 먼저, 2000년 글은 새 패키지를 먼저 적는다), 안정 추상 원칙(SAP)으로 안정된 패키지를 추상적으로 만들라고 한다. SAP 는 DIP 의 재진술이라고도 했다(Martin 1996; Martin 1997; Martin 2000). 변동 지점은 미리 알기 어렵다(결합은 밟기 전에는 드러나지 않는다. Beck 2023 [2차 출처]).

13. **모듈 사이 의존 그래프에는 순환을 두지 않는다. 순환은 공통 부분을 새 패키지로 떼어 내거나 의존성 역전으로 끊는다.**
    - 근거: ADP "The dependencies betwen packages must not form cycles". 순환은 격리, 단위 테스트, 릴리스를 어렵게 한다. Page-Jones 의 도메인 규칙도 낮은 도메인이 높은 도메인에 묶이면 재사용이 어렵다고 한다.
    - 출처: Martin 1996; Martin 2000; Wirfs-Brock & McKean 2003, pp.135–136(Page-Jones 인용)
    - 근거 강도: 형식 논증 + 전문가 의견. 중. 직접 실증 없음
    - 반론과 한계: ADP 의 경제적 근거(별도 릴리스, 재검증, 재배포 비용)는 한 패키지 안에서는 약해진다(노트의 추론). 두 처방의 순서는 글마다 다르다.

14. **의존은 덜 변하는(바꾸기 어려운, 안정된) 쪽을 향하게 한다.**
    - 근거: SDP "Depend in the direction of stability". Metz "Depend on things that change less often than you do". Larman: 문제는 특히 불안정한 것에 대한 결합이다. Khononov 의 변동성 차원.
    - 출처: Martin 1997; Martin 2000; Metz 2012 [2차 출처]; Larman 2002; Khononov n.d.
    - 근거 강도: 정의(I 지표) + 전문가 의견. 약~중. 패키지 지표와 결함, 이해도의 상관을 본 실증이 있으나 단일 시스템이거나 소표본이다(Elish et al. 2011 [2차 출처], Eclipse; Elish 2010 [2차 출처], 18개 패키지)
    - 반론과 한계: 안정성은 바뀔 확률이 아니라 바꾸기 어려운 정도다. Martin 스스로 "a metric is not a god"이라 했고 이상적인 패키지는 절반쯤이라 했다(Martin 1997). Ce 를 세는 단위가 글마다 다르다(노트의 추론). 변동성은 커밋 수가 아니라 도메인 판단이다(Khononov n.d.).

15. **모듈 바깥에는 좁은 공개면만 보이고, 비공개 내부에 기대는 통합(침투 결합)은 막는다.**
    - 근거: 침투 결합은 "the most fragile and implicit"(Khononov). 수줍은 코드와 데메테르 법칙(Hunt & Thomas). RDD 퍼사드는 "a restricted set of responsibilities"를 가진 내부 인터페이서이고, 1990년 책은 서브시스템 안팎의 통신을 모으고 계약 수를 줄이라 했다. 깊은 모듈과 과다 노출(overexposure) 적신호(Ousterhout).
    - 출처: Khononov n.d.; Hunt & Thomas 2003; Wirfs-Brock & McKean 2003(5장); Wirfs-Brock et al. 1990 [2차 출처]; Ousterhout 2018a [2차 출처]
    - 근거 강도: 전문가 의견 + 형식 논증. 중
    - 반론과 한계: 데메테르의 대가는 작은 감싸기 메서드다(Hunt & Thomas 2003). 그대로 넘기는 메서드는 얕은 모듈의 적신호다(Ousterhout 2018b). Fowler 는 Tell, Don't Ask 를 쓰지 않는다(Fowler 2013). RDD 의 퍼사드는 자기 책임을 가진 설계된 객체여서 생성된 재내보내기 목록과는 다르다(노트의 추론).

16. **구조 규칙과 지표는 판정보다 질문과 경고로 내놓고, 고치는 순서를 함께 준다.**
    - 근거: 실무 원칙들은 처방을 순서와 함께 준다. CRC(다시 쓰기, 그다음 나누기), Beck(응집된 부분 떼어 내기 또는 결합 안 된 부분 옮기기), Martin(새 패키지 또는 DIP), Brown(강한 connascence 를 이름 결합으로), Metz(잘못된 추상은 인라인으로 되돌리기). 원저자들은 자기 규칙을 판정으로 쓰지 말라고 한다. Martin "a metric is not a god", Hunt & Thomas 의 데메테르는 "more of a good idea than a physical constant", Rutherford 는 아홉 형태 목록이 예시였다고 하며, 1974년 문법 시험은 틀릴 수 있다. North 는 원칙이 통과와 위반만 가르는 규칙이 되는 것을 경계한다.
    - 출처: Beck & Cunningham 1989; Beck 2022; Martin 1996; Martin 1997; Brown 2011; Metz 2016; Hunt & Thomas 2003; Rutherford 2022; Stevens et al. 1974; North 2022
    - 근거 강도: 전문가 의견. 중
    - 반론과 한계: 실증 없음. LLM 의 SOLID 위반 판정은 코드가 복잡할수록 크게 나빠져(Pehlivan et al. 2025 [2차 출처]), 판단을 요구하는 질문을 에이전트가 늘 같게 처리한다는 보장이 없다.

17. **모듈 구성은 처음부터 고정되지 않고 자라면서 흔들린다. 합치기와 나누기를 주기적으로 다시 본다.**
    - 근거: 패키지 구조는 위에서 아래로 설계할 수 없고 "jitters and grows"(1996), 구성은 "jitter and evolve"(2017). Beck 은 대부분의 설계 결정이 되돌릴 수 있고 정리는 시점을 고르는 경제적 선택이라 본다. Metz 는 매몰 비용에 끌리지 말고 잘못된 추상을 되돌리라고 한다.
    - 출처: Martin 1996; Martin 2017 [2차 출처]; Beck 2023 [2차 출처]; Metz 2016
    - 근거 강도: 전문가 의견. 중
    - 반론과 한계: 실증 없음. 언제 다시 볼지의 기준은 출처마다 없다.

## ln-structure 시사점

### 뒷받침

1. **책임 한 줄에 무엇을 맡는지만 적고 어떻게 하는지(기능 나열, 알고리즘, 처리 단계, 함수 이름)는 적지 않는 규칙.** RDD 는 책임을 속성이나 연산 목록보다 한 단계 높은 진술로 적게 하고, CRC 교육 경험은 "what, rather than how"를, Hunt & Thomas 는 요구처럼 들리는 높은 수준의 호출을 권한다. 출처: Wirfs-Brock & Wilkerson 1989; Wirfs-Brock & McKean 2003, pp.128–131; Biddle et al. 2002; Hunt & Thomas 2003; Stevens et al. 1974(2장)
2. **책임을 모듈(폴더)에 두는 것.** 1990년 책은 클래스와 서브시스템의 책임이 규모만 다르다고 보고, 서브시스템 카드에 "Responsible for…" 한 줄과 계약 목록을 두어 계약마다 안쪽 클래스에 위임했다. 모듈 한 줄에 파일(클래스)별 세부 책임이 딸린 ln 의 구성과 가장 가까운 선례다. 2003년 책은 이웃(neighborhood)과 서브시스템도 응집된 전체여야 한다고 하고, Larman 은 PV 를 서브시스템과 애플리케이션까지 적용하며, Khononov 는 설계가 프랙털이라 모든 수준에 같은 모형을 쓴다. 출처: Wirfs-Brock et al. 1990 [2차 출처]; Wirfs-Brock & McKean 2003, p.145; Larman 2001; Khononov 2026
3. **"책임으로 써 보면 같은 일을 맡은 모듈이 여럿인지 드러난다"는 프로토콜 문장과, 층 표면의 이름 충돌을 같은 책임을 두 모듈이 주장하는 설계 오류로 보는 것.** RDD 의 "Don't overlap responsibilities", "Keep information about one thing in one place", DRY 의 단일 권위 표현, 직교성이 같은 방향이다. 출처: Wirfs-Brock & McKean 2003; Thomas & Hunt 2019 [2차 출처]
4. **모듈 사이 순환 금지와 모듈 안 파일 사이 순환 허용.** ADP 는 패키지 사이의 규칙이다. Page-Jones 는 경계 안의 connascence 를 최대화하라 하고, Beck 은 결합된 요소를 같은 요소 안에 두라 하며, Ousterhout 는 긴밀한 두 코드는 합치라 하고, 1990년 책은 강하게 결합된 객체를 같은 서브시스템에 두라 한다. 출처: Martin 1996; Martin 2000; Page-Jones 1992 [2차 출처]; Beck 2022; Ousterhout & Martin 2025; Wirfs-Brock et al. 1990 [2차 출처]
5. **층을 의미 없이 의존으로 계산하는 것.** Martin 은 패키지 구조를 위에서 아래로 설계할 수 없고, 패키지 의존 그림은 기능 설명과 거의 무관한 빌드 지도라고 했다. 출처: Martin 1996. (의미 수준과의 차이는 아래 '도전' 7번)
6. **표면으로만 import 하고 모듈은 표면만 공개하는 것.** 비공개 인터페이스로 통합하는 침투 결합을 기계적으로 막는다. 수줍은 코드, RDD 퍼사드와 1990년 책의 '서브시스템 안팎 통신 모으기, 계약 수 줄이기', Ousterhout 의 인터페이스와 구현 분리가 같은 방향이다. 출처: Khononov n.d.; Hunt & Thomas 2003; Wirfs-Brock & McKean 2003; Wirfs-Brock et al. 1990 [2차 출처]; Ousterhout 2018a [2차 출처]
7. **의존성 역전을 최후 수단으로 두고 1:N 플러그인과 패키지 밖 코드에 한정하며, 연결은 진입점에서만 하는 것.** Larman 의 "pick your battles", 구현이 많을수록 인터페이스가 깊다는 Ousterhout 의 관찰과 장치 드라이버 예(1:N 이 바로 그 경우), 거리나 변동성이 클 때만 계약이 값을 한다는 Khononov, 저수준 구성 요소를 고수준의 플러그인으로 보는 Martin, Modem 예의 "Nobody except main needs to know that it exists", Metz 와 AHA 의 투기적 추상 경고가 모두 뒷받침한다. 출처: Larman 2001; Ousterhout 2021; Khononov n.d.; Martin 2017 [2차 출처]; Martin & Martin 2006; Metz 2016; Dodds 2020
8. **해결 순서의 '1:1 상호 호출이면 한 모듈로 합치기'.** 양방향으로 함께 쓰이면 합칠 징후라는 Ousterhout, 너무 작은 역할은 다시 합치라는 RDD, 강한 결합은 가까이 두라는 Khononov 와 Page-Jones 가 뒷받침한다. 출처: Ousterhout 2021 [2차 출처]; Ousterhout & Martin 2025; Wirfs-Brock & McKean 2003, p.134; Khononov n.d.; Page-Jones 1992 [2차 출처]
9. **import 부수효과로 스스로 등록하는 방식의 금지와, 역전을 명시 상속으로 선언하는 것.** 숨은 등록은 실행 순서와 동일성에 기대는 동적 connascence 이고, 동적 형태는 소스만 보고 알아낼 수 없어 더 강하다. 불분명함(obscurity)은 Ousterhout 가 꼽은 복잡성의 두 원인 가운데 하나이고, 1974년 논문은 공통 데이터 영역과 전역 변수가 막대한 연결을 만든다고 했다. 이 대응은 노트의 추론이다. 출처: connascence.io n.d.; Khononov n.d.; Ousterhout 2021, p.99; Stevens et al. 1974
10. **Rust 의 impl 을 그 타입이나 트레이트의 모듈 안에 두는 것.** "Keep behavior with related information"과 GRASP 의 정보 전문가, 누출된 지식을 한 곳으로 모으라는 Ousterhout, 강한 결합을 가까이 두라는 Khononov 와 맞는다. 출처: Wirfs-Brock & McKean 2003; Larman 2002; Ousterhout 2018b; Khononov n.d.
11. **사람이 책임을 정하고 에이전트가 구현하는 분업, 그리고 기계 규칙은 결정적으로 두고 판단이 드는 것은 책임 줄과 review 질문으로 넘기는 구성.** RDD 는 책임 배정을 구현보다 앞에 둔다. Martin 의 행위자는 조직 지식이라 코드에서 추론할 수 없고, 이름은 무엇에든 붙일 수 있으며(Ousterhout), LLM 의 SOLID 위반 판정은 복잡한 코드에서 크게 나빠진다. Ousterhout 는 AI 가 코드를 쓸수록 설계가 더 중요하다고 했다. 이 묶음은 이 파일의 종합이다. 출처: Wirfs-Brock & Wilkerson 1989; Martin 2014; Martin 2017 [2차 출처]; Ousterhout & Martin 2025; Pehlivan et al. 2025 [2차 출처]; Pragmatic Engineer 2025 [2차 출처]
12. **위반을 해결 방법과 함께 돌려주는 것(판단 기준 2).** 실무 원칙들은 처방을 순서와 함께 준다(규칙 후보 16). 출처: Beck & Cunningham 1989; Beck 2022; Martin 1996; Brown 2011; Metz 2016
13. **`lnt review` 가 우회 의존, 고아 모듈, 클래스가 여럿인 파일, 숨은 타입 노출을 판정이 아닌 질문으로 보이는 것.** 원저자들이 자기 규칙과 지표를 판정이 아니라 지침으로 읽으라고 한 것과 맞는다. 출처: Martin 1997; Hunt & Thomas 2003; Rutherford 2022; Stevens et al. 1974; North 2022

### 도전하거나 어긋나는 것

1. **'책임'의 층위가 다르다.** ln 의 '모듈마다 책임 하나'는 RDD 의 역할이나 목적 수준이다. RDD 의 '책임'은 한 객체에 여럿 있는 짧은 진술이다. Booch 와 Henney 는 클래스마다 책임 몇 개를 정상으로 본다. 보고서와 프로토콜에서 두 뜻을 섞지 않아야 한다. 출처: Wirfs-Brock & McKean 2003; Henney 2012; Dunn 2021 [2차 출처]
2. **책임의 기준이 Martin 과 다르다.** ln 의 한 줄은 내용 기준(무엇을 맡는가, 무엇에 답하는가)이고, Martin 의 2014/2017 SRP 는 행위자 기준이다. Employee 는 한 개념을 맡아도 행위자가 셋이라 SRP 위반이므로, ln 의 한 줄을 통과해도 Martin 의 SRP 는 실패할 수 있다. 반대로 North 는 내용과 형식처럼 함께 바뀌는 것을 가르면 인위적 이음매가 생긴다고 한다. 출처: Martin 2014; Martin 2017 [2차 출처]; North 2022
3. **모든 모듈에 단일 책임을 강제하면 과분할 쪽으로 기울 수 있다.** Martin 자신의 조건부 SRP(증상 없이 나누면 Needless Complexity), Cecconi 의 '메서드 하나짜리 클래스 백만 개', Ousterhout 의 클래스염, RDD 의 너무 작은 역할과 접착 객체, Olano 의 '국소 복잡성을 위로 밀어 올림'과 부딪힌다. Wirfs-Brock 은 데이터 중심 설계의 모습을 '단순한 정보 보유자가 많고 저수준 메시지가 많은' 구조로 그린다. Mayes 는 RDD 자체도 남의 데이터에 작용하는 서비스 하나짜리 클래스를 낳을 수 있다고 했다. 1파일 1클래스, 타입만 공개, 함수를 정적 메서드로 두는 규칙이 겹치면 이런 클래스(남의 데이터에 작용하는 정적 메서드 묶음)가 늘 수 있다. 마지막 문장은 노트의 추론이고 실증은 없다. 출처: Martin & Martin 2006; Cecconi 2014 [2차 출처]; Ousterhout 2018a [2차 출처]; Wirfs-Brock & McKean 2003, pp.134, 137; Wirfs-Brock 2014; Mayes 1992; Olano 2025 [2차 출처]
4. **그대로 넘기는 메서드와 얕은 층이 생길 수 있다.** 중첩 모듈이 맨 위 안쪽 층만 공개하고 모든 접근이 표면을 거치면, 받은 호출을 넘기기만 하는 메서드나 추상이 비슷한 이웃 층이 생기기 쉽다. Ousterhout 는 이를 적신호로 보고, Hunt & Thomas 는 데메테르의 대가로 작은 감싸기 메서드를 든다. RDD 의 퍼사드는 자기 책임을 가진 설계 객체이지 생성된 재내보내기가 아니다. 출처: Ousterhout 2018b; Ousterhout 2018a [2차 출처]; Hunt & Thomas 2003; Wirfs-Brock & McKean 2003(5장)
5. **같은 층 import 금지가 추상을 서두르게 만든다.** 형제 모듈이 같은 로직을 필요로 하면 중복하거나 아래 층으로 떼어 내야 하고, ln 의 해결 순서는 '공통 부분 떼어 내기'를 역전보다 앞에 둔다. 3의 규칙, AHA, 잘못된 추상, 1974년 GET CARD 예는 우연히 닮은 코드를 일찍 떼어 내는 쪽을 더 비싼 실수로 본다. 떼어 낼 조건(같은 지식인가)은 프로토콜에 없다. 반대로 import 가 막힌 에이전트가 로직을 복제하면 드러난 이름 결합이 숨은 기능 결합으로 바뀐다. 이는 가설이고 데이터가 없다. 출처: Metz 2016; Fowler 1999 [2차 출처]; Dodds 2020; Stevens et al. 1974; Khononov n.d.; Juergens et al. 2009 [2차 출처]
6. **import 그래프가 보지 못하는 결합이 있다.** 기능, 의미, 알고리즘, 값, 실행 순서 결합과 뒷문 누출, 시간적 분해는 import 에 나타나지 않는다. Beck 의 정의로 결합은 변경에 상대적이고, 2026년 산업 연구에서 구조적 결합은 동시 변경과 약하게만 상관했다. ln 규칙은 낮은 변경 결합의 필요조건일 뿐 충분조건이 아니다. 출처: Beck 2023 [2차 출처]; Khononov n.d.; connascence.io n.d.; Ousterhout 2018a [2차 출처]; Liljas et al. 2026
7. **층의 방향과 의미.** Martin 의 '고수준'(정책, 가장 많이 의존받음)은 ln 에서 l0 쪽에 온다. ln 문서의 '상위/하위'(층 번호)는 Martin 의 high/low level 과 거꾸로이므로 그의 표현을 빌려 쓰면 안 된다. Martin 과 Page-Jones 의 층은 의미(입출력으로부터의 거리, 응용, 업무, 구조, 기반 도메인)로 정해지지만 ln 의 층은 계산되어 그 의미 점검이 빠진다. 출처: Martin 2017 [2차 출처]; Wirfs-Brock & McKean 2003, pp.135–136
8. **안정성과 변동성 차원이 없다.** 층 계산은 비순환을 보장할 뿐 SDP 를 보장하지 않는다. 예를 들어 l2 의 모듈 A(의존받는 곳 10, 의존 1, I≈0.09)가 l1 의 B(의존받는 곳 1, 의존 1, I=0.5)에 의존하는 것은 ln 에서 합법이지만 SDP 위반이다(노트의 계산). 자주 바뀌는 l0 모듈은 위의 모든 것을 흔든다(Metz 의 휴리스틱). Khononov 의 변동성 차원도 없다. 출처: Martin 1997; Martin 2000; Metz 2012 [2차 출처]; Khononov n.d.
9. **표면이 내부 모델 타입을 그대로 내보내면 모듈 사이 결합은 계약 결합이 아니라 모델 결합이다.** Khononov 라면 패키지나 크레이트, 팀 경계처럼 거리가 크거나 변동성이 큰 곳에 명시적 계약을 요구한다. 출처: Khononov n.d.
10. **Martin 의 패키지 경제학은 한 패키지 안에서 약해진다.** CCP, CRP, REP, ADP 의 경제적 근거는 별도 릴리스, 재검증, 재배포 비용인데, 한 Python 패키지나 Rust 크레이트 안의 폴더에서는 이 비용이 작다. 남는 근거는 이해와 변경 국소화다. Martin 은 Python 같은 동적 언어에는 재컴파일과 재배포를 강제하는 소스 의존이 없다고 했다. 출처: Martin 2000; Martin 2017 [2차 출처]; 노트의 추론
11. **세분도가 시간에 따라 바뀐다는 개념이 없다.** Martin 은 구성이 흔들리며 진화한다고 하고, Beck 은 정리의 시점(먼저, 나중, 안 함)을 경제적 선택으로 본다. 편집마다 검사하는 훅은 '나중'과 '안 함'을 없앤다. 에이전트의 리팩터링이 싸다는 점이 이를 정당화할 수는 있지만, 그것은 Beck 의 경제학을 적용한 것이 아니라 벗어난 것이다. 늘 함께 바뀌는 모듈을 합치라는 지침도 없다. 출처: Martin 2017 [2차 출처]; Beck 2023 [2차 출처]
12. **1파일 1클래스와 '함수는 정적 메서드로'에는 이 장의 출처가 결합상의 근거를 주지 않는다.** connascence 로 보면 어느 쪽이든 이름 결합이다(노트의 추론). Martin 은 1파일 1클래스면 I 를 계산하기 쉽다는 측정 편의만 말했고, Ousterhout 는 크기보다 깊이를 보며 200–2000줄 클래스도 괜찮다고 한다. 이 규칙의 근거(파일 이름이 세부 책임을 드러냄, 탐색 등)는 다른 장에서 찾아야 한다. 출처: connascence.io n.d.; Martin 1997; Ousterhout 2018b
13. **한 줄은 얇다.** CRC 카드는 맥락 없이 이해되지 않았고, RDD 는 목적문과 설계 이야기를 함께 쓰며, Ousterhout 는 인터페이스의 비형식적 지식을 주석으로 적어야 한다고 본다. ln 이 코드 밖 계약과 설계 이유를 마커 밖 Notes 에 짧게 적게 하는 것이 일부 보완한다. 출처: Beck & Cunningham 1989; Wirfs-Brock & McKean 2003; Ousterhout & Martin 2025

### 열린 질문

1. **책임 줄의 형식.** RDD 의 목적문("An X is a … that …", 무엇이 아닌지 포함), 짧은 책임 구, Larman 의 질문형("누가 X 를 아는가, 정하는가"), Ousterhout 의 점검표(이 모듈만 주는 가치, 핵심 지식, 드러낼 최소량), 변경 주체를 적는 꼴("…가 바뀔 때 바뀐다") 가운데 무엇을 권할까. 출처: Wirfs-Brock & McKean 2003, pp.94–95; Larman 2002; Ousterhout 2018b; Martin 2014
2. **정하거나 조율하는 모듈의 책임은 어떻게 적나.** RDD 는 아는 것, 하는 것, 정하는 것을 모두 일급 책임으로 보고 controller, coordinator 고정관념을 둔다. '무엇에 답하는지'라는 표현이 이런 모듈을 잘 담는지. 출처: Wirfs-Brock & McKean 2003
3. **책임 문장 린트의 정확도.** and/or, 시간어, 약한 동사, 대상 없는 술어를 잡는 린트의 오탐, 미탐률은 얼마인가. 한국어 책임 줄에서 'and/or'에 해당하는 표지(그리고, 또는, ~하고, ~거나, 쉼표)를 어떻게 잡나. 실증은 없다. 출처: Stevens et al. 1974; Metz 2012 [2차 출처]; Wirfs-Brock & McKean 2003
4. **길이 예산.** CRC 카드처럼 한 줄의 길이에 상한을 두고, 넘치면 '더 높은 수준으로 다시 쓰고, 그래도 안 되면 나누기'를 알릴까. 카드 크기의 효과를 잰 연구는 없다. 출처: Beck & Cunningham 1989; Biddle et al. 2002
5. **과분할 감지.** 깊이(표면 항목과 문서 길이 대비 숨은 코드), 그대로 넘기는 메서드, 양방향으로 함께 import 되거나 함께 바뀌는 모듈 쌍을 합치기 힌트로 보일 수 있나. 깊이의 축척 임의성과 줄 수 비율의 부풀리기 문제가 있다. 출처: Ousterhout 2021 [2차 출처]; Normand 2021; Pocock 2026
6. **같은 층 형제 모듈의 공통 코드를 떼어 낼 조건.** 같은 지식 시험, 세 번째 사용 문턱, 사람이 책임 줄에 남기는 결정 가운데 무엇으로 할까. 에이전트에게 중복 지식은 더 위험한가(복사본 하나를 놓쳐 비일관 변경이 생김) 덜 위험한가(찾아서 인라인하고 다시 떼어 내기가 쌈). 출처: Metz 2016; Fowler 1999 [2차 출처]; Juergens et al. 2009 [2차 출처]
7. **책임 줄의 '맡는다'에 DRY 의 힘을 줄까.** 두 모듈이 같은 지식을 맡는다고 적으면 알리는 것. 프로토콜은 이미 층 표면의 이름 충돌을 같은 책임을 두 모듈이 주장하는 설계 오류로 보는데, 이를 책임 문장 수준으로 넓힐지. 출처: Thomas & Hunt 2019 [2차 출처]; Wirfs-Brock & McKean 2003
8. **안정성과 변동성 자문.** SDP 위반(의존 방향으로 I 가 커짐)이나 많이 의존받는데 자주 바뀌는 바닥 모듈을 알릴까. 그렇다면 Ce 를 클래스로 셀지 모듈 사이 간선으로 셀지, 추상도 A 를 Python 의 ABC/Protocol 이나 Rust 트레이트로 어떻게 정의할지 정해야 한다. 사람이 모듈마다 변동성(핵심, 지원, 일반)을 적게 할지도 문제다. 출처: Martin 1997; Martin 2000; Metz 2012 [2차 출처]; Khononov n.d.
9. **동시 변경 이력으로 책임 분리를 검증할 수 있나.** 한 모듈의 파일은 함께 바뀌고 다른 모듈끼리는 덜 함께 바뀌는지 보는 것이 Beck 의 결합 정의와 CCP 를 운용하는 길이다. 에이전트의 커밋 패턴이 도메인 변경을 반영하는지는 모른다. 출처: Beck 2023 [2차 출처]; Martin 2000; Liljas et al. 2026
10. **정적 검사로 잡을 수 있는 경계 넘는 강한 결합.** 위치 인자(키워드 전용 인자나 매개변수 구조체 요구), 매직 리터럴(의미 결합), 모듈 사이 클론(알고리즘, 기능 결합), 중복 상수(값 결합). `lnt blast` 로 차수(의존받는 수)를 보일 수 있나. 출처: connascence.io n.d.; Brown 2011; Khononov n.d.
11. **표면에서 계약 타입과 모델 타입을 구분해 보일까.** 출처: Khononov n.d.
12. **구현이 하나뿐인 트레이트나 ABC 는 얕은 역전인가.** 1:N 이 실제로 생길 때까지 역전을 미루라고 명시할지. 출처: Ousterhout 2021 [2차 출처]; Larman 2001
13. **엄격한 층 구조와 협력 스타일.** 같은 층 import 금지와 '역전은 최후 수단' 아래에서 동료 객체끼리의 협력(모델이 뷰에 변경을 알리는 식)이나 분산 제어는 역전을 요구한다. RDD 저자들은 위임형 제어를 선호하고 프레임워크를 쓸 때는 그 제어 스타일을 따르라고 한다. ln 의 '진입점에서 조립'과 어떻게 맞물리는지는 노트의 추론 수준이다. 출처: Wirfs-Brock & McKean 2003, pp.196–200
14. **사람 중심 비용 모형이 AI 에이전트에도 옮겨지나.** 인지 부하, 조정 비용으로 정당화된 원칙들이 에이전트에게도 같은 무게를 갖는지, 에이전트가 ln 규칙 아래에서 과분할하는지 과소분할하는지 데이터가 없다. 출처: Ousterhout & Martin 2025; Khononov n.d.; Pehlivan et al. 2025 [2차 출처]
15. **Khononov 의 Claude Code 플러그인(vladikk/modularity)으로 경계를 교차 검토할 수 있나.** CC BY-NC-SA 4.0 과 AI 학습 제한이 재사용을 제한한다. 출처: Khononov 2026
16. **1974년 정지 규칙을 쓸까.** "no subset of elements that could be useful alone"과 한 번에 파악할 수 있는 크기를 너무 굵거나 너무 잘게 나눈 모듈의 지침으로 삼을지. 출처: Stevens et al. 1974(2장)
17. **효과의 증거.** 책임을 사람이 먼저 정하는 분해가 유지보수성을 높인다는 통제된 증거는 이 장의 출처에 없다(RDD, CRC, GRASP, SRP, 깊은 모듈, connascence, 균형 결합 모두). ln-structure 의 효과를 주장하려면 자체 평가가 필요하다. 출처: Svetinović et al. 2005; Beck & Cunningham 1989; Ousterhout 2024; Rutherford 2022

## 이 파일에만 나오는 출처

- Fowler, M. (2013). "TellDontAsk." martinfowler.com, 2013-09-05. https://martinfowler.com/bliki/TellDontAsk.html
- Martin, R. C. (1997). "Stability." *C++ Report* (Engineering Notebook 칼럼 6). http://web.archive.org/web/2011/http://www.objectmentor.com/resources/articles/stability.pdf
- Elish, M. O. (2010). 패키지 수준 지표와 이해도. ICPC 2010. https://doi.org/10.1109/ICPC.2010.43 [2차 출처: 초록]
- Wirfs-Brock, R. (2014). "Object Design Roots and New Directions." 발표 슬라이드. https://wirfs-brock.com/rebecca/assets/documents/ObjectDesignRoots.pdf
