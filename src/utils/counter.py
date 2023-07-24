class Counter:
    def __init__(self, initial: int = 0):
        self._value = initial
        self._initial = initial

    def __str__(self):
        return str(self._value)

    def increment(self, num: int = 1) -> int:
        self._value += num
        return self._value

    def reset(self) -> int:
        self._value = self._initial
        return self._value

    def value(self) -> int:
        return self._value
