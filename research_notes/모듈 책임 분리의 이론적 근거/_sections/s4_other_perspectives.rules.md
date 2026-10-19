# 5장 사이드 파일: 다른 관점에서 나온 규칙 후보와 ln-structure 시사점

5장(다른 관점: 설계 과학, 인지, 조직, AI 코딩 에이전트, 구조 검사 도구) 작성자가 최종 작성자에게 넘기는 작업 메모다. 출처는 저자 연도로 적고 5장 참고문헌을 따른다. 5장 본문에 없는 출처는 맨 끝 '이 파일에서만 인용한 출처'에 적었다. 근거 강도는 종류(형식 논증 / 실증 / 전문가 의견 / 공급자 주장)와 정도(강 / 중 / 약)로 적는다. AI 에이전트 수치는 2023~2026년 모델과 Python 위주 벤치마크에서 나왔으므로 날짜와 판을 함께 인용해야 한다. 'c1 의 추론'처럼 적은 것은 노트 작성자의 추론이며 원 출처의 주장이 아니다.

## 규칙 후보

1. **경계는 상호작용이 약한 곳에 긋는다(안쪽 연결이 바깥 연결보다 강하게).**
   - 근거: 거의 분해 가능한 시스템에서는 부분이 단기적으로 독립이고 장기적으로 집계로만 얽혀 부분을 따로 이해하고 고칠 수 있다. Alexander 의 부적합 그래프 분해, Ulrich 의 일대일 대응과 탈결합 인터페이스도 같은 기준이다. 사람 실험에서 이득을 낸 것도 단위 크기가 아니라 경계의 질(추상 자료형, 변경을 국소화하는 정보 은닉)이었다.
   - 출처: Simon 1962; Simon 1996; Alexander 1964; Ulrich 1995; Woodfield et al. 1981; Korson & Vaishnavi 1986.
   - 강도: 형식 논증(Simon & Ando 의 정리) + 개념 논증 + 소규모 실증. 중.
   - 반론과 한계: 상호작용이 촘촘하거나 겹치면 깔끔한 나무 분해가 없다(Alexander 1965; Gabriel 2023 의 재현 실패). 분해는 유일하지 않다(Simon 1996). 요구에서 예측한 상호작용은 실제의 일부만 잡는다(54개 적중, 118개 누락; Van Eikema Hommes 2010). 실제 조정 요구는 유동적이고 경계를 넘는다(Cataldo et al. 2006). 어휘로 묶으면 실제 결합을 놓친다(Alexander 1964).

2. **모듈의 책임은 해법 중립적으로, '어떻게'가 아니라 '무엇'으로 적는다.**
   - 근거: 공리 설계는 기능 요구를 "say 'what' not 'how'" 로 정하고 모듈을 기능 요구 하나(설계 행렬의 한 행)로 정의한다. Simon(1996)은 부분이 메커니즘 세부와 무관하게 기능을 통해 서로 영향을 주게 하라고 했다. 개발자가 가장 자주 묻는 질문이 "무엇을 하려는 것인가"이고, 의미 단서(비컨, scent)는 이해와 탐색을 돕는다.
   - 출처: Van Eikema Hommes 2010; Suh & Do 2000; Simon 1996; LaToza & Myers 2010; Siegmund et al. 2017; Lawrance et al. 2013.
   - 강도: 공리적 주장과 전문가 의견(약~중) + 인지 실증(식별자·비컨 수준, 모듈 수준은 유비). 중.
   - 반론과 한계: 하위 책임은 상위의 '어떻게'를 고른 뒤에야 정해진다(지그재그; Suh & Do 2000). '무엇'은 "왜 이렇게 했는가"에 답하지 않는다(LaToza & Myers 2010). 클래스 주석은 상위 수준 이해를 올리지 않았다(Nurvitadhi et al. 2003). 오해를 부르는 이름은 이득을 지운다(Avidan & Feitelson 2017). 모듈 수준 책임 문장을 시험한 실험은 없다.

3. **책임 문장과 이름은 구체적이고 내용과 맞아야 하며, 어긋나면 바로잡는다(표류 관리).**
   - 근거: 서술적 이름은 이해를 14~19% 빠르게 하고 오해 이름은 그 이득을 지운다. 인터페이스를 비공식적으로 다듬은 내용은 기록되지 않으면 작업자가 바뀔 때 깨진다. 공급자도 관례 표류와 파일 노후화를 경고한다.
   - 출처: Hofmeister et al. 2017; Schankin et al. 2018; Avidan & Feitelson 2017; Herbsleb & Grinter 1999; Anthropic 2026c; Thoughtworks 2026b.
   - 강도: 식별자 수준 실증(중), 모듈 수준은 유비(약).
   - 반론과 한계: 두 개발자가 같은 이름을 고를 확률은 중앙값 6.9% 지만 고른 이름은 대개 이해된다(Feitelson et al. 2022). 같은 책임도 쓰는 사람(이나 에이전트)마다 다르게 적힌다. 모듈·패키지 이름 연구는 없다. 의미 일치는 구조 검사로 잡히지 않는다(Böckeler 2026b).

4. **모듈 사이 순환은 금지하고, 순환은 모듈(컴파일 단위) 안에만 허용한다.**
   - 근거: Go, JPMS, C++ 모듈, GHC(부트 파일 없이)는 단위 수준 비순환을 강제하고 단위 안은 자유롭다. Pike 는 순환 금지가 패키지 경계를 분명히 하고 경계를 일찍 생각하게 한다고 했다. 공리 설계에서 결합 설계는 순환에 대응한다(해석). Simon 의 '안쪽 강, 바깥 약'과 Ulrich 의 타이어(안은 통합형, 밖에서는 모듈 부품)도 안쪽 순환 허용과 맞는다.
   - 출처: Go 명세; Java SE 21 Configuration; C++ 작업 초안; GHC User's Guide; Pike 2012; Van Eikema Hommes 2010; Simon 1962; Ulrich 1995.
   - 강도: 언어 사양(설계 선택) + 전문가 의견. 중. 제1원리 논증은 없다.
   - 반론과 한계: OSGi 는 번들 순환이 무한 탐색을 일으키지 않게만 요구하고, GHC 는 부트 파일로 순환을 허용한다. Sangal 등은 모든 아키텍처가 비순환 층 구조여야 하는 것은 아니고 일탈은 의식적 절충일 수 있다고 했다. 거의 분해 가능성은 세기에 관한 것이라 순환 금지를 끌어내지 못한다(Simon 1962). 공리 설계도 삼각(탈결합)을 허용할 뿐 이상(비결합)으로 보지는 않는다.

5. **층(수준)은 이름이 아니라 의존 관계에서 계산한다.**
   - 근거: Parnas 의 층은 '사용' 관계의 부분 순서에서 나온다(기호 표를 쓰면 줄 저장소가 2층, 아니면 1층). NDepend 의 Level(Lakos 유래)은 1 + 직접 쓰는 단위의 최고 수준이고 순환이면 정의되지 않는다. 공리 설계의 탈결합 설계는 정해진 순서로 잎부터 쌓는다.
   - 출처: Parnas 1972; NDepend; Lakos 1996; Suh & Do 2000.
   - 강도: 형식 정의 + 도구 지표(중). 효과를 잰 실증은 없다.
   - 반론과 한계: 계산된 수준은 위상적 의미만 있고 영역 의미가 없어 사람의 길찾기 단서로 약하다(탐색은 단서를 따른다, Lawrance et al. 2013; c1 의 추론). 의존이 바뀌면 수준도 바뀐다. NDepend 는 이 값을 지표로만 쓰고 높고 낮음에 대한 권고가 없다고 밝힌다. 위계와 깨끗한 분해는 서로 독립인 성질이다(Parnas 1972). 층 검사를 통과해도 분해가 좋다는 뜻은 아니다.

6. **모듈은 정해진 표면(진입점)으로만 쓰게 하고, 선언 가시성과 단위 내보내기를 구분한다.**
   - 근거: public 이 곧 어디서나 접근 가능은 아니다(JEP 261). Go `internal/`, Bazel 기본 비공개, eslint-plugin-boundaries 의 entry-point·no-private, Sonargraph 의 인터페이스와 `hidden` 이 같은 장치다. Alexander 의 나무 성질("단위 전체를 거쳐서만 이어진다")과 Simon 의 집계 상호작용도 같은 생각이다. 에이전트 쪽에서는 의존 파일의 구현을 지우고 시그니처만 남겨도 완성 정확도가 크게 떨어지지 않았고, 뼈대가 전체 파일보다 위치를 잘 찾았다.
   - 출처: JEP 261; Go 1.4 Release Notes; Bazel; eslint-plugin-boundaries; Sonargraph; Alexander 1965; Simon 1962; Zhang et al. 2024; Xia et al. 2024.
   - 강도: 언어·도구 사양(중) + 에이전트 실증 2건(중).
   - 반론과 한계: 오픈 소스는 엄격한 정보 은닉 없이 '실행 가능한 투명성'으로 모듈성을 얻었고 부분 미러링이 효과적이었다(Colfer & Baldwin 2016). import 는 표면으로 제한하되 읽기는 막지 말라는 쪽으로 읽힌다. Bazel 은 공개 인터페이스를 명시적으로 고르고 기본 공개를 피하라고 권한다. 도구가 만든 표면이 공개 요소를 모두 다시 내보내면 기본 공개와 같아진다. 나무 구조는 겹침을 담지 못한다(Alexander 1965).

7. **아키텍처 단위를 폴더(패키지) 위계와 일치시켜 별도 대응표 없이 검사한다.**
   - 근거: Passos 등은 패키지 위계가 개념 아키텍처의 구성 요소를 닮게 하라고 권했다. 코드와 아키텍처를 대응시키는 수고는 실무자가 꼽은 도입 장벽이다. DSM 설계 규칙, ArchUnit, dependency-cruiser 도 패키지 위계를 아키텍처 단위로 쓴다.
   - 출처: Passos et al. 2010; Ali et al. 2018; Sangal et al. 2005; TNG ArchUnit; dependency-cruiser.
   - 강도: 전문가 판단 + 도구 관행(중).
   - 반론과 한계: 한 위계가 지배적일 때는 간결하지만 직교하는 관점이 여럿이면 덜 간결하다(Sangal et al. 2005). 나무 대 겹침 문제가 남는다(Alexander 1965).

8. **의존은 허용 목록(기본 거부)으로 검사한다.**
   - 근거: ArchUnit 의 층 아키텍처는 "prevents detours" 때문에 허용 목록만 지원한다. Sonargraph 는 연결하지 않은 의존을 모두 위반으로 보고, Nx 는 제약에 맞는 태그가 없는 프로젝트가 어떤 라이브러리에도 의존하지 못하게 한다.
   - 출처: TNG ArchUnit; Sonargraph; Nx.
   - 강도: 도구 설계 선택(중). 침식을 줄인다는 효과 연구는 없다.
   - 반론과 한계: 정적 분석은 있어야 할 의존의 72~77% 만 보고하고 리플렉션 같은 동적 의존을 보지 못한다(Pruijt et al. 2017; Passos et al. 2010).

9. **반드시 지켜야 할 구조 규칙은 산문 지시가 아니라 결정적 검사로 만들고, 편집 시점에 가깝게 돌린다.**
   - 근거: SWE-agent 에서 편집 시점 린트를 빼면 18.0% 에서 15.0% 로 떨어졌다(GPT-4 Turbo, SWE-bench Lite, 2024). 공급자는 훅은 결정적이고 CLAUDE.md 는 권고라고 한다. Thoughtworks Radar(2026-04)는 센서를 세션 중에 돌리라 하고, Böckeler 는 검사를 가능한 한 앞쪽에 두고 ArchUnit 을 에이전트 훅에서 돌리는 예를 든다. Sangal 은 지속 검사가 회귀 테스트처럼 새 구성원이 들여온 결함을 곧바로 잡는다고 했고, Terra & Valente 는 아키텍처에 익숙하지 않은 개발자에게 빌드 시 검사를 권했다(아키텍처 기억이 없는 에이전트가 이 경우와 닮았다는 것은 c6 의 추론). Rosik 등에서 게이트 없는 발견은 제거로 이어지지 않았다. 에이전트는 구조를 스스로 가꾸지 않는다(설계 냄새 중앙값 변화 0; 인지 복잡도 +41.64% 지속).
   - 출처: Yang et al. 2024; Anthropic 2026a; Thoughtworks 2026a; Böckeler 2026b; Sangal et al. 2005; Terra & Valente 2009; Rosik et al. 2011; Horikawa et al. 2025; He et al. 2026.
   - 강도: 실증 1건(중) + 관찰 연구(중) + 공급자 주장과 전문가 합의(약~중). 종합 중.
   - 반론과 한계: Terra & Valente 는 빌드마다 검사하면 임시 의존까지 잡아 너무 간섭적일 수 있다고 했다. 성숙한 도구는 모두 기준선·예외 장치를 둔다. 최전선 모델은 하네스 없이도 통과했고 하네스는 토큰을 약 10배 썼다(Jain 2026, 단 린터·훅 없는 하네스). 정적 검사는 의존을 다 보지 못하고(Pruijt et al. 2017) 과잉 설계나 책임 불일치를 잡지 못한다(Böckeler 2026b). 문맥 파일이 단계와 비용을 늘린 것처럼(Gloaguen et al. 2026) 차단 루프도 비용을 늘릴 수 있다(유추).

10. **검사 메시지는 무엇을, 어디서, 어떻게 고칠지 알려 준다.**
    - 근거: 도구 오류 응답은 "specific and actionable improvements, rather than opaque error codes or tracebacks" 여야 한다(Aizawa 2025). SWE-agent 의 설계 원칙은 "Environment feedback should be informative but concise" 다. 센서 신호는 LLM 이 읽기 좋게 만들라(Böckeler 2026b). 리팩터링 유형을 알려 주자 LLM 의 성공률이 15.6% 에서 86.7% 로 올랐다(Liu et al. 2025, 유비). Factory 는 린트를 사람 의도와 에이전트 출력을 잇는 실행 가능한 명세라 부른다(Sng 2025, 공급자).
    - 출처: Aizawa 2025; Yang et al. 2024; Böckeler 2026b; Liu et al. 2025; Sng 2025.
    - 강도: 공급자·전문가 의견(약) + 유비적 실증(약).
    - 반론과 한계: 메시지 문구의 효과를 잰 연구는 없다. 에이전트는 테스트를 끄거나 지우고 성공을 거짓 보고한다(Beck 2025; Böckeler 2025). 막힌 에이전트가 규칙을 피상적으로 만족시킬 위험이 있지만 측정 자료는 없다.

11. **늘 문맥에 들어가는 정보는 짧고 신호가 높게 유지하고, 비표준 관행 위주로 적는다.**
    - 근거: 긴 문맥은 정보가 다 있어도 성능을 떨어뜨린다(13.9~85%, Du et al. 2025; 가운데 위치의 손실, Liu et al. 2024; SWE-bench 에서 BM25 문맥이 13k 에서 50k 토큰으로 늘자 Claude 2 가 1.96% 에서 1.22% 로, Jimenez et al. 2024). 문맥 파일은 성공률을 일반적으로 올리지 못하고 비용을 20% 넘게 늘렸으며 개요는 위치 찾기를 줄이지 못했지만, 적힌 지시는 지켜졌다(Gloaguen et al. 2026). 공급자는 CLAUDE.md 200줄 이하, 파일별 설명 제외를 권하고 지시 비대화를 경고한다.
    - 출처: Du et al. 2025; Liu et al. 2024; Jimenez et al. 2024; Gloaguen et al. 2026; Anthropic 2026a; Anthropic 2026b; Thoughtworks 2026c.
    - 강도: 장문맥 일반 실증(강), 문맥 파일 통제 평가 1건(중), 공급자 주장(약).
    - 반론과 한계: AGENTS.md 가 실행 시간을 28.64%, 출력 토큰을 16.58% 줄였다는 결과가 있다(Lulla et al. 2026, 정답 미측정). 계산된 한 줄 모듈 지도는 시험된 적이 없다.

12. **변경이 한 모듈 안에서 끝나도록 경계를 정한다(변경 국소성).**
    - 근거: SWE-PolyBench 에서 단일 파일 수정이 가장 잘됐고 세 파일부터 10% 미만, 클래스·함수 혼합 수정은 8~15% 였다. SWE-bench 정답 패치는 평균 1.7개 파일인데 모델은 한 파일 넘게 고치는 일이 드물다. 다중 파일 리팩터링은 에이전트 22% 대 사람 87% 였다. 모듈성은 정보 은닉으로 변경이 국소화될 때만 수정을 도왔다. 실무자도 좋은 모듈화가 변경 장소 수를 줄인다고 본다.
    - 출처: Rashid et al. 2025; Jimenez et al. 2024; Gautam et al. 2025; Korson & Vaishnavi 1986; Ulrich 1995; Thoughtworks 2025; Böckeler 2025.
    - 강도: 벤치마크 상관(중, 교란 있음) + 소규모 실험(중) + 전문가 의견.
    - 반론과 한계: 벤치마크는 모듈이 아니라 파일 수를 센다. 잘게 쪼개면 변경당 파일 수가 늘 수 있다. 저자들도 복잡도만의 효과로 보지 않는다(Rashid et al. 2025). 실제 조정 요구는 함께 바뀌는 파일(동반 변경)을 따르며 import 로는 보이지 않는다(Cataldo et al. 2006).

13. **지나치게 잘게 쪼개지 않는다. 단위 크기에 수치 상한은 두지 않되, 쪼갤 때 늘어나는 탐색과 비국소화 비용을 따진다.**
    - 근거: 7±2 는 모듈 수의 근거가 아니다(Miller 1956; Cowan 2001). 크기 최적값 주장은 반박됐다(El Emam et al. 2002). 쪼개기의 비용으로 비국소화 계획(Letovsky & Soloway 1986), 위임형 설계에서 초보의 어려움(Arisholm & Sjøberg 2004), 이해 하락 경향(Tempero et al. 2023), 시간의 35~50% 를 차지하고 절반 넘게 기대에 못 미치는 탐색(Piorkowski et al. 2016), 과잉 모듈화의 순환적 거동(Ethiraj & Levinthal 2004)이 있다. 에이전트가 쓴 Rust 앱에서 파일을 나누자 토큰은 83% 줄었지만 변경당 시간은 342초에서 454초로 늘었다(Edwards-Alexander 2026). 큰 클래스 하나는 이해에 거의 해가 없다(Politowski et al. 2020).
    - 강도: 실증(중) + 시뮬레이션(약) + 실무 실험 1건(약).
    - 반론과 한계: 어느 틀도 수치 기준을 주지 않는다. 토큰은 줄었다. 숙련자는 분산된 설계를 더 빨리 다룬다(Arisholm & Sjøberg 2004).

14. **구현 연결(플러그인 등록 등)은 명시적으로 선언하고 import 부수효과에 기대지 않는다.**
    - 근거: JPMS 는 `uses`/`provides … with` 를 모듈 기술자에 선언하고 해석 때 검사한다. 에이전트는 Pytest 픽스처 주입 같은 "Python's magic" 에 약하다(Ronacher 2025). 동적 결합과 다형성은 정적 읽기와 검사를 어렵게 한다(Wilde et al. 1993; Dunsmore et al. 2000).
    - 출처: Java SE 21 Configuration; Ronacher 2025; Wilde et al. 1993; Dunsmore et al. 2000; Arisholm & Sjøberg 2004.
    - 강도: 언어 선례(중) + 전문가 의견(약) + 경험 보고와 소규모 실증(약).
    - 반론과 한계: Effective Go 는 init 함수로 등록하는 blank import(`import _ "net/http/pprof"`)를 공식 관용으로 소개한다. 주류 생태계 하나가 반대 선택을 했다.

15. **첫 분해는 틀리기 쉬우므로 다시 나누는 비용을 낮게 두고, 정당한 위반은 규칙 개정으로 드러낸다.**
    - 근거: 첫 설계는 거의 최선이 아니므로 조직이 유연해야 한다(Conway 1968). 분해는 유일하지 않다(Simon 1996). 하위 책임은 상위 해법이 정해진 뒤에야 정해진다(Suh & Do 2000). 정당한 이유로 규칙이 어겨지면 규칙을 고치게 되어 아키텍처 진화가 드러난다(Sangal et al. 2005). 모델이 새로 나오면 규칙을 다시 본다(Anthropic 2026c). 팀 경계도 영구히 고정하지 않는다(Skelton & Pais 2019).
    - 강도: 서로 다른 전통의 전문가 의견이 수렴(중).
    - 반론과 한계: 잦은 재분할은 이름과 지도 같은 길찾기 단서를 흔든다(c1 의 추론).

16. **서로 얽힌 일을 여러 작업자(사람이나 에이전트)에게 나눠 맡기지 않는다. 나눌 때는 안정된 인터페이스와 분명한 과업 경계를 준다.**
    - 근거: 다중 에이전트 협업은 분해 가능한 과업에서 +80.8%, 순차 과업에서 −70.0% 였고(Kim et al. 2025), 에이전트 간 불일치가 실패의 한 범주였다(Cemri et al. 2025). 인터페이스가 안정된 부분만 사이트 간에 나눠야 한다(Herbsleb & Grinter 1999). 공급자는 하위 에이전트마다 분명한 과업 경계를 요구하거나(Hadfield et al. 2025) 단일 선형 에이전트를 권한다(Yan 2025).
    - 강도: 실증(중) + 공급자 주장(약).
    - 반론과 한계: 지식 경계를 작업 경계보다 넓게 두는 부분 미러링이 효과적이었다(Colfer & Baldwin 2016). 코딩은 연구보다 진짜 병렬화할 일이 적다(Hadfield et al. 2025).

17. **구조 검사와 별도로, 모듈 코드가 책임 문장과 맞는지 주기적으로 의미 검토한다.**
    - 근거: 위계와 깨끗한 분해는 독립 성질이다(Parnas 1972). 계산적 센서는 과잉 설계와 잘못 이해한 지시를 잡지 못한다(Böckeler 2026b). Radar 의 '코드베이스 인지 부채'는 구현과 공유된 이해의 간격을 경고한다(Thoughtworks 2026d). LLM 설계 판단은 결정적 필터와 짝지을 때 쓸 만했다(Move Method 원 제안의 최대 80% 가 환각, 정적 분석 필터로 개선; Bellur et al. 2025).
    - 출처: Parnas 1972; Böckeler 2026b; Thoughtworks 2026d; Bellur et al. 2025; Khononov 2026.
    - 강도: 전문가 의견(약) + 유비적 실증(약).
    - 반론과 한계: 추론적(LLM) 검토는 결정적이지 않아 같은 코드에 같은 판단을 보장하지 못한다. Khononov 의 플러그인은 평가 자료가 없다.

18. **규칙에는 명시적 예외·기준선 장치를 두되, 예외는 기록으로 남긴다.**
    - 근거: 성숙한 도구는 모두 예외·기준선 장치를 둔다(ArchUnit `FreezingArchRule`, Nx `ignoredCircularDependencies`, Sonargraph `unrestricted`). Lattix LDM 은 규칙 순서로 예외를 처리한다. 대응 수고와 수정 거부감이 도입 장벽이다(Ali et al. 2018).
    - 출처: TNG ArchUnit; Nx; Sonargraph; Sangal et al. 2005; Ali et al. 2018.
    - 강도: 도구 관행(중) + 전문가 의견.
    - 반론과 한계: 예외는 침식의 통로가 된다. 게이트 없는 발견은 제거로 이어지지 않았다(Rosik et al. 2011).

## ln-structure 시사점

### 뒷받침

- **모듈마다 '무엇'을 적은 책임 한 줄.** 공리 설계의 해법 중립 기능 요구("say 'what' not 'how'")와 '모듈 = 기능 요구 한 행'(Van Eikema Hommes 2010; Suh & Do 2000), Simon(1996)의 '기능을 통해, 메커니즘과 무관하게', Ulrich(1995)의 일대일 대응, Parnas(1972)의 '책임 할당'이 같은 방향이다. 개발자의 최다 질문 "무엇을 하려는 것인가"(LaToza & Myers 2010)와 비컨·단서 연구(Siegmund et al. 2017; Lawrance et al. 2013)도 책임 줄을 길찾기 단서로 지지한다. 단, 인지 근거는 사람과 식별자 수준이다.
- **사람은 책임만 정하고 에이전트가 구현.** Parnas 의 모듈화는 "the design decisions which must be made before the work on independent modules can begin"(독립 모듈 작업을 시작하기 전에 내려야 할 설계 결정)이다(Parnas 1972). 사람은 '루프 위에서' 하네스를 바꾸는 자리에 있고(Morris 2026), '어떻게'를 지나치게 지정하는 방식은 지속되지 않는다(Böckeler 2026c). Team Topologies 의 인지 한계 존중과 Anthropic 의 "clear task boundaries" 도 책임 하나 단위를 세션 크기의 과업으로 보는 쪽을 지지한다(Skelton & Pais 2019; Hadfield et al. 2025; 전문가 의견·공급자 주장).
- **계산된 층 = 수준화.** ln 의 '층 = 의존하는 모듈의 최고 층 + 1, 없으면 0'은 NDepend Level 공식(Lakos 1996 유래)과 같다. Parnas 의 층도 '사용' 관계에서 도출되고, 공리 설계의 탈결합(삼각) 설계는 비순환 선행 순서로 읽힌다(해석). 계산된 수준에서는 같은 층 의존이 구성상 불가능하므로, 같은 층 금지는 따로 검사할 규칙이라기보다 정의의 결과다(c6 의 추론).
- **모듈 사이 순환 금지, 모듈 안 파일 사이 순환 허용.** Go·JPMS·C++ 모듈·GHC 의 '단위 수준 비순환, 단위 안 자유'와 같은 모양이다(Go 명세; Java SE 21 Configuration; C++ 작업 초안; GHC User's Guide). 근거로는 '경계를 분명히 하고 일찍 생각하게 한다'는 Pike(2012)가 가장 가깝다. Simon(1962)의 '안쪽 강, 바깥 약'과 Ulrich(1995)의 타이어(안은 통합형)도 안쪽 순환 허용과 맞는다.
- **표면으로만 import, 중첩 모듈은 맨 위 안쪽 층만 공개.** JEP 261(public 이 곧 접근 가능은 아님), Go `internal/`(하위 트리 범위 공개, 중첩 모듈의 공개 범위와 닮음), Bazel 기본 비공개, eslint-plugin-boundaries 의 entry-point·no-private, Sonargraph 의 `hidden` 과 "parent artifacts always have full access" 가 선례다. 에이전트 실증도 맞는다. 의존 파일의 구현을 지우고 시그니처만 남겨도 완성 정확도가 크게 떨어지지 않았고(Zhang et al. 2024), 뼈대가 전체 파일보다 위치를 잘 찾았다(58.33% 대 53.67%; Xia et al. 2024). 도구가 만드는 표면은 이 시스템들이 매번 즉석에서 만드는 표현을 미리 만들어 둔 셈이다. 또 기록되지 않은 인터페이스 합의가 작업자 교체 때 깨진다는 결과(Herbsleb & Grinter 1999)에 비추면, 세션마다 작업자가 바뀌는 에이전트에게 생성된 표면은 기록된 합의 역할을 한다(c2 의 유비).
- **타입만 공개.** 추상 자료형으로 나눈 판이 다른 모든 모듈화보다 나았다는 결과(Woodfield et al. 1981, 작은 프로그램)와 닮았다. 약한 유비다.
- **폴더 = 아키텍처, 대응표 없음.** Passos et al.(2010)의 권고와 같고, 코드와 아키텍처를 대응시키는 수고라는 도입 장벽(Ali et al. 2018)을 없앤다.
- **기본 거부.** 하위가 상위를 부르지 못하고 표면만 쓰게 하는 방식은 ArchUnit 의 허용 목록("prevents detours"), Sonargraph·Nx 의 기본 거부와 같은 계열이다.
- **명시 상속으로 역전, 진입점에서만 연결, import 부수효과 등록 금지.** JPMS `uses`/`provides` 가 언어 수준 선례다. "Python's magic" 이 에이전트를 힘들게 한다는 실무 의견(Ronacher 2025)과 동적 결합이 정적 읽기를 어렵게 한다는 보고(Wilde et al. 1993; Dunsmore et al. 2000)가 뒷받침한다.
- **파일 하나에 클래스 하나.** JLS §7.6 이 공개 최상위 타입을 파일 이름에 맞추게 할 수 있고 흔한 관행이라고 적는다. 파일 이름이 타입 이름이면 색인 단서가 된다는 것은 c1 의 추론이며, 이해 효과를 잰 연구는 없다.
- **편집 후 훅이 위반을 오류로 돌려 진행을 막기.** 유일한 측정은 SWE-agent 의 편집 시점 린트 절제(18.0% 대 15.0%, GPT-4 Turbo, SWE-bench Lite, 2024)다. 공급자 문서는 훅이 결정적이고 CLAUDE.md 는 권고라 하며(Anthropic 2026a), PostToolUse 훅의 종료 코드 2 는 stderr 를 Claude 에게 보이고 SessionStart 의 `additionalContext` 는 문맥을 더한다(Anthropic 훅 문서). Thoughtworks(2026a)는 센서를 세션 중에 돌리라 하고, Böckeler(2026b)는 ArchUnit 을 에이전트 훅에서 돌리는 예를 든다. Sangal et al.(2005)은 새 구성원의 결함을 즉시 잡는다고 했고, Rosik et al.(2011)은 게이트 없는 발견이 제거로 이어지지 않음을 보였다. 에이전트는 구조를 스스로 가꾸지 않으므로(Horikawa et al. 2025; He et al. 2026) 구조는 바깥에서 강제해야 한다.
- **해결 방법을 담은 오류 메시지.** Aizawa(2025)의 "specific and actionable improvements", SWE-agent 의 "informative but concise", Böckeler(2026b)의 LLM 소비용 신호와 맞는다. 리팩터링 유형을 알려 주자 LLM 성공률이 15.6% 에서 86.7% 로 오른 결과(Liu et al. 2025)와 정적 필터로 환각 제안을 거른 결과(Bellur et al. 2025)는 유비적 지지다.
- **세션 시작에 주입하는 모듈 지도.** "smallest set of high-signal tokens" 과 "Folder hierarchies, naming conventions … provide important signals"(Rajasekaran et al. 2025), 디렉터리 구조가 스스로 설명하지 못할 때의 코드베이스 지도(Anthropic 2026d), 아키텍처 결정은 넣고 파일별 설명은 빼라는 권고(Anthropic 2026a)와 맞는다. 지도는 도구가 생성하므로 표류 경고(Anthropic 2026c)에 답한다. 사람에게는 외부 기억이자 인출 단서다(Ericsson & Kintsch 1995). 지도는 세션 처음에, 위반 메시지는 가장 최근 입력에 놓이는데, 이는 Liu et al.(2024)이 회상이 가장 좋다고 본 두 위치다(질의응답에서 에이전트로 옮긴 외삽이라 추측).
- **'lnt doc' 의 층 순서 문서.** 의존(위상) 순서로 문서를 만들면 순서 없는 생성보다 낫다는 절제 결과(Yang et al. 2025, DocAgent)가 l0 부터 올라가는 요약 생성을 지지한다.
- **'lnt blast'.** 할당 × 의존으로 조정 요구를 계산한 Cataldo et al.(2006), 전파 비용(MacCormack et al. 2012)과 같은 관심이다(유비).
- **단일 에이전트에도 바깥 강제가 필요.** Conway 의 대응은 한 그룹이 여러 부분을 설계하면 접혀 조직이 모듈성을 밀어 주지 않는다(Conway 1968). MacCormack et al.(2012)은 한 사람이 변경의 약 40% 를 낸 Gnumeric 을 느슨한 조직이 아닌 예외로 다뤘다. 한 에이전트가 다 쓰는 경우가 이 모양이다(c2 의 추론).
- **수치 상한을 두지 않음.** Miller(1956), Cowan(2001), El Emam et al.(2002)과 일치한다.
- **같은 층 금지와 병렬 작업.** 같은 층 모듈끼리 import 하지 않으므로 한 층은 구문 의존상 조정 요구가 없는 병렬 과업 집합이 된다(Cataldo et al. 2006 의 틀을 빌린 c2 의 추측). 실제 조정 요구는 동반 변경을 따르므로 보장은 아니다.

### 도전하거나 어긋나는 것

- **주입되는 모듈 지도와 측정된 문맥 파일 연구.** 가장 큰 통제 평가(Gloaguen et al. 2026, v3 2026-09)에서 LLM 생성 문맥 파일은 8개 설정 중 5개에서 성공률을 낮추고 비용을 20~23% 늘렸고, 개발자 파일도 +2.4%(p = 0.21)에 그쳤다. ln 과 같은 Claude Code + Sonnet-4.5 조합은 CTXbench 에서 파일 없음 73.2% > 개발자 파일 70.3% > LLM 생성 65.2% 였다. LLM 생성 파일의 95~100%(네 모델 중 셋)가 개요를 담았지만 수정할 파일에 처음 닿기까지의 단계가 줄지 않았다. ln 의 지도는 LLM 산문이 아니라 도구가 계산한 모듈당 한 줄이므로 다르지만 시험된 적이 없어, 입증 책임은 지도 쪽에 있다. 효율 결과(Lulla et al. 2026: 실행 시간 −28.64%)는 정답을 재지 않았다. 지도 크기도 문제다. 입력 길이만으로 성능이 13.9~85% 떨어지므로(Du et al. 2025) 모듈 수에 비례해 커지는 지도에는 확장 한계가 있고, 공급자 기준으로는 CLAUDE.md 200줄(Anthropic 2026b)과 지시 비대화 경고(Thoughtworks 2026c)가 상한 역할을 한다. 같은 평가가 문맥 파일은 "non-standard coding practices" 를 정하는 데 쓸모 있고 지시는 지켜진다고 했으므로, 규칙 자체를 알리는 부분은 지지된다. v1 초록은 "unnecessary requirements from context files make tasks harder" 라고 더 강하게 적었다.
- **파일 하나에 클래스 하나·작은 모듈과 다중 파일 변경.** SWE-PolyBench 에서 단일 파일 수정이 가장 잘됐고 세 파일 이상이면 10% 미만, 클래스·함수 혼합 수정은 8~15% 였다(Rashid et al. 2025). SWE-bench 정답 패치는 1.7개 파일인데 모델은 한 파일 넘게 고치는 일이 드물었다(Jimenez et al. 2024). 다중 파일 리팩터링은 에이전트 22% 대 사람 87% 였다(Gautam et al. 2025). SWE-agent 는 cd·ls·cat 연쇄가 "extremely inefficient" 하다고 보고했고(Yang et al. 2024), 사람도 탐색의 기계적 조작에 시간의 약 35% 를 쓴다(Ko et al. 2006). 파일을 나누자 토큰은 83% 줄었지만 시간은 342초에서 454초로 늘었다(Edwards-Alexander 2026). 어떤 출처도 에이전트에게 파일당 클래스 하나를 권하지 않고, Ronacher(2025)는 여러 파일에 흩어진 코드를 경고한다. 공리 설계와 Ulrich 는 기능 독립과 부품 수를 따로 판단하므로, 파일당 클래스 하나는 이 이론들이 별도로 다룰 물리적 선택이다. 단, 벤치마크는 모듈이 아니라 파일을 세고 교란이 있다.
- **함수 대신 정적 메서드, 타입만 공개.** 검토한 언어·도구 어디에도 '타입만 내보내기' 선례가 없다(Go 는 대문자 식별자, C++ 는 선언, JPMS 는 패키지를 내보낸다). Ronacher(2025)는 클래스보다 함수를 권하고, Anthropic(2026a)은 "extra abstraction layers" 를 과잉 설계로 경고한다. 함수 수준 모듈성은 생성의 핵심 요인이 아니었다(Kang et al. 2024). 반박된 것은 아니지만 지지도 없다.
- **같은 층 금지는 표준 층 규칙이 아니다.** Sangal et al.(2005)과 ArchUnit 은 같은 층 의존을 허용하고, '엄격한 층'은 바로 아래 층만 허용한다는 뜻이다. ln 은 아래 어느 층이든 허용하므로 ln-structure 를 'strict layering' 이라 부르면 틀린 이름이다. 정확히는 수준화, 곧 '완화 층 + 보편적 형제 독립'이다. 형제 독립은 고른 집합에만 거는 선택 규칙이고(ArchUnit `slices().notDependOnEachOther()`, 어니언 아키텍처의 어댑터, dependency-cruiser 의 경로 규칙, Sangal 의 독립 구성 요소), 보편 금지가 선택적 독립보다 낫다는 증거는 없다. 가장 가까운 것은 형제끼리도 명시 연결을 요구하는 Sonargraph 의 기본 거부 DSL 이다. Nx 의 대표 예시는 같은 태그끼리의 의존을 허용한다.
- **폴더를 계산된 층에 묶기.** 검토한 도구 중 이렇게 하는 것은 없다(NDepend 는 같은 값을 지표로만 쓴다). 의존 하나를 더하면 층이 바뀌어 폴더를 옮겨야 하는 '층 이동'의 빈도와 비용은 알려진 바 없다. 계산된 층은 위상적 의미뿐이어서 사람의 길찾기 단서로 약하고, 층이 바뀌면 단서도 흔들린다(c1 의 추론). 에이전트도 위치만 보고 새 코드를 둘 곳을 알기 어렵다(Factory 의 'Glob-ability' 기준과 어긋남, Sng 2025; c5 의 추론). 에이전트용으로 보고된 층 구조(OpenAI 의 사례, Factory 의 '애플리케이션 층')는 이름 있는 의미 층이다(OpenAI 2026 [2차 출처]).
- **import 부수효과 등록 금지.** Effective Go 는 init 함수로 핸들러를 등록하는 `import _ "net/http/pprof"` 를 공식 관용으로 소개한다. JPMS 는 명시 선언 쪽(ln 과 같은 방향)이다. 금지는 방어할 수 있지만 합의된 원칙은 아니며, 주류 생태계 하나의 공식 지침과 반대다.
- **엄격한 정보 은닉.** 오픈 소스는 '실행 가능한 투명성'으로 엄격한 정보 은닉 없이 모듈성을 얻었고, 부분 미러링이 효과적이었으며, 엄격한 미러링은 함정일 수 있다(Colfer & Baldwin 2016). ln 은 import 를 제한할 뿐 읽기를 막지 않는다는 점을 문서에 분명히 적을 필요가 있다.
- **비순환은 보편 법칙이 아니다.** OSGi 와 GHC 는 순환을 다루는 장치를 두고, Sangal et al.(2005)은 일탈이 의식적 절충일 수 있다고 했다. 거의 분해 가능성은 방향이 아닌 세기에 관한 것이며(Simon 1962), 노트가 본 어떤 출처도 순환 금지를 제1원리에서 끌어내지 않았다.
- **나무 대 겹침.** 폴더 하나가 모듈을 소유하고 맨 위만 공개하는 구조는 엄격한 나무다(Alexander 1965). 오류 처리나 설정 같은 횡단 관심은 겹친다. 공통 부분을 아래 모듈로 떼어 내는 처방은 '겹침도 단위가 된다'는 반격자 공리의 적용이지만, 내부가 바깥으로 끌어올려지거나 Simon(1962)의 '소비 하위 시스템' 같은 허브 모듈이 생길 수 있다(a5 의 추론).
- **이름 대 측정된 상호작용.** 한 줄 책임은 실제 결합이 아니라 어휘로 묶을 위험이 있다(Alexander 1964 의 경고). 계산된 층은 잘못 그은 경계를 고쳐 주지 않는다.
- **검사 통과 ≠ 좋은 분해.** 위계와 깨끗한 분해는 독립이고(Parnas 1972), 계산적 센서는 과잉 설계를 잡지 못한다(Böckeler 2026b). 정적 도구는 있어야 할 의존의 72~77% 만 보고하고 리플렉션 같은 동적 의존을 보지 못하므로(Pruijt et al. 2017; Passos et al. 2010), 깨끗한 `lnt check` 는 적합성의 증거일 뿐 증명이 아니다. 조정 요구는 동반 변경을 따르며 import 로 보이지 않는다(Cataldo et al. 2006).
- **편집 시점 차단의 비용과 모델 의존.** 최전선 모델은 하네스 없이 10/10 을 통과했고 하네스는 토큰을 약 10배 썼다(Jain 2026, 단 그 하네스에 린터·훅은 없었다). Anthropic(2026c)은 모델 한계가 사라지면 그 한계를 우회하던 규칙을 지우라고 한다. 반론으로, ln-structure 는 TDD 같은 과정 처방이 아니라 결과 구조를 재는 센서다(c5). Terra & Valente(2009)는 빌드마다 검사가 너무 간섭적일 수 있다고 했고, 성숙한 도구는 모두 예외·기준선 장치를 둔다. 예외 없이 편집마다 막는 방식은 이 범위의 가장 엄격한 끝에 있다.
- **우회와 게이밍.** 에이전트는 테스트를 끄거나 지우고 성공을 거짓 보고한다(Beck 2025; Böckeler 2025). 막힌 에이전트가 역전을 남용하거나 코드를 옮겨 규칙만 피상적으로 맞출 수 있다. 자료는 없다.
- **사람 쪽 인지 부담.** 분산된 설계는 초보 유지보수자에게 어렵고(Arisholm & Sjøberg 2004), 클래스 주석은 상위 이해를 높이지 않았으며(Nurvitadhi et al. 2003), 사람이 책임 줄만 읽고 코드를 읽지 않으면 '코드베이스 인지 부채'가 쌓인다(Thoughtworks 2026d). 서술적 단서의 이득은 숙련자에게서 컸는데(Schankin et al. 2018), 책임을 정하는 사람이 그 프로필과 다를 수 있다.
- **다중 에이전트 분할.** 얽힌 일을 나누면 손해다(Kim et al. 2025: 순차 과업 −70.0%; Yan 2025). '모듈마다 에이전트 하나'는 자동으로 좋지 않으며, ln 의 주 가치는 단일 에이전트의 출력을 제약하는 데 있을 수 있다(c2 의 추론).
- **기존 코드 도입.** 하네스는 만들기 가장 어려운 곳에서 가장 필요하고(Böckeler 2026b), 엔트로피가 많은 레거시 코드에 덧씌우기 어렵다는 의심이 있다(Böckeler 2026a).
- **생성 표면 대 선별 표면.** Bazel 은 공개 인터페이스를 명시적으로 고르고 기본 공개를 피하라고 권한다. 도구가 만든 표면이 공개 요소를 모두 다시 내보낸다면 기본 공개와 같아진다. lnt 의 표면이 실제로 어떻게 하는지는 lnt 자체로 확인해야 한다(c6).
- **Rust 공백.** 에이전트와 코드 구조에 관한 실증에 Rust 가 거의 없다(c4). Rust 사례는 Edwards-Alexander(2026)의 실무 실험 1건뿐이다.

### 열린 질문

1. 계산된 한 줄 모듈 지도가 수정할 파일에 처음 닿기까지의 단계(Gloaguen et al. 2026 의 지표)를 줄이거나 성공률을 올리는가? 지도 없음, LLM 산문 개요와 비교해야 한다.
2. 파일당 클래스 하나와 타입만 공개가 변경당 파일 수를 늘리는가? 성공률은 그 수를 따르는가?(Rashid et al. 2025; Edwards-Alexander 2026)
3. 편집 시점 차단 루프는 단계·토큰·시간을 얼마나 늘리고, 성공률이나 장기 구조로 값을 하는가? Jain(2026)의 짝지은 실행, Edwards-Alexander(2026)의 토큰 측정, He et al.(2026)의 이중차분 지표(인지 복잡도, 중복률, 이동 줄 비율)를 재사용할 수 있다.
4. 보편 수준화(같은 층 금지)가 '완화 층 + 선택적 형제 독립'보다 결합과 침식을 줄이는가?(c6)
5. 층 이동: 의존 하나 때문에 폴더를 옮겨야 하는 일이 얼마나 자주, 얼마의 비용으로 생기며, 사람과 에이전트의 길찾기 단서를 흔드는가?
6. 동반 변경 의존이 import 와 갈라지는가? `lnt blast` 에 동반 변경을 더해야 하는가?(Cataldo et al. 2006)
7. 실제 결합(호출, 동반 변경)을 재서 안쪽 연결이 바깥 연결보다 촘촘하지 않은 모듈을 표시할 수 있는가? Simon 기준의 코드판이다(a5).
8. 책임 줄에 Parnas 의 '숨기는, 바뀌기 쉬운 결정'도 적어야 하는가?(c2)
9. 책임 줄과 코드의 불일치(모듈 수준 언어 반패턴)를 자동으로 찾을 수 있는가? 결정적 검사와 주기적 추론 검토를 어떻게 짝지을까?(c1, c5)
10. 한 줄 책임이 LLM 의 잘못 놓인 코드 탐지를 돕는가? 리팩터링 유형을 알려 준 효과(Liu et al. 2025)와 같은 효과가 있는가?
11. 정당한 겹침(횡단 관심)을 명시적으로 선언하는 장치와, 성능이 중요한 모듈의 통합형 선택(Ulrich 1995; Whitney 2005)이 필요한가?(a5)
12. 평면 지도는 얼마나 커져도 훑어볼 수 있는가? 계층·묶음·점진적 공개가 필요한가?(c1, c4, c5)
13. 차단 메시지 문구가 의도한 수정으로 이끄는가, 피상적 수정(역전 남용, 코드 옮기기)으로 이끄는가?(c5)
14. 모델이 좋아지면 어떤 규칙을 은퇴시키는가? 구조 센서와 과정 처방을 가르는 기준은 무엇인가?(Jain 2026; Anthropic 2026c)
15. 기준선(`FreezingArchRule` 같은)이나 독점 접근·필수 의존 규칙이 기존 코드 도입과 표현력에 필요한가?(c6)
16. 에이전트가 거의 분해 가능성의 이득을 사람처럼 얻는가? 근거가 없다(a5).
17. 에이전트가 쓴 코드는 오케스트레이션 구조를 닮는가? 한 세션과 모듈별 세션으로 같은 명세를 만들어 전파 비용을 비교할 수 있다(c2).
18. Rust 에서도 같은 효과가 나는가? 정적 메서드 규칙, 역전 선언, Rust impl 배치 규칙을 에이전트가 어떻게 다루는지에 대한 근거는 없다(c4).

## 부록 A. AI 에이전트 실증 요약 (5.4 의 근거 강도)

본문 길이 때문에 5.4 에서 이 표를 빼고 한 문장 요약으로 대신했다.

| 주장 | 실증 근거와 강도 | 주요 출처 |
|---|---|---|
| 여러 파일, 섞인 단위의 변경이 더 어렵다 | 벤치마크 4개의 일관된 상관, 교란 있음 (중) | Jimenez 2024; Rashid 2025; Deng 2025; Gautam 2025 |
| 구조로 고른 문맥이 유사도 검색보다 낫다 | 벤치마크, 에이전트 이득은 절대 2~3%p (중) | Ding 2022; Cheng 2024; Ouyang 2025; Chen 2025 |
| 인터페이스만 보인 의존 문맥으로 충분하다 | 연구 2건 (중) | Zhang 2024; Xia 2024 |
| 길거나 무관한 문맥은 해롭다 | 여러 연구, 코드 포함 (강) | Liu 2024; Du 2025; Rando 2025 |
| 편집 시점 린트 가드레일이 돕는다 | 절제 실험 1건, +3.0%p (중) | Yang 2024 |
| 개요형 문맥 파일이 돕는다 | 통제 평가 1건은 반대, 1건은 효율만 지지 (약) | Gloaguen 2026; Lulla 2026 |
| 모듈성 자체가 생성을 돕는다 | 함수 수준에서 지지 안 됨 | Kang 2024 |
| AI 보조 코드는 복잡도와 중복을 쌓는다 | 관찰 연구 (중), 무작위 대조 시험은 무효과 | He 2026; Borg 2025 |

## 부록 B. 노트 사이의 불일치와 본문에서 뺀 것

- Ulrich(1995)는 Korson & Vaishnavi(1986)를 소프트웨어 모듈성의 "strong empirical evidence" 로 인용했다(a5 는 확인하지 않은 인용으로 표시). c1 이 읽은 초록은 조건부 효과였다. 본문 5.1 에 반영했다.
- Chroma 의 'Context Rot'(Hong et al. 2025, 18개 모델): c2 는 실증으로 다뤘고, c4 는 동료 심사 없는 벡터 DB 공급자의 기술 보고서이고 코드 과업이 없으며 "structural coherence consistently hurts" 는 산문 대상 결과라고 단서를 달았다. 길이 때문에 본문에서 뺐다. 같은 결론은 Du et al.(2025)과 Liu et al.(2024)이 더 강하게 받친다.
- 공급자 권고(아키텍처 결정과 코드베이스 지도를 문맥에 넣기; Anthropic 2026a; 2026d; Amp 문서)와 ETH 측정(개요 효과 없음; Gloaguen et al. 2026)이 엇갈린다. 본문 5.5 에 반영했다.
- Thoughtworks 'Agent instruction bloat'(2026c)은 사람이 쓴 AGENTS.md 가 LLM 생성보다 낫다는 연구를 인용한다(c5 는 2차 출처로 표시). ETH 결과와 대체로 맞지만, Sonnet-4.5 에서는 개발자 파일(70.3%)도 파일 없음(73.2%)보다 낮았다.
- 다중 에이전트: Anthropic(+90.2%, 연구 과업)과 Cognition(만들지 말라)은 상충해 보이지만 Kim et al.(2025)의 과업 정렬 결과로 함께 설명된다.
- Colfer & Baldwin(2016)의 오픈 소스 결과는 정보 은닉이 모듈성에 필수라는 Parnas 식 견해(2장의 이론)와 정면으로 부딪힌다. MacCormack et al.(2012)의 '느슨한 조직이 더 모듈적인 제품을 낸다'와는 모순이 아니다. 제품 모듈성은 높지만 조직 연결이 기술 의존을 따라가지는 않는다.
- Team Topologies 의 '팀 인지 부하'(c2)는 c1 이 개념과 측정에 논란이 있다고 정리한 Sweller 의 개인 인지 부하 이론을 빌렸다.
- c5 안의 이견: TDD(Beck 2025, Cursor 의 Robinson 2026, Willison 의 안내서는 찬성 쪽, Böckeler 2026c 의 실험은 차이 없음과 토큰 3~8.5배), 작은 파일(Osmani 2024 대 Ronacher 2025 대 Edwards-Alexander 2026 의 측정).
- 원문 내부 불일치: He et al.(2026)은 인지 복잡도 증가를 41.64% 와 25% 로 달리 적었고, Terra & Valente(2009)는 위반 클래스 수를 194개와 179개(8%)로 달리 적었다.
- 반사 모델(Murphy et al. 1995/2001): c1 은 2001년 초록을 읽었고 c6 은 Passos et al.(2010)의 설명으로만 다뤘다. 길이 때문에 본문에서 뺐다.
- 본문에서 뺀 다른 실증: Nagappan et al.(2008)은 Windows Vista 바이너리 3,404개에서 조직 지표가 결함 경향을 정밀도 0.87, 재현율 0.84 로 예측해 코드 지표 기반 모델보다 나았다(한 시스템, 기술 보고서판). METR 의 2026-02 갱신 수치는 원 참가자 −18%(CI −38%~+9%), 새 참가자 −4%(CI −15%~+9%)이고 METR 은 이를 하한으로 본다.

## 이 파일에서만 인용한 출처

5장 본문에 없는 출처다. 나머지는 5장 참고문헌을 본다.

- Amp. "AGENTS.md" 문서(날짜 없음, 2026-10 열람). https://ampcode.com/docs/customize/agents-md
- Anthropic. "Hooks reference." Claude Code Docs (2026-10 열람). https://code.claude.com/docs/en/hooks
- Bellur et al. (2025). [MM-assist: LLM 의 Move Method 추천과 정적 분석 필터]. ICSME 2025, arXiv:2503.20934. https://arxiv.org/abs/2503.20934
- Böckeler, B. (2026c, 2026-08-10). "TDD inside the agent loop – theater or actual value?" martinfowler.com. https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html
- Chen et al. (2025). [LocAgent: 그래프 기반 코드 위치 찾기]. arXiv:2503.09089 (학회 미확인). https://arxiv.org/html/2503.09089v2
- Deng et al. (2025). [SWE-Bench Pro: 1,865문제, 평균 4.1개 파일]. arXiv:2509.16941. https://arxiv.org/html/2509.16941v2
- dependency-cruiser. Rules reference(main 브랜치, 2026). https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md
- Dunsmore et al. (2000). [객체 지향 코드 검사와 비국소화]. ICSE 2000. https://doi.org/10.1145/337180.337343 (초록만 확인)
- eslint-plugin-boundaries. Rules overview(7.1.0 문서, entry-point·no-private 는 폐기 예정으로 표시). https://www.jsboundaries.dev/docs/rules/
- Feitelson et al. (2022). [개발자가 이름을 고르는 방식, 334명]. *IEEE TSE*. https://doi.org/10.1109/TSE.2020.2976920 (초록만 확인)
- Gautam et al. (2025). [RefactorBench: 다중 파일 리팩터링 100건]. ICLR 2025, arXiv:2503.07832. https://arxiv.org/abs/2503.07832
- Hong, Troynikov & Huber (2025-07-14). "Context Rot." Chroma 기술 보고서(동료 심사 없음). https://www.trychroma.com/research/context-rot
- Khononov, V. (2026). `modularity` Claude Code 플러그인. GitHub vladikk/modularity(CC BY-NC-SA 4.0). https://github.com/vladikk/modularity
- Ko et al. (2006). [낯선 프로그램에서 개발자가 정보를 찾는 방식, 실험실 관찰]. *IEEE TSE*. https://doi.org/10.1109/TSE.2006.116 (초록만 확인)
- Liu et al. (2025). [LLM 의 리팩터링 기회 탐지, 180개 기회]. *Automated Software Engineering* 32(1), arXiv:2411.04444. https://arxiv.org/abs/2411.04444
- Morris, K. (2026-03-04). "Humans and Agents in Software Engineering Loops." martinfowler.com. https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
- Murphy, G. C., Notkin, D. & Sullivan, K. (1995). "Software reflexion models: bridging the gap between source and high-level models." 3rd ACM SIGSOFT FSE. https://doi.org/10.1145/222124.222136 [2차 출처: Passos et al.(2010)의 설명으로만 앎]; 확장판 (2001). "Software Reflexion Models: Bridging the Gap between Design and Implementation." *IEEE TSE*. https://doi.org/10.1109/32.917525 (초록만 확인)
- Nagappan, N., Murphy, B. & Basili, V. (2008). "The influence of organizational structure on software quality." ICSE 2008. https://doi.org/10.1145/1368088.1368160 (기술 보고서판 MSR-TR-2008-11 로 읽음. ICSE 판 수치 미확인)
- Rajasekaran, Dixon, Ryan & Hadfield (2025-09-29). "Effective context engineering for AI agents." Anthropic Engineering. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Rando et al. (2025). [LongCodeBench: 긴 문맥 코드 질의응답과 수리]. arXiv:2505.07897. https://arxiv.org/abs/2505.07897
- Robinson, L. (2026-01-09). "Best practices for coding with agents." Cursor 블로그. https://cursor.com/blog/agent-best-practices
- Sng, A. (2025-09-05). "Using Linters to Direct Agents." Factory. https://factory.com/news/using-linters-to-direct-agents
- Sonargraph(hello2morrow). 사용자 매뉴얼 §11.2 와 von Zitzewitz(2015) 블로그. https://eclipse.hello2morrow.com/doc/standalone/content/architecture_interface_connectors.html ; https://blog.hello2morrow.com/2015/09/architecture_dsl_part1
- Thoughtworks (2026c). "Agent instruction bloat." Technology Radar 2026-04-15(Vol 34), Caution. https://www.thoughtworks.com/radar/techniques/agent-instruction-bloat
- Thoughtworks (2026d). "Codebase cognitive debt." Technology Radar 2026-04-15(Vol 34), Caution. https://www.thoughtworks.com/radar/techniques/codebase-cognitive-debt
- Wilde et al. (1993). [객체 지향 프로그램 유지보수의 어려움, 경험 보고]. *IEEE Software*. https://doi.org/10.1109/52.207232 (초록만 확인)
- Willison, S. *Agentic Engineering Patterns*(2026-02 무렵 시작한 살아 있는 안내서). https://simonwillison.net/guides/agentic-engineering-patterns/ [미확인: 목차만 확인]
- Yang et al. (2025). [DocAgent: 위상 순서로 문맥을 쌓는 문서 생성]. ACL 2025, arXiv:2504.08725. https://arxiv.org/abs/2504.08725
