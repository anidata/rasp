class EngineError(Exception):
    def __init__(self, value):
        self.value = value
        return

    def __str__(self):
        return repr(self.value)


class MasterErrror(Exception):
    def __init__(self, value):
        self.value = value
        return

    def __str__(self):
        return repr(self.value)