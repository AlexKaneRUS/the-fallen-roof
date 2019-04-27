class BaseMovementHandlerState:
    def __init__(self):
        pass

    def __call__(self, direction):
        return direction, self
