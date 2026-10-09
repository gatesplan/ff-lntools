from .....l1.order import Order
from .....l2.report import Report
from ...l0.tick_snapshot import TickSnapshot


class Store:
    def put(self, snap: TickSnapshot, order: Order) -> None:
        pass
