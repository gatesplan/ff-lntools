from shop.l0.candle import Candle


class TickSnapshot:
    def __init__(self, candle: Candle):
        self.candle = candle
