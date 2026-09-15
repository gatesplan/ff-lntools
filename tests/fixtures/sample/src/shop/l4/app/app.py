from shop.l1.email_notifier import EmailNotifier
from shop.l1.order import Order
from shop.l3.portfolio import Store


class App:
    def __init__(self):
        self.notifier = EmailNotifier()
        self.store = Store()
