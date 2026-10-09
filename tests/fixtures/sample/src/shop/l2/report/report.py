from __future__ import annotations
from typing import TYPE_CHECKING

from ...l1 import Order

if TYPE_CHECKING:
    from ...l1.wallet import Wallet


class Report:
    def run(self, order: Order, wallet: Wallet) -> str:
        return order.symbol
