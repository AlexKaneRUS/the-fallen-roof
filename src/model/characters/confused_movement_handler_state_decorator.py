import random


class ConfusedMovementHandlerStateDecorator:
    def __init__(self, base, duration):
        self._base = base
        self._duration = duration

    def __call__(self, direction):
        direction, base = self._base(direction)
        if self._duration:
            return (
                direction.turn_clockwise(random.randint(-1, 1)),
                ConfusedMovementHandlerStateDecorator(base, self._duration - 1)
            )
        else:
            return direction, base
