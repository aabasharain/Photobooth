class CameraBackendError(ValueError):
    def __init__(self, backend: str) -> None:
        super().__init__(f"Unknown camera backend: {backend!r}")


class StateError(RuntimeError):
    def __init__(self, state: object) -> None:
        super().__init__(f"No handler for state {state}")
