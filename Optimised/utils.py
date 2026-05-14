
import time


class CallCounter:
    def __init__(self):
        self._counts: dict[str, int] = {}

    def increment(self, method_name: str):
        self._counts[method_name] = self._counts.get(method_name, 0) + 1

    def total(self) -> int:
        return sum(self._counts.values())

    def report(self) -> dict:
        return dict(sorted(self._counts.items()))

    def reset(self):
        self._counts = {}


call_counter = CallCounter()


def log(component: str, message: str):
    ts = time.strftime("%H:%M:%S")
    print(f"  [{ts}]  {component:<25} ->  {message}")
