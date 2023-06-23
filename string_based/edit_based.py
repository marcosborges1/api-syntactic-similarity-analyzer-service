from .string_based import StringBased
import textdistance


class EditBased(StringBased):
    def __init__(self, name, similarity_measures=None):
        super().__init__(name)
        if similarity_measures is None:
            similarity_measures = [
                "ham",
                "mli",
                "lev",
                "dam",
                "jar",
                "str",
                "nee",
                "smi",
            ]
        self.similarity_measures = similarity_measures

    # def to_string(self, results):
    #     columns = ["word1", "word2"] + self.similarity_measures
    #     df = pd.DataFrame(results, columns=columns)
    #     print(df.to_string(index=False))

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
            "ham": self.calculate_hamming_similarity,
            "mli": self.calculate_mlipns_similarity,
            "lev": self.calculate_levenshtein_similarity,
            "dam": self.calculate_damerau_levenshtein_similarity,
            "jar": self.calculate_jaro_winkler_similarity,
            "str": self.calculate_strcmp95_similarity,
            "nee": self.calculate_needleman_wunsch_similarity,
            "smi": self.calculate_smith_waterman_similarity,
        }

        if similarity_measure in similarity_methods:
            similarity = similarity_methods[similarity_measure](word1, word2)
            return similarity

        return None

    def calculate_hamming_similarity(self, word1, word2):
        return textdistance.hamming.normalized_similarity(word1, word2)

    def calculate_mlipns_similarity(self, word1, word2):
        return textdistance.mlipns.normalized_similarity(word1, word2)

    def calculate_levenshtein_similarity(self, word1, word2):
        return textdistance.levenshtein.normalized_similarity(word1, word2)

    def calculate_damerau_levenshtein_similarity(self, word1, word2):
        return textdistance.damerau_levenshtein.normalized_similarity(word1, word2)

    def calculate_jaro_winkler_similarity(self, word1, word2):
        return textdistance.jaro_winkler.normalized_similarity(word1, word2)

    def calculate_strcmp95_similarity(self, word1, word2):
        return textdistance.strcmp95.normalized_similarity(word1, word2)

    def calculate_needleman_wunsch_similarity(self, word1, word2):
        return textdistance.needleman_wunsch.normalized_similarity(word1, word2)

    def calculate_smith_waterman_similarity(self, word1, word2):
        return textdistance.smith_waterman.normalized_similarity(word1, word2)
