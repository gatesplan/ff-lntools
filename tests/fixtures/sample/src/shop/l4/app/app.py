from ...l1.email_notifier import EmailNotifier
from ...l1.order import Order
from ...l3.portfolio import Store


class App:
    def __init__(self):
        self.notifier = EmailNotifier()
        self.store = Store()
