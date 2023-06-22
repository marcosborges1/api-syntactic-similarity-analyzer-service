from abc import abstractmethod


class StringBased:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def analyze(self):
        pass
