from abc import abstractmethod
import pandas as pd
from IPython.display import display, HTML


class StringBased:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def analyze(self):
        pass

    def to_string(self, results):
        columns = ["word1", "word2"] + self.similarity_measures
        df = pd.DataFrame(results, columns=columns)
        print(df.to_string(index=False))

    def display_html(self, results):
        columns = ["word1", "word2"] + self.similarity_measures
        df = pd.DataFrame(results, columns=columns)
        display(HTML(df.to_html(index=False)))
