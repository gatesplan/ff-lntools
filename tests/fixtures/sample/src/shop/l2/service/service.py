from shop.l0.notifier import Notifier


class Service:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def go(self) -> None:
        self.notifier.send('a', 'b')
