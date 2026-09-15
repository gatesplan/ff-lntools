import requests

from shop.l0.candle import Candle


class Wallet:
    def value(self, candle: Candle) -> float:
        return candle.close
