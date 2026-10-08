# 0.2 에서 0.3 으로 옮기기

0.2 에서 위반이 없던 프로젝트도 0.3 에서는 위반이 나고 `__init__.py` 가 바뀐다.
규칙 전문은 `src/lntools/protocol/for-agent-codingprotocol-ln-structure.md` 이다.

## 바뀐 것

1. 객체 기반 표면. 모듈이 공개하는 이름은 클래스와 타입 별칭뿐이다
   - 함수는 메서드로, 상수는 클래스 속성으로, 진입 함수 `main` 은 진입 클래스의 메서드로 둔다
   - 이름이나 파일 이름이 `_` 로 시작하면 비공개다
   - C2 가 넓어졌다. 표면에 없는 이름을 import 하는 것, 같은 층에서 공개 이름이 겹치는 것도 위반이다
2. `__init__.py` 는 패키지 루트까지 모두 `lnt doc` 이 만든다
   - 모듈은 자기 파일의 공개 이름을, 중첩 모듈과 패키지 루트는 맨 위 층의 표면을, 층은 그 층 모듈 표면의 합을 내보낸다
   - 손으로 쓴 내용은 사라진다. 다만 쓰면 사라질 정의가 있으면 그 파일은 쓰지 않고 알린다
   - `__main__.py` 는 진입 스크립트라 만들지 않는다
3. 문서. `lnt init` 은 ln-structure 문서 하나만 설치한다(0.2 부터)
   - python 코딩 프로토콜, moduleinfo 와 layerinfo 템플릿, 모듈마다의 `for-agent-moduleinfo.md`,
     층마다의 `for-agent-layerinfo-lN.md` 는 lnt 가 더 만들지도 읽지도 않는다
   - 시그니처는 `lnt sig` 로 그 자리에서 본다. 위반이 아닌 점검 대상은 `lnt review` 로 본다

## 0.2 가 깔린 채로 옮기기

lnt 명령은 모두 0.3 소스로 돌린다. 프로젝트 루트에서:

```
# bash
PYTHONPATH=<ff-lntools>/src python -m lntools check
# PowerShell
$env:PYTHONPATH = "<ff-lntools>/src"; python -m lntools check
# 저장소 없이 PyPI 판으로
uvx --from ff-lntools==0.3.0 lnt check
```

아래의 `lnt X` 는 이 형태로 읽는다.
훅은 계속 0.2 로 돈다. 0.2 의 훅, `check`, `doc` 은 0.3 에 맞춘 코드와 `__init__` 에서 틀린 결과를 내지 않는다(실측).
0.2 의 `doc` 은 `__init__` 을 만들지 않을 뿐이다. `move` 만 0.2 로 돌리지 않는다. 층 `__init__` 을 예전 형식으로 다시 써서 중첩 모듈의 이름을 빠뜨린다.

## 순서

1. `lnt init` 으로 `.claude/` 의 ln-structure 문서를 0.3 판으로 바꾼다. 있는 CLAUDE.md 는 그대로 두고, 훅이 없던 프로젝트에는 훅을 더한다
   - lnt 가 더 배포하지 않는 문서 `.claude/for-agent-codingprotocol-python.md`, `.claude/for-agent-*-template.md` 를 지운다
   - CLAUDE.md 가 그 문서들을 가리키면 그 줄을 지운다. 새 문구는 `src/lntools/protocol/CLAUDE-template.md` 의 '구조 규칙' 절
2. `lnt check` 의 위반을 고친다
   - 표면에 없는 이름: 함수는 그 책임의 클래스 메서드로, 상수는 클래스 속성으로 옮기고 쓰는 곳을 `Class.name` 으로 바꾼다
   - 이름 겹침: 같은 층의 두 모듈이 같은 이름을 내놓는다. 이름을 바꾸거나 한 모듈로 모은다
   - 예전부터 있던 위반(C1, C3, C4)도 같이 고친다. 메시지 뒤에 풀이가 붙는다
3. `lnt doc` 으로 `__init__.py` 와 layerinfo 를 다시 만든다. "지울 수 없는 정의가 있어 쓰지 않음" 알림이 없어질 때까지 고치고 다시 돌린다
   - `__init__` 안에 정의한 함수, 상수, 객체는 모듈 파일의 클래스로 옮긴다
   - 그 `__init__` 경로로 import 하던 곳은 그 이름이 있는 모듈 표면에서 import 하게 고친다
   - 다른 모듈의 이름을 다시 내보내던 `__init__` (루트가 맨 위 층이 아닌 이름을 내보내던 경우 등)은 고친 뒤에도 알림이 남는다. 그 파일을 지우고 다시 `lnt doc`
   - 진입 함수 `main` 을 클래스 메서드로 옮기면 pyproject 의 `[project.scripts]` 도 `pkg.l4.cli:Cli.main` 처럼 바꾸고, `__main__.py` 도 그 메서드를 부르게 한다
   - 프레임워크가 경로로 찾는 객체(ASGI `app` 등)는 클래스가 아니라 표면에 들지 않는다. 실행 설정이 그 객체를 정의한 파일을 가리키게 한다
   - 중첩 모듈 안쪽 층에도 모듈 폴더가 있어야 한다(`portfolio/l0/tick_snapshot/tick_snapshot.py`). 층 폴더에 파일을 바로 두었으면 모듈 폴더로 옮긴다
4. 예전 문서를 지운다. `for-agent-moduleinfo.md` 와 `for-agent-layerinfo-lN.md` 에 남길 내용이 있으면 layerinfo 의 책임 한 줄이나 Notes 로 옮긴다
5. 테스트를 돌린다. 지연 로드로 바뀐 `__init__` 은 이름을 쓸 때 import 하므로, import 부수효과에 기대던 코드가 있으면 여기서 드러난다

끝난 상태: `lnt check` 위반 0, `lnt doc --check` 불일치 0, `lnt doc` 알림 0, 테스트 통과. `lnt review` 는 참고로 본다.
