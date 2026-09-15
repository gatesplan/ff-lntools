# ff-lntools

ln-structure 프로젝트용 정적 검사, 영향 범위, 문서 생성 도구와 Claude Code 훅.
표준 라이브러리만 사용. Python 3.10+.

ln-structure 규칙: `src/lntools/protocol/for-agent-codingprotocol-ln-structure.md`

## 설치

```
pip install ff-lntools
```

프로젝트가 쓰는 Python 환경마다 설치한다. 훅이 `python -m lntools` 로 호출하기 때문이다.

## 프로젝트 세팅

```
lnt init --skill    # 1회. ~/.claude/skills/init-protocol 스킬 설치
cd my-project
lnt init            # .claude/ 에 프로토콜 문서 복사, CLAUDE.md 생성, 훅 병합
```

Claude Code 에서는 `/init-protocol` 이 같은 일을 한다. 코딩 프로토콜 문서의 원본은 이 저장소의
`src/lntools/protocol/` 이다.

## 명령

```
lnt init [--skill]          # 프로젝트에 코딩 프로토콜 설치
lnt check [--file PATH]     # C1 방향, C2 표면, C3 층 일치, C4 순환. 위반 시 exit 1
lnt blast MODULE [-d N]     # MODULE 변경 시 영향받는 상위 모듈. 인터페이스 상속 경유 포함
lnt map                     # 모듈 목록, 층, 의존
lnt doc                     # for-agent-layerinfo.md, for-agent-layerinfo-lN.md 생성
lnt doc --check             # 생성 결과와 파일 비교. 다르면 exit 1
lnt doc --stamp MODULE      # for-agent-moduleinfo.md 의 sources hash 갱신
lnt move MODULE lK          # 모듈을 lK 로 이동. 패키지/tests 의 import 재작성, tests 미러 이동,
                            # 두 층의 __init__ 을 지연 re-export 로 재생성, 문서 재생성
lnt hook post-edit          # Claude Code PostToolUse 훅 진입 (stdin JSON)
lnt hook session-start      # Claude Code SessionStart 훅 진입
```

`--root` 로 프로젝트 안의 아무 경로를 주면 `src/<pkg>/lN` 을 찾아 올라간다. 기본은 현재 디렉토리.

## 검사 규칙

| 코드 | 내용 |
|---|---|
| C1 | import 대상 층이 자기 층보다 낮아야 한다. 같은 층도 위반. `TYPE_CHECKING` 안의 import 도 포함 |
| C2 | `pkg.lN.module` 표면까지만 import. 모듈 안의 파일이나 중첩 모듈 내부로 진입 금지 |
| C3 | 선언 층 == 계산 층 (의존 최고 층 + 1, 의존 없으면 0, 외부 패키지 의존이 있으면 최소 1) |
| C4 | 모듈 간 runtime import 순환 금지. 모듈 내부 파일 간 순환은 규칙 밖 |

## Claude Code 훅

`.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup|resume|clear|compact",
      "hooks": [{"type": "command", "command": "python -m lntools hook session-start"}]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{"type": "command", "command": "python -m lntools hook post-edit", "timeout": 30}]
    }]
  }
}
```

- session-start: `src/<pkg>/for-agent-layerinfo.md` 를 세션 컨텍스트에 주입
- post-edit: 편집한 파일이 `src/**/*.py` 이면 그 모듈을 검사.
  위반은 exit 2 + stderr 로 에이전트에게 오류로 전달되고, 위반이 없으면 영향 범위와
  문서 stale 여부가 additionalContext 로 전달된다

## 문서

- `for-agent-layerinfo.md` (패키지 루트, 중첩 모듈 루트): 층별 모듈 목록. 마커 사이는 생성, 한 줄 설명과 마커 밖은 보존
- `for-agent-layerinfo-lN.md` (각 층): 공개 클래스 메서드 시그니처. 마커 사이는 생성
- `for-agent-moduleinfo.md` (각 모듈): 사람이 쓴다. `sources` 헤더의 hash 로 stale 판정만 한다
