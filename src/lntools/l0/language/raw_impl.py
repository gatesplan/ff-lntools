from dataclasses import dataclass


# 파일 하나에서 뽑은 덧붙이기 하나 (Rust 의 impl 블록). 아직 모듈로 해석되기 전 상태
# 대상 경로 규칙: 패키지명을 포함한 절대 점 경로. "" 는 이 파일 안 정의. None 은 패키지 밖(외부, 표준)이거나 제네릭 매개변수
@dataclass
class RawImpl:
    text: str                  # impl Display for Order 처럼 머리 한 줄
    line: int
    type_target: str | None    # 덧붙는 타입이 정의된 곳
    trait_target: str | None   # 구현하는 트레이트가 정의된 곳. 메서드 덧붙이기(inherent)면 None
    inherent: bool             # impl T { ... } 이면 True, impl Trait for T 이면 False
