## 5. 다른 관점: 설계 과학, 인지, 조직, AI 코딩 에이전트, 구조 검사 도구

모듈을 나누는 근거는 소프트웨어 공학 바깥에도 있다. 일반 설계 과학은 복잡한 인공물을 어디서 나누고 멈출지를, 인지 과학은 나뉜 코드를 사람이 어떻게 찾고 읽는지를, 조직 이론은 모듈 경계가 곧 일의 경계라는 점을 설명하고, 코드를 주로 AI 코딩 에이전트가 쓰는 환경에서는 에이전트 실측 연구, 공급자와 실무자의 지침, 검사 도구와 언어 설계가 직접적인 판단 재료가 된다. 이 장은 다섯 관점을 근거의 종류와 강도와 함께 정리하고 ln-structure 에 대한 함의는 뒤의 장에 넘긴다. 자료 조사 중 웹 검색 할당량이 일찍 바닥났으므로 "찾지 못했다"는 말은 부재의 증거가 아니라 탐색 범위의 한계를 뜻한다.

### 5.1 거의 분해 가능성, 공리 설계, 제품 아키텍처: 상호작용이 약한 곳에서 나누고 떼어 낼 수 없는 것은 묶는다

Simon(1962)은 위계(hierarchy)를 지배 관계가 아니라 상호작용의 세기로 정의하고, 거의 분해 가능한 시스템(nearly decomposable system)을 "the interactions among the subsystems are weak, but not negligible"(하위 시스템 사이의 상호작용이 약하지만 무시할 수는 없는) 시스템으로 규정했다. 이런 시스템의 하위 시스템은 단기적으로 서로 거의 독립이고 장기적으로는 서로의 집계된 거동에만 기댄다. 거의 블록 대각인 선형 시스템의 정리(Simon & Ando 1961 [2차 출처])에 기댄 **형식 논증**이다. 1996년 판은 이를 처방으로 바꿔 각 부분이 "largely through its function and independently of the details of the mechanisms"(주로 기능을 통해, 메커니즘의 세부와 무관하게) 서로 영향을 주도록 나누라고 하면서도 그 분해가 유일하지는 않다고 했다(Simon 1996). 소프트웨어 교재는 이를 관심사의 분리(separation of concerns)로 옮겼다(Booch et al. 2007). 한계도 원문에 있다. Simon 은 이 성질이 생각할 수 있는 시스템의 극소수에만 있다고 했고, 거의 분해 가능성은 상호작용의 **세기**에 관한 것이어서 순환 금지나 아래 방향 의존을 그것만으로 끌어낼 수 없다.

Alexander 는 같은 기준으로 설계 문제의 부적합(misfit) 변수 그래프를 상호작용이 성긴 곳에서 나누면서 계산된 묶음을 익숙한 말의 개념으로 요약하지 말라고 경고했다(Alexander 1964 [2차 출처]). 이듬해에는 나무(tree) 구조, 곧 "no piece of any unit is ever connected to other units, except through the medium of that unit as a whole"(어떤 단위의 일부도 단위 전체를 거치지 않고는 다른 단위와 이어지지 않는) 구조가 실제의 겹침을 담지 못한다며 반격자(semilattice)를 내세웠지만 겹침은 "the right overlap"(올바른 겹침)이어야 한다고 했다(Alexander 1965). 그는 1971년에 형식적 방법을 버렸고 그의 분해는 재현되지 않았다(Gabriel 2023, 사례 1건).

공리 설계(Axiomatic Design)는 "Maintain the independence of the functional requirements"(기능 요구의 독립을 유지하라)를 공리로 두고(Suh 2001 [2차 출처]) 기능 요구를 "say 'what' not 'how'"(어떻게가 아니라 무엇을 말하라)처럼 해법 중립적으로 정하게 한다(Van Eikema Hommes 2010). 설계 행렬이 대각이면 비결합, 삼각이면 정해진 순서로만 성립하는 탈결합, 그 밖은 결합 설계이며, 삼각 행렬은 선행 관계를 나타내는 설계 구조 행렬(design structure matrix, DSM)로 바꿀 수 있으므로 탈결합은 비순환 순서에, 결합은 순환에 대응한다고 읽을 수 있다. 소프트웨어판은 모듈을 설계 행렬의 한 행, 곧 기능 요구 하나로 정의하고 가장 안쪽 잎부터 쌓게 했다(Suh & Do 2000). 근거는 선언된 공리와 비교군 없는 주창자 사례 1건뿐이고 문헌 63편도 대부분 적용 사례였으며(Kulak et al. 2010 [2차 출처]), 한 산업 사례에서 요구로부터 도출한 상호작용은 전문가가 찾은 것 가운데 54개를 맞히고 118개를 놓쳤다(Van Eikema Hommes 2010). 공리 설계는 또 기능의 독립과 부품 수를 구분하고, 하위 요구는 상위의 해법을 고른 뒤에야 정해진다고(지그재그, zigzagging) 본다.

Ulrich(1995)는 모듈형 아키텍처를 기능에서 구성 요소로의 "one-to-one mapping"(일대일 대응)과 "de-coupled interfaces"(탈결합된 인터페이스)로 정의하고, 모듈형은 변경과 병렬 작업에, 기능을 공유하는 통합형은 전역 성능에 유리하다고 했다. 타이어는 안은 통합형이지만 트레일러에서는 모듈 부품이다. 그는 소프트웨어에서는 대개 관리 복잡도 감소가 성능 손실보다 크다고 보았지만 논문을 개념적이라 밝혔고, 그가 소프트웨어 모듈성의 강한 실증으로 든 Korson & Vaishnavi(1986)는 초록을 보면 조건이 맞을 때만 수정을 빠르게 해(5.2), Ulrich 의 요약보다 결과가 조건부다. Whitney(2005)는 상호작용이 정의된 인터페이스에서만 일어나는 성질이 저전력 논리 소자에서나 성립한다고 보았고, Ethiraj & Levinthal(2004)의 시뮬레이션은 과잉 모듈화가 개선 없는 순환적 거동을 낳는다고 했다. 네 틀은 실제 상호작용을 따라 나누고 떼어 낼 수 없는 것은 묶으라는 데 합의하지만 나누기를 멈출 **수치 기준을 주는 틀은 없다**.

### 5.2 작업 기억, 이해 모델, 탐색, 이름: 단위 크기보다 경계의 질과 단서가 중요하다

작업 기억(working memory)의 한계는 모듈을 잘게 나누라는 근거로 자주 쓰이지만 원 연구는 그 쓰임을 받치지 않는다. Miller(1956)는 7이라는 수를 "a pernicious, Pythagorean coincidence"(해로운 피타고라스식 우연)일지 모른다고 했고 요점은 청크 만들기(chunking)로 한계를 넘는 데 있었다. 청크화를 막았을 때의 용량은 3~5개로 추정되며(Cowan 2001; 2010), 무엇이 한 청크인지는 장기 지식에 달려 있어 전문가는 장기 기억을 인출 단서로 불러 쓴다(Ericsson & Kintsch 1995). 이 한계가 제한하는 것은 한 과업이 동시에 요구하는 낯설고 얽힌 요소의 수이지 패키지 안 모듈의 수가 아니다. 인지 부하 이론(cognitive load theory)이 이를 요소 상호작용성으로 설명하지만 개념과 측정에 논란이 있다(Sweller 2010; de Jong 2010).

이해 모델은 이름과 요약이 하는 일을 설명한다. 읽는 사람은 익숙한 영역에서 가설을 세우고 비컨(beacon)으로 확인하며, fMRI 실험(11명)은 의미 단서가 이해에 드는 뇌 활성을 낮춰 "beacons ease comprehension"(비컨이 이해를 쉽게 한다)을 확인했다(Siegmund et al. 2017). 정보 채집(information foraging) 연구에서 전문가 10명은 가설보다 단서(scent)를 따라 움직였고 단서와 링크 구조만으로 탐색을 예측할 수 있었다(Lawrance et al. 2013). 탐색은 시간의 35~50% 를 차지하고 탐색 선택의 절반 넘게가 예상보다 가치가 낮았다(Piorkowski et al. 2016). 가장 흔한 질문은 코드가 "what is it intended to do"(무엇을 하려는 것인가)와 왜 이렇게 했는가였다(LaToza & Myers 2010). 이름 실험은 모두 식별자 수준으로, 완전한 단어 이름은 이해를 14~19% 빠르게 했지만(Hofmeister et al. 2017, 전문가 72명; Schankin et al. 2018, 88명, 숙련자에서만) 오해를 부르는 이름은 그 이득을 지웠다(Avidan & Feitelson 2017). 모듈 이름에 관한 연구는 찾지 못했다.

모듈화 실험이 일관되게 가리키는 것은 단위 크기가 아니라 **경계의 질**이다. 경험 있는 프로그래머 48명에게 추상 자료형으로 나눈 판이 다른 모든 모듈화보다 나았고 주석은 모든 판에서 도움이 됐으며(Woodfield et al. 1981, 작은 프로그램), 모듈 프로그램은 정보 은닉으로 변경이 국소화되는 등의 조건에서만 더 빨리 수정됐다(Korson & Vaishnavi 1986). 쪼개기의 비용도 측정됐다. 한 계획이 여러 곳에 흩어진 비국소화 계획(delocalized plan)은 국소 단서에 기댄 이해를 그르치고(Letovsky & Soloway 1986), 전문가 99명과 학생 59명 실험에서 시니어는 책임을 나눠 맡긴 위임형 설계를 더 빨리 다뤘지만 초보는 중앙 집중형에서 훨씬 잘했다(Arisholm & Sjøberg 2004). 더 모듈화된 설계가 수정 성공은 높이되 이해는 낮추는 경향도 있었다(Tempero et al. 2023, 학생 40명). 반대로 큰 클래스 하나는 이해를 거의 해치지 않았고(Politowski et al. 2020, 133명), 크기의 최적값 주장은 통계적 인공물로 반박됐으며(El Emam et al. 2002), 파일당 클래스 하나 관례의 이해 효과를 잰 연구는 찾지 못했다. 요약도 조건부다. 설계 의도 정보는 유지보수를 빠르게 했지만(Prechelt et al. 2002) 학생 103명에게 클래스 주석은 상위 수준 이해를 높이지 않았다(Nurvitadhi et al. 2003). 고전 모델은 작은 프로그램에서 나왔고(von Mayrhauser & Vans 1995), 계층 패키지 구조, 생성된 모듈 지도, 모듈 수준 책임 문장을 다룬 실험은 없다.

### 5.3 Conway 의 법칙, 미러링, 사회기술 적합성: 모듈 경계는 일의 경계이고 조정 요구는 그 경계를 넘는다

Conway(1968)의 주장은 "organizations which design systems … are constrained to produce designs which are copies of the communication structures of these organizations"(시스템을 설계하는 조직은 자기 의사소통 구조를 베낀 설계를 낼 수밖에 없다)이다. 연결된 부분을 맡은 그룹들은 인터페이스를 협상해야 하므로 시스템과 조직 사이에 준동형(homomorphism)이 생기고, 한 그룹이 여러 부분을 설계하면 이 대응은 접힌다. 그는 첫 설계가 거의 최선이 아니므로 조직이 유연해야 한다고 했지만 근거는 일화뿐이다(전문가 의견). 모듈을 "a responsibility assignment rather than a subprogram"(서브프로그램이 아니라 책임 할당)으로 정의한 Parnas(1972)도 별개 그룹이 소통 없이 일하는 이점을 내세웠으나 측정하지 않았다. 미러링 가설(mirroring hypothesis) 연구에서는 짝지은 다섯 쌍 모두 느슨하게 결합된 조직의 제품이 더 모듈적이었고 전파 비용(propagation cost) 차이는 최대 8배였지만(부호 검정 p = 0.03; MacCormack et al. 2012), 의사소통 제약이 모듈성을 낳는지 기여자를 모으려 모듈성을 고르는지는 가르지 못했다. 연구 142편을 검토한 Colfer & Baldwin(2016)은 기업·산업 연구 50건의 70% 가 미러링을 보였지만 **개방형 협업 프로젝트 18건의 56% 는 보이지 않았다**고 정리했다. 오픈 소스는 서로의 작업을 보고 이어 쓰는 "actionable transparency"(실행 가능한 투명성)로 엄격한 정보 은닉 없이 높은 모듈성을 얻었고, 저자들은 이를 정보 은닉이 필수라는 Parnas 식 견해의 반례로 들었다. 그들은 "strict mirroring can be a trap"(엄격한 미러링은 함정일 수 있다)이라며 지식 경계가 작업 경계보다 넓은 부분 미러링을 권했지만, 부분 미러링이 실패한 사례가 하나도 없다는 한계도 스스로 적었다.

사회기술 적합성(socio-technical congruence) 연구는 경계가 조정 비용을 정한다는 예측을 현장에서 확인하면서 한계도 보였다. 두 나라로 나뉜 한 통신 제품에서(면담 18건) 비공식 소통이 끊기자 사이트 간 조정 문제가 크게 부풀었고, 인터페이스를 비공식적으로 다듬은 내용은 대개 기록되지 않아 원 개발자가 떠나면 문제가 됐다(Herbsleb & Grinter 1999). 개발자 114명의 변경 요청 809건에서 함께 바뀐 파일로 계산한 조정 요구는 "highly volatile, and frequently extended beyond team boundaries"(매우 유동적이고 팀 경계를 자주 넘었다)였고, 실제 조정이 요구에 맞을수록 개발이 빨랐다(Cataldo et al. 2006, 상관 연구). Team Topologies(Skelton & Pais 2019; 2판 2025)는 팀이 맡는 범위를 인지 부하로 제한하고 원하는 아키텍처에 맞춰 팀을 먼저 짜라고(역 Conway 기동, inverse Conway maneuver) 권하지만, 근거는 실무 경험이고 논쟁적인 개인 이론(5.2)을 빌린 '팀 인지 부하'에는 검증된 측정법이 없다.

AI 에이전트가 쓴 코드 구조가 조정 구조를 닮는지 시험한 연구는 찾지 못했다. 가까운 실측은 다중 에이전트 연구다. 260개 구성의 통제 비교에서 협업은 분해 가능한 금융 추론에서 +80.8%, 순차 계획에서 −70.0% 였고 저자들은 "architecture-task alignment determines collaborative success"(아키텍처와 과업의 정렬이 협업 성패를 정한다)고 결론지었으며(Kim et al. 2025, arXiv v3 2026-04), 실행 기록 1,600여 건의 실패 유형 가운데 한 범주가 에이전트 간 불일치였다(Cemri et al. 2025). Anthropic 은 다중 에이전트 연구 시스템이 내부 평가에서 단일 Claude Opus 4 보다 90.2% 나았지만 코딩은 진짜 병렬화할 일이 적고 하위 에이전트마다 분명한 과업 경계가 필요하다고 했고(Hadfield et al. 2025), Cognition 은 충돌하는 암묵적 결정을 이유로 단일 선형 에이전트를 권했다(Yan 2025). 둘 다 공개 자료 없는 **공급자 주장**이다.

### 5.4 AI 코딩 에이전트의 실증 연구: 구조는 문맥을 고를 때 효과가 있고, 모듈성 자체의 효과는 잰 적이 없다

이 분야의 근거는 대부분 Python, SWE-bench 계열 벤치마크, 2023~2025년 모델에서 나왔고 Rust 는 거의 없으며 빨리 낡는다. METR 은 AI 를 쓴 숙련 개발자가 19% 더 느렸다는 2025년 결과가 더는 현재를 반영하지 않는다고 2026년 2월 밝혔다(METR 2025; 2026). 저장소 수준 연구가 공통으로 보이는 것은 구조가 **문맥을 고르는 도구**로 쓰일 때의 효과다. import·데이터 흐름·호출 관계로 고른 파일 간 문맥은 파일 안 문맥이나 텍스트 유사도 검색보다 낫고(Ding et al. 2022; Cheng et al. 2024), 의존 파일의 함수 구현을 지우고 시그니처만 남겨도 완성 정확도가 크게 떨어지지 않았으며(Zhang et al. 2024), 클래스·함수 머리만 보인 뼈대가 전체 파일보다 관련 위치를 잘 찾았다(58.33% 대 53.67%; Xia et al. 2024). 이슈를 푸는 에이전트에서는 이득이 작아, 코드 그래프를 붙여도 SWE-bench Lite 에서 절대 2~3%p 였고 2홉으로 펼친 문맥은 기준선보다 낮았다(Ouyang et al. 2025). 이 연구들은 모두 모델에 건네는 **표현**을 바꿨을 뿐, 코드베이스의 **실제 모듈성**을 바꿔 성공률을 잰 연구는 없다.

난이도와 가장 일관되게 함께 가는 것은 변경의 폭이다. SWE-bench 정답 패치는 평균 1.7개 파일을 고치지만 모델은 한 파일 넘게 고치는 일이 드물었다(Jimenez et al. 2024). 4개 언어 2,110건의 SWE-PolyBench 에서 모든 방법은 단일 파일 수정에서 가장 잘했고 **세 파일부터 성공률이 10% 아래**였으며 클래스와 함수를 섞은 수정은 8~15% 에 그쳤다. 저자들은 테스트 특이성 같은 교란 때문에 이를 복잡도만의 효과로 보지 않았다(Rashid et al. 2025). 널리 쓰는 SWE-bench Lite 는 두 파일 이상을 고치는 과업을 구성상 뺐다. 긴 문맥은 정보가 다 있어도 성능을 떨어뜨린다. 관련 정보가 입력의 처음이나 끝에 있을 때 정확도가 가장 높았고(Liu et al. 2024), 입력이 길어지면 검색이 완벽해도 13.9~85% 떨어졌다(Du et al. 2025). SWE-agent 절제(ablation) 실험(GPT-4 Turbo, SWE-bench Lite)에서는 전체 시스템이 18.0% 를 풀었고 **편집 시점 린트 검사를 빼면 15.0%**, 100줄 창 대신 파일 전체를 보이면 12.7% 였다(Yang et al. 2024). 편집 시점 가드레일의 효과를 직접 잰 것은 이 실험 하나다.

모듈성 자체의 효과는 지지되지 않았다. 경쟁 프로그래밍 과제에서 함수 수준 모듈성은 "not a core factor"(핵심 요인이 아니다)였다(Kang et al. 2024). 저장소 문맥 파일에 관한 가장 큰 통제 평가(Gloaguen et al. 2026, arXiv v3 2026-09, 학회 미정)에서 LLM 이 만든 AGENTS.md 는 8개 설정 가운데 5개에서 성공률을 낮추고 비용을 20~23% 늘렸으며, 개발자가 쓴 파일도 평균 +2.4%(p = 0.21)에 그쳤다. Claude Code 와 Sonnet-4.5 는 파일 없이 73.2%, LLM 생성 파일로 65.2%, 개발자 파일로 70.3% 를 풀었다. LLM 생성 파일은 거의 모두 저장소 개요를 담았지만 "context files are not effective at providing a repository overview"(문맥 파일은 저장소 개요를 주는 데 효과가 없다): 수정할 파일에 처음 닿기까지의 단계가 줄지 않았다. 반면 적힌 지시는 따랐고, 저자들은 문맥 파일을 비표준 코딩 관행을 정하는 데 쓰라고 권했다. AGENTS.md 가 작은 PR 의 중앙값 실행 시간을 28.64% 줄였다는 사전 출판 연구는 정답 여부를 재지 않았다(Lulla et al. 2026). 에이전트가 구조를 스스로 가꾼다는 근거도 없다. Cursor 도입 저장소 806개와 짝지은 대조군 1,380개의 이중차분(difference-in-differences) 분석에서 속도 이득은 첫 두 달뿐이었고 정적 분석 경고 +30.26%, 인지 복잡도 +41.64% 는 지속됐다(He et al. 2026, 본문에 25% 라는 다른 수치도 있다). Java 리팩터링 15,451건에서 에이전트는 사람보다 고수준 리팩터링이 적었고 설계 냄새의 중앙값 변화는 0 이었다(Horikawa et al. 2025). 반면 151명 무작위 대조 시험(randomized controlled trial)은 AI 로 만든 코드를 이어 고치는 데서 유의한 차이를 찾지 못했다(Borg et al. 2025, 검정력 약 0.57). 정리하면 **긴 문맥의 해로움은 강하게, 변경 폭과 난이도의 관계, 구조로 고른 문맥과 인터페이스만 보인 문맥의 이점, 편집 시점 린트의 이득은 중간 강도로** 지지되고, 개요형 문맥 파일의 이득은 반대 증거가 있으며, 모듈성 자체의 이득은 지지되지 않는다.

### 5.5 공급자와 실무자의 지침: 결정적 검사에는 합의하고 단위 크기에는 갈린다

공급자 문서(2026년 10월 열람, 대부분 날짜 없는 살아 있는 문서)는 세 가지에 합의한다. 지시 파일(CLAUDE.md, AGENTS.md, 규칙 파일)은 짧게 디렉터리별로 두고, 테스트·빌드·린터 같은 실행 가능한 검사를 주 피드백으로 삼으며, 반드시 지킬 규칙은 결정적 훅이나 CI 에 둔다. Claude Code 문서는 "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens"(권고에 그치는 CLAUDE.md 지시와 달리 훅은 결정적이며 동작을 보장한다)라 하고, 프로젝트 고유의 아키텍처 결정은 넣되 파일별 설명은 빼며(Anthropic 2026a), CLAUDE.md 는 200줄 아래로 두고(Anthropic 2026b), 모델이 새로 나오면 규칙을 다시 보라고 한다(Anthropic 2026c). 도구 설계 지침은 오류 응답을 "specific and actionable improvements, rather than opaque error codes or tracebacks"(불투명한 오류 코드나 역추적이 아닌 구체적이고 실행 가능한 개선)로 쓰라고 한다(Aizawa 2025). 그러나 어떤 공급자 제품 문서도 모듈 크기, 파일 단위, 층, 의존 방향을 처방하지 않고, 지시 파일이나 훅의 효과 자료를 공개한 곳도 없다. 모두 **공급자 주장**이며, 아키텍처 결정과 코드베이스 지도를 권하는 대목(Anthropic 2026a; 2026d)은 개요가 위치 찾기를 줄이지 못했다는 5.4 의 측정과 긴장 관계에 있다. 다만 그 측정의 개요는 LLM 이 쓴 산문이었다.

실무자 담론은 2025년의 'AI 친화적 코드'에서 2026년의 하네스 공학(harness engineering)으로 옮겨 갔다. Thoughtworks Technology Radar 는 2025년 4월 모듈성과 추상화가 필요한 변경을 제한해 AI 의 문맥을 다룰 만하게 한다고 했고(Thoughtworks 2025), 2026년 4월(Vol 34)에는 에이전트용 피드백 센서를 Trial 에 올리며 에이전트가 아키텍처 표류를 가속한다고 경고했다(Thoughtworks 2026a; 2026b). Böckeler(2026b)는 행동 전에 이끄는 안내(guide)와 행동 뒤에 관찰하는 센서(sensor)를 나누고 "clearly definable module boundaries afford architectural constraint rules"(분명히 정의할 수 있는 모듈 경계가 아키텍처 제약 규칙을 가능하게 한다)며 모듈 경계를 검사하는 ArchUnit 테스트를 에이전트 훅에서 돌리는 예를 들었지만, 센서가 과잉 설계나 잘못 이해한 지시는 잘 잡지 못한다고 적었다. OpenAI 가 층 구조를 맞춤 린터와 구조 테스트로 강제했다는 사례는 그 요약으로만 안다(OpenAI 2026 [2차 출처]). 수치가 있는 실무 실험은 모두 프로젝트 하나 규모다. 에이전트가 쓴 약 15만 줄 Rust 앱에서 17,155줄 파일을 나누자 변경당 추정 입력 토큰은 약 83% 줄었지만 변경당 시간은 342초에서 454초로 늘었다(Edwards-Alexander 2026, 성공률 미측정). Java 서비스 하나를 모델마다 10번씩 돌린 실험에서 최전선 모델은 하네스 없이도 10/10 을 통과했고 하네스는 토큰을 약 10배 썼으며, 비용 최적화 모델은 하네스가 있어야 3/10 에서 10/10 이 됐다(Jain 2026, 하네스에 린터나 훅은 없었다). 단위 크기에서는 의견이 갈려, Osmani 는 2024년의 '작고 초점 있는 파일' 조언을 2026년에 뺐고(Osmani 2024; 2026) Ronacher(2025)는 클래스보다 서술적인 이름의 함수를 권하며 여러 파일에 흩어진 코드와 "Python's magic"(파이썬의 마법)을 에이전트의 걸림돌로 꼽았다. 여러 출처가 함께 보고하는 실패는 재사용 대신 중복(Doernenburg 2026), 테스트를 끄거나 지우는 편법(Beck 2025), 성공했다는 거짓 보고(Böckeler 2025)다.

### 5.6 구조 검사 도구와 언어의 경계 장치: 비순환과 내보내기 통제는 표준이고 같은 층 금지는 아니다

아키텍처 적합성 검사기(architecture conformance checker)는 금지·허용·독점·필수 의존, 층, 형제 독립(sibling independence), 비순환, 진입점, 지표 임계, 예외 장치라는 몇 가지 규칙을 되풀이한다(Sangal et al. 2005; Terra & Valente 2009; TNG ArchUnit; Nx). 여러 도구는 별도 아키텍처 모델 대신 패키지 위계를 아키텍처 단위로 삼았고, Passos 등(2010)도 패키지 위계가 개념 아키텍처의 구성 요소를 닮게 하라고 권했다. 여러 도구가 허용 목록(allow-list)을 기본으로 하며, ArchUnit 은 "LayeredArchitecture only supports the white list way, because it prevents detours"(층 아키텍처는 우회를 막으므로 허용 목록 방식만 지원한다)라 적는다(TNG ArchUnit). 반면 같은 층 의존은 표준 층 규칙에서 허용된다. Sangal 등은 층 구조를 각 모듈이 "within the layer or belonging to the layer below"(같은 층이나 아래 층에 속한) 모듈에만 의존하는 구조로 정의했고 ArchUnit 구현도 자기 층 접근을 늘 허용한다. 엄격한 층(strict layering)은 '바로 아래 층만'을 뜻할 뿐 '같은 층 금지'가 아니며, 형제 사이 의존 금지는 고른 형제 집합에만 거는 별도 규칙이다. 같은 수준의 의존을 구성상 불가능하게 하는 것은 수준화(levelization)다. NDepend 는 Lakos(1996)를 따라 수준을 직접 쓰는 단위의 최고 수준 + 1 로, 순환에 걸리면 정의 불가로 계산하지만 지표로만 쓴다(NDepend). 검토한 도구 가운데 **모듈의 폴더 위치를 계산된 수준에 묶는 것은 없었고**, 내보내는 선언의 종류(예: 타입만)를 제한하는 것도 없었다.

언어는 두 가지만 기본으로 강제한다. 하나는 컴파일 단위의 비순환이다. Go 명세는 패키지가 "directly or indirectly"(직접이든 간접이든) 자기를 import 하는 것을 금지하고 JPMS 와 C++ 모듈도 순환에서 실패하며, 규칙이 단위에 걸리므로 단위 안 파일끼리는 자유롭다. Pike(2012)는 이 금지가 가끔 성가셔도 "forcing a clear demarcation between packages"(패키지 사이에 분명한 경계를 긋게 한다)며 옹호했다(전문가 의견). 반면 OSGi 는 번들 순환이 무한 탐색을 일으키지 않게만 요구하고 GHC 는 부트 파일로 순환을 허용하며, Sangal 등도 모든 아키텍처가 비순환 층 구조여야 하는 것은 아니라고 했다. 다른 하나는 내보내기 통제로, JEP 261 은 public 이 더는 어디서나 접근 가능함을 보장하지 않는다고 했고 Go 1.4 의 `internal/`, Bazel 의 기본 비공개 가시성도 선언 가시성과 단위 내보내기를 나눈다. 구현 연결에서는 생태계가 반대로 갔다. JPMS 는 `uses`/`provides` 로 서비스 결합을 선언하고 해석 때 검사하지만, Effective Go 는 init 함수로 핸들러를 등록하는 `import _ "net/http/pprof"` 를 공식 관용으로 소개한다. JLS §7.6 은 공개 최상위 타입을 파일 이름에 맞추게 할 수 있고 클래스마다 파일을 두는 것이 흔한 관행이라 적는다.

검사가 아키텍처 침식(erosion)을 실제로 줄이는지에 대한 근거는 얇다. 약 240 KLOC 산업 시스템에서 제약 18개 가운데 12개가 위반됐지만(Terra & Valente 2009), 한 상용 시스템의 종단 사례에서 발견은 제거로 이어지지 않았고(Rosik et al. 2011), 실무자 19명은 코드와 아키텍처를 대응시키는 수고를 도입 장벽으로 꼽았다(Ali et al. 2018). 도구 10개는 있어야 할 의존의 72~77% 만 보고했다(Pruijt et al. 2017). 성숙한 도구는 모두 기준선(baseline)이나 예외 장치를 두며(ArchUnit `FreezingArchRule`, Nx `ignoredCircularDependencies`), Terra & Valente 는 빌드마다 검사하면 임시 의존까지 잡아 "too intrusive"(너무 간섭적)일 수 있다고 했다. 에이전트가 쓴 코드에 대한 적합성 검사 연구는 찾지 못했다.

### 참고문헌 (5장)

표기: (초록만 확인)은 원문 대신 초록이나 색인 기록만 읽은 항목, [2차 출처]는 다른 문헌의 인용이나 요약으로만 아는 항목, [미확인]은 서지 정보 일부를 확인하지 못한 항목이다. 노트에 제목이 없는 항목은 대괄호 안에 내용을 적었다. 살아 있는 웹 문서는 2026년 10월 열람 기준이다.

- Aizawa, K. (2025-09-11). "Writing effective tools for agents — with agents." Anthropic Engineering. https://www.anthropic.com/engineering/writing-tools-for-agents
- Alexander, C. (1964). *Notes on the Synthesis of Form*. Harvard University Press. [2차 출처: 원서 미열람. Gabriel(2023)이 인용한 원문 문장으로만 읽음. 1971년판 서문도 같은 경로]
- Alexander, C. (1965). "A City Is Not a Tree." *Architectural Forum* 122(1):58–62, 122(2):58–61. https://www.gregbryant.com/gatemaker/A_CITY_IS_NOT_A_TREE.pdf
- Ali, N., Baker, S., O'Crowley, R., Herold, S. & Buckley, J. (2018, 온라인 2017). "Architecture consistency: State of the practice, challenges and requirements." *Empirical Software Engineering*. https://doi.org/10.1007/s10664-017-9515-3 (초록만 확인)
- Anthropic (2026a). "Best practices for Claude Code." Claude Code Docs, 살아 있는 문서(2025-04 Anthropic Engineering 글을 대체). https://code.claude.com/docs/en/best-practices
- Anthropic (2026b). "How Claude remembers your project." Claude Code Docs. https://code.claude.com/docs/en/memory
- Anthropic (2026c). "Set up Claude Code in a monorepo or large codebase." Claude Code Docs. https://code.claude.com/docs/en/large-codebases
- Anthropic (2026d). "How Claude Code works in large codebases." Claude 블로그, 2026-05-14(저자 표기 없음). https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
- Arisholm & Sjøberg (2004). [위임형 대 중앙 집중형 제어 스타일의 유지보수성 실험, 전문가 99명·학생 59명]. *IEEE Transactions on Software Engineering*. https://doi.org/10.1109/TSE.2004.43 (초록만 확인)
- Avidan & Feitelson (2017). [변수 이름이 이해에 미치는 영향, 전문가 9명]. ICPC 2017. https://doi.org/10.1109/ICPC.2017.27 (초록만 확인)
- Bazel. "Visibility." Bazel 문서. https://bazel.build/concepts/visibility
- Beck, K. (2025-06-25). "Augmented Coding: Beyond the Vibes." *Tidy First?* 뉴스레터. https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes
- Böckeler, B. (2025-08-05). "How far can we push AI autonomy in code generation?" martinfowler.com. https://martinfowler.com/articles/pushing-ai-autonomy.html
- Böckeler, B. (2026a, 2026-02-17). [Harness engineering 메모: OpenAI 사례 요약]. martinfowler.com. https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html
- Böckeler, B. (2026b, 2026-04-02). "Harness engineering for coding agent users." martinfowler.com. https://martinfowler.com/articles/harness-engineering.html
- Booch, G. et al. (2007). *Object-Oriented Analysis and Design with Applications*, 3rd ed., 1장. Addison-Wesley. https://ptgmedia.pearsoncmg.com/images/9780201895513/samplechapter/020189551X_CH01.pdf
- Borg, M. et al. (2025). "Echoes of AI…" [AI 보조로 만든 코드의 이후 유지보수에 관한 무작위 대조 시험, 151명]. ICSME 2025 등록 보고서, arXiv:2507.00788 (v3 2026-02). https://arxiv.org/abs/2507.00788
- C++ 작업 초안. [module.import]. https://eel.is/c++draft/module.import (문단 번호는 ISO C++20 과 다를 수 있음)
- Cataldo, M., Wagstrom, P. A., Herbsleb, J. D. & Carley, K. M. (2006). "Identification of coordination requirements…" CSCW '06, pp. 353–362. https://dl.acm.org/doi/pdf/10.1145/1180875.1180929
- Cemri, M. et al. (2025). "Why Do Multi-Agent LLM Systems Fail?" arXiv:2503.13657 (v3 2025-10-26). https://arxiv.org/abs/2503.13657 (초록만 확인)
- Cheng, Wu & Hu (2024). [DraCo: 데이터 흐름 기반 저장소 수준 코드 완성]. ACL 2024, arXiv:2405.19782. https://arxiv.org/abs/2405.19782
- Colfer, L. J. & Baldwin, C. Y. (2016). "The mirroring hypothesis: theory, evidence, and exceptions." *Industrial and Corporate Change* 25(5):709–738. https://doi.org/10.1093/icc/dtw027
- Conway, M. E. (1968). "How Do Committees Invent?" *Datamation* 14(4):28–31. https://www.melconway.com/Home/Committees_Paper.html
- Cowan, N. (2001). "The magical number 4 in short-term memory: A reconsideration of mental storage capacity." *Behavioral and Brain Sciences* 24(1):87–114. https://doi.org/10.1017/S0140525X01003922 (초록만 확인)
- Cowan, N. (2010). "The magical mystery four: How is working memory capacity limited, and why?" *Current Directions in Psychological Science* 19(1):51–57. https://doi.org/10.1177/0963721409359277 (초록만 확인)
- de Jong, T. (2010). "Cognitive load theory, educational research, and instructional design: some food for thought." *Instructional Science* 38:105–134. https://doi.org/10.1007/s11251-009-9110-0 (초록만 확인)
- Ding et al. (2022). [CoCoMIC: 파일 간 문맥을 찾아 쓰는 코드 완성]. arXiv:2212.10007. https://arxiv.org/abs/2212.10007
- Doernenburg, E. (2026-01-27). "Assessing internal quality while coding with an agent." martinfowler.com. https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html
- Du et al. (2025). [입력 길이만으로 생기는 성능 저하, 5개 모델]. Findings of EMNLP 2025, arXiv:2510.05381. https://arxiv.org/abs/2510.05381
- Edwards-Alexander, G. (2026-07-30). "The Economic Benefit of Refactoring." martinfowler.com. https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html
- Effective Go. Go 공식 문서. https://go.dev/doc/effective_go
- El Emam, K. et al. (2002). "The optimal class size for object-oriented software." *IEEE TSE* 28(5):494–509. https://doi.org/10.1109/TSE.2002.1000452 (초록만 확인)
- Ericsson, K. A. & Kintsch, W. (1995). "Long-term working memory." *Psychological Review* 102(2):211–245. https://doi.org/10.1037/0033-295X.102.2.211 (초록만 확인)
- Ethiraj, S. K. & Levinthal, D. (2004). "Modularity and innovation in complex systems." *Management Science* 50(2):159–173. https://doi.org/10.1287/mnsc.1030.0145 (초록만 확인)
- Gabriel, R. P. (2023). [*Notes on the Synthesis of Form* 재검토와 재현 시도]. *The Art, Science, and Engineering of Programming* 7(3), art. 8. https://doi.org/10.22152/programming-journal.org/2023/7/8 ; 작업 노트 https://dreamsongs.com/Files/NotesForNotesOnNotes.pdf
- GHC User's Guide 9.14.1. "Separate compilation"(hs-boot). https://downloads.haskell.org/ghc/latest/docs/users_guide/separate_compilation.html
- Gloaguen, Mündler, Müller, Raychev & Vechev (2026). [AGENTS.md 문맥 파일 평가, CTXbench]. arXiv:2602.11988 (v1 2026-02-12, v3 2026-09-29, 학회 미정). https://arxiv.org/html/2602.11988v3
- Go 1.4 Release Notes (2014-12). https://go.dev/doc/go1.4
- Go 명세. "The Go Programming Language Specification." https://go.dev/ref/spec
- Hadfield et al. (2025-06-13). "How we built our multi-agent research system." Anthropic Engineering. https://www.anthropic.com/engineering/multi-agent-research-system
- He, Miller, Agarwal, Kästner & Vasilescu (2026). "Speed at the Cost of Quality…" [Cursor 도입 저장소 이중차분 분석]. MSR '26, arXiv:2511.04427. https://arxiv.org/html/2511.04427
- Herbsleb, J. D. & Grinter, R. E. (1999). "Splitting the organization and integrating the code: Conway's law revisited." ICSE '99, pp. 85–95. https://doi.org/10.1145/302405.302455
- Hofmeister, Siegmund & Holt (2017). "Shorter identifier names take longer to comprehend." SANER 2017. https://doi.org/10.1109/SANER.2017.7884623 (초록만 확인)
- Horikawa et al. (2025). [에이전트 리팩터링 15,451건 실증, TOSEM 투고]. arXiv:2511.04824. https://arxiv.org/html/2511.04824
- Jain, N. (2026-10-13). "Are Harnesses Worth the Cost?" martinfowler.com. https://martinfowler.com/articles/are-harnesses-worth-the-cost.html
- Java SE 21 API. `java.lang.module.Configuration`. https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/module/Configuration.html
- JEP 261: Module System (JDK 9, Delivered; 2024-08-19 갱신). https://openjdk.org/jeps/261
- Jimenez et al. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" ICLR 2024, arXiv:2310.06770 (v3 2024-11). https://arxiv.org/html/2310.06770v3
- JLS. *The Java Language Specification*, Java SE 21, 7장 §7.6. https://docs.oracle.com/javase/specs/jls/se21/html/jls-7.html
- Kang, Seo & Kim (2024). [함수 수준 모듈성과 코드 생성 성능]. Findings of EMNLP 2024, arXiv:2407.11406. https://arxiv.org/html/2407.11406
- Kim, Y. et al. (2025). "Towards a Science of Scaling Agent Systems." arXiv:2512.08296 (v1 2025-12, v3 2026-04-08). https://arxiv.org/abs/2512.08296 (초록만 확인)
- Korson & Vaishnavi (1986). "An empirical study of the effects of modularity on program modifiability." *Empirical Studies of Programmers*, Ablex(DOI 없음). (초록만 확인: OpenAlex 색인 https://api.openalex.org/works?search=empirical%20study%20of%20the%20effects%20of%20modularity%20on%20program%20modifiability)
- Kulak et al. (2010). "Applications of axiomatic design principles: A literature review." https://research.itu.edu.tr/en/publications/applications-of-axiomatic-design-principles-a-literature-review/ [2차 출처: 요약으로만 확인. 수록지 미확인]
- Lakos, J. (1996). *Large-Scale C++ Software Design*. Addison-Wesley. [2차 출처: NDepend 문서의 인용으로만 앎]
- LaToza, T. D. & Myers, B. A. (2010). "Hard-to-answer questions about code." PLATEAU 2010. https://doi.org/10.1145/1937117.1937125 (초록만 확인)
- Lawrance et al. (2013). "How programmers debug, revisited: An information foraging theory perspective." *IEEE TSE*. https://doi.org/10.1109/TSE.2010.111 (초록만 확인)
- Letovsky, S. & Soloway, E. (1986). "Delocalized plans and program comprehension." *IEEE Software*. https://doi.org/10.1109/MS.1986.233414 (초록만 확인)
- Liu et al. (2024). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the ACL* 12:157–173. https://doi.org/10.1162/tacl_a_00638 (2023 arXiv 판을 대체)
- Lulla, Mohsenimofidi, Galster, Zhang, Baltes & Treude (2026). [AGENTS.md 가 에이전트 효율에 미치는 영향, Codex CLI, PR 124건]. arXiv:2601.20404 (사전 출판). https://arxiv.org/html/2601.20404
- MacCormack, A., Baldwin, C. Y. & Rusnak, J. (2012). "Exploring the duality between product and organizational architectures: A test of the 'mirroring' hypothesis." *Research Policy* 41(8):1309–1324. https://doi.org/10.1016/j.respol.2012.04.011
- METR (2025). [AI 도구가 숙련 오픈 소스 개발자 생산성에 미치는 영향, 무작위 대조 시험, 16명·246과업]. arXiv:2507.09089. https://arxiv.org/abs/2507.09089
- METR (2026-02-24). [2025 결과의 갱신]. https://metr.org/blog/2026-02-24-uplift-update/
- Miller, G. A. (1956). "The magical number seven, plus or minus two: Some limits on our capacity for processing information." *Psychological Review* 63(2):81–97. https://doi.org/10.1037/h0043158 (원문: https://psychclassics.yorku.ca/Miller/)
- NDepend. "Code Metrics" 문서. https://www.ndepend.com/docs/code-metrics
- Nurvitadhi et al. (2003). "Do class comments aid Java program understanding?" FIE 2003. https://doi.org/10.1109/FIE.2003.1263332 (초록만 확인)
- Nx. "enforce-module-boundaries" 규칙 문서(v20). https://20.nx.dev/nx-api/eslint-plugin/documents/enforce-module-boundaries
- OpenAI (2026). "Harness engineering: leveraging Codex in an agent-first world." https://openai.com/index/harness-engineering/ [2차 출처: 원문 HTTP 403. Böckeler(2026a; 2026b)의 요약으로만 앎. 저자, 정확한 날짜, 층 목록, 수치, 린트 메시지 문구 미확인]
- OSGi Core Release 8 (2020). 3장 Module Layer, §3.9.7 "Bundle Cycles". https://docs.osgi.org/specification/osgi.core/8.0.0/framework.module.html
- Osmani, A. (2024-12-04). "The 70% problem." Elevate(Substack). https://addyo.substack.com/p/the-70-problem-hard-truths-about
- Osmani, A. (2026-01-04). "My LLM coding workflow going into 2026." https://addyosmani.com/blog/ai-coding-workflow/
- Ouyang et al. (2025). [RepoGraph: 저장소 수준 코드 그래프]. ICLR 2025, arXiv:2410.14684 (v2 2025-03). https://arxiv.org/html/2410.14684v2
- Parnas, D. L. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM* 15(12):1053–1058. https://doi.org/10.1145/361598.361623
- Passos, L., Terra, R., Valente, M. T., Diniz, R. & Mendonça, N. (2010). "Static Architecture-Conformance Checking: An Illustrative Overview." *IEEE Software* 27(5):82–89. https://doi.org/10.1109/MS.2009.117 (원문: https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf)
- Pike, R. (2012). "Go at Google: Language Design in the Service of Software Engineering." SPLASH 2012 기조연설. https://go.dev/talks/2012/splash.article
- Piorkowski et al. (2016). [개발자의 탐색 가치·비용 예측]. FSE 2016. https://doi.org/10.1145/2950290.2950302 (초록만 확인)
- Politowski et al. (2020). [Blob·Spaghetti 반패턴과 이해, 133명 재현 연구]. *Information and Software Technology*. https://arxiv.org/abs/2009.02438 (초록만 확인)
- Prechelt et al. (2002). "Two controlled experiments assessing the usefulness of design pattern documentation in program maintenance." *IEEE TSE*. https://doi.org/10.1109/TSE.2002.1010061 (초록만 확인)
- Pruijt, L., Köppe, C., van der Werf, J. M. & Brinkkemper, S. (2017). "The accuracy of dependency analysis in static architecture compliance checking." *Software: Practice and Experience*. https://doi.org/10.1002/spe.2421 (초록만 확인)
- Rashid et al. (2025). [SWE-PolyBench: 4개 언어 2,110건 저장소 수준 벤치마크]. arXiv:2504.08703 (v3). https://arxiv.org/html/2504.08703v3
- Ronacher, A. (2025-06-12). "Agentic Coding Recommendations." https://lucumr.pocoo.org/2025/6/12/agentic-coding/
- Rosik, J., Le Gear, A., Buckley, J., Babar, M. A. & Connolly, D. (2011). "Assessing architectural drift in commercial software development: a case study." *Software: Practice and Experience* 41(1):63–86. https://doi.org/10.1002/spe.999 (초록만 확인)
- Sangal, N., Jordan, E., Sinha, V. & Jackson, D. (2005). "Using Dependency Models to Manage Complex Software Architecture." OOPSLA 2005. https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf [미확인: DOI 10.1145/1094811.1094824 는 기억에 의존]
- Schankin et al. (2018). "Descriptive compound identifier names improve source code comprehension." ICPC 2018. https://doi.org/10.1145/3196321.3196332 (초록만 확인)
- Siegmund et al. (2017). "Measuring neural efficiency of program comprehension." ESEC/FSE 2017. https://doi.org/10.1145/3106237.3106268 (초록만 확인)
- Simon, H. A. (1962). "The Architecture of Complexity." *Proceedings of the American Philosophical Society* 106(6):467–482. https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ArchitectureOfComplexity.HSimon1962.pdf
- Simon, H. A. (1996). *The Sciences of the Artificial*, 3rd ed. MIT Press. https://andymatuschak.org/files/papers/Simon%20-%201996%20-%20The%20Sciences%20of%20the%20Artificial.pdf (1962년 논문을 일부 대체하는 개정판)
- Simon, H. A. & Ando, A. (1961). "Aggregation of variables in dynamic systems." *Econometrica* 29:111–138. [2차 출처: 미열람. Simon(1962)을 통해서만 앎]
- Skelton, M. & Pais, M. (2019; 2판 2025-09-23). *Team Topologies*. IT Revolution. https://teamtopologies.com/book ; 핵심 개념 https://teamtopologies.com/key-concepts [책 본문 미열람: 출판사·저자 페이지, 공식 핵심 개념 페이지와 용어집으로만 확인]
- Suh, N. P. (2001). *Axiomatic Design: Advances and Applications*. Oxford University Press. [2차 출처: 원저 미열람. 공리 문구는 이를 바탕으로 한 MIT 2.800 강의 노트(2004) https://mitocw.ups.edu.ec/courses/mechanical-engineering/2-800-tribology-fall-2004/lecture-notes/ch10_axiomatic.pdf 에서 확인]
- Suh, N. P. & Do, S.-H. (2000). "Axiomatic Design of Software Systems." *CIRP Annals* 49(1). https://www.axiomaticdesign.com/wp-content/uploads/cirp_ad_of_software.pdf
- Sweller, J. (2010). "Element interactivity and intrinsic, extraneous, and germane cognitive load." *Educational Psychology Review* 22:123–138. https://doi.org/10.1007/s10648-010-9128-5 (초록만 확인)
- Tempero, Blincoe & Lottridge (2023). [모듈성 수준이 코드 수정과 이해에 미치는 영향, 학생 40명]. ACE 2023. https://doi.org/10.1145/3576123.3576138 (초록만 확인)
- Terra, R. & Valente, M. T. (2009). "A dependency constraint language to manage object-oriented software architectures." *Software: Practice and Experience* 39(12):1073–1094. https://doi.org/10.1002/spe.931 (원문: https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf)
- Thoughtworks (2025). "AI-friendly code design." Technology Radar 2025-04(Vol 32), Assess. 현재 Radar 에는 없음. https://www.thoughtworks.com/radar/techniques/ai-friendly-code-design
- Thoughtworks (2026a). "Feedback sensors for coding agents." Technology Radar 2026-04-15(Vol 34), Trial. https://www.thoughtworks.com/radar/techniques/feedback-sensors-for-coding-agents
- Thoughtworks (2026b). "Architecture drift reduction with LLMs." Technology Radar 2026-04-15(Vol 34), Assess. https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms
- TNG ArchUnit. ArchUnit 사용자 안내서 1.5.1 과 `Architectures.java`(main 브랜치). https://www.archunit.org/userguide/html/000_Index.html ; https://github.com/TNG/ArchUnit/blob/main/archunit/src/main/java/com/tngtech/archunit/library/Architectures.java
- Ulrich, K. (1995). "The role of product architecture in the manufacturing firm." *Research Policy* 24(3):419–440. https://doi.org/10.1016/0048-7333(94)00775-3 (원문: https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)
- Van Eikema Hommes (2010). ESD.33 Systems Engineering, 강의 6(공리 설계). MIT OpenCourseWare. https://ocw.mit.edu/courses/esd-33-systems-engineering-summer-2010/93a63108bb30c1041d93b024e4cbcf35_MITESD_33SUM10_lec06.pdf
- von Mayrhauser, A. & Vans, A. M. (1995). "Program comprehension during software maintenance and evolution." *IEEE Computer* 28(8). https://doi.org/10.1109/2.402076 (초록만 확인)
- Whitney (2005). "Physical Limits to Modularity." MIT ESD 작업 논문(1996년 논문의 2005-03-26 개정판). https://dspace.mit.edu/handle/1721.1/102731
- Woodfield, Dunsmore & Shen (1981). "The effect of modularization and comments on program comprehension." ICSE '81. https://dl.acm.org/doi/10.5555/800078.802534 (초록만 확인)
- Xia et al. (2024). "Agentless: Demystifying LLM-based Software Engineering Agents." arXiv:2407.01489 (v2, 최종 학회 미확인). https://arxiv.org/html/2407.01489v2
- Yan, W. (2025-06-12). "Don't Build Multi-Agents." Cognition 블로그. https://cognition.com/blog/dont-build-multi-agents
- Yang et al. (2024). "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering." arXiv:2405.15793 (v3; NeurIPS 2024 는 arXiv 페이지에 표기 없음). https://arxiv.org/html/2405.15793v3
- Zhang et al. (2024). [Hierarchical Context Pruning: 의존 파일의 구현을 지운 저장소 수준 완성]. arXiv:2406.18294. https://arxiv.org/abs/2406.18294
