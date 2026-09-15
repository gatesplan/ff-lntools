class Candle:
    def __init__(self, open: float, close: float):
        self.open = open
        self.close = close

    def body(self) -> float:
        return self.close - self.open
