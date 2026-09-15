from typing import Protocol


class Notifier(Protocol):
    def send(self, to: str, message: str) -> None: ...
