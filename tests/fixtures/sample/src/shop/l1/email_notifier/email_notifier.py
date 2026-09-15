import smtplib

from shop.l0.notifier import Notifier


class EmailNotifier(Notifier):
    def send(self, to: str, message: str) -> None:
        pass
