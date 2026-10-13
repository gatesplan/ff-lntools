from dataclasses import dataclass


# 공개 시그니처가 쓰는 타입 하나와 그 타입이 정의된 곳. 아직 모듈로 해석되기 전 상태
@dataclass(frozen=True)
class RawTypeRef:
    owner: str             # 그 시그니처의 공개 이름. 다시 내보낸 이름이면 바깥에 드러나는 이름
    name: str              # 정의에 쓰인 원래 이름. 별칭으로 들였어도 원래 이름이다
    target: str            # 이름이 있는 곳. 패키지명을 포함한 절대 점 경로 (shop.l1.order, crate.l1)
    is_owner: bool = False # 이 타입이 owner 자신이다. owner 의 정의, 다시 내보낸 원래 정의, 경로 하나로 된 타입 별칭의 값
