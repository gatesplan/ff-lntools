from shop.l1.order import Order
from shop.l2.report import Report
from shop.l3.portfolio.l0.tick_snapshot import TickSnapshot


class Store:
    def put(self, snap: TickSnapshot, order: Order) -> None:
        pass
