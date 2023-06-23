from .string_based import StringBased
import textdistance


class SequenceBased(StringBased):
    def __init__(self, name):
        super().__init__(name)
        self.similarity_measures = ["lcsseq", "lcsstr", "ratcliff_obershelp"]

    def analyze(self, word_list):
        results = []
        for words in word_list:
            row = [words[0], words[1]]
            for measure in self.similarity_measures:
                similarity = self.calculate_similarity(words[0], words[1], measure)
                if similarity is not None:
                    similarity = round(similarity, 3)  # Round to three decimal places
                    row.append(similarity)
                else:
                    print(f"Unable to calculate similarity for measure: {measure}")
            results.append(row)
        return results

    def calculate_similarity(self, word1, word2, similarity_measure):
        similarity_methods = {
            "lcsseq": self.calculate_lcsseq_similarity,
            "lcsstr": self.calculate_lcsstr_similarity,
            "ratcliff_obershelp": self.calculate_ratcliff_obershelp_similarity,
        }

        if similarity_measure in similarity_methods:
            similarity = similarity_methods[similarity_measure](word1, word2)
            return similarity

        return None

    def calculate_lcsseq_similarity(self, word1, word2):
        return textdistance.lcsseq.normalized_similarity(word1, word2)

    def calculate_lcsstr_similarity(self, word1, word2):
        return textdistance.lcsstr.normalized_similarity(word1, word2)

    def calculate_ratcliff_obershelp_similarity(self, word1, word2):
        return textdistance.ratcliff_obershelp.normalized_similarity(word1, word2)
