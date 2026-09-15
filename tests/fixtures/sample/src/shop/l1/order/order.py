from shop.l0.candle import Candle


class Order:
    def __init__(self, symbol: str, qty: float):
        self.symbol = symbol
        self.qty = qty

    def fill(self, qty: float) -> None:
        self.qty -= qty

    def mark(self, candle: Candle) -> float:
        return candle.close * self.qty

    def _internal(self) -> None:
        pass
