from abc import abstractmethod
import pandas as pd
from IPython.display import display, HTML


class StringBased:
    def __init__(self, name):
        self.name = name

    def analyze(self, word_list):
        raise NotImplementedError(
            "additional_processing must be overridden in subclasses"
        )

    def get_dataframe(self, results):
        columns = ["word1", "word2"] + self.similarity_measures
        df = pd.DataFrame(results, columns=columns)
        return df

    def to_string(self, results):
        df = self.get_dataframe(results)
        print(df.to_string(index=False))

    def display_html(self, results):
        df = self.get_dataframe(results)
        display(HTML(df.to_html(index=False)))
