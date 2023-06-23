from .string_based import StringBased
import textdistance


class EditBased(StringBased):
    def __init__(self, name, similarity_measures=None):
        super().__init__(name)
        if similarity_measures is None:
            similarity_measures = [
                "hamming",
                "mlipns",
                "levenshtein",
                "damerau_levenshtein",
                "jaro_winkler",
                "strcmp95",
                "needleman_wunsch",
                "gotoh",
                "smith_waterman",
            ]
        self.similarity_measures = similarity_measures

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
            "hamming": self.calculate_hamming_similarity,
            "mlipns": self.calculate_mlipns_similarity,
            "levenshtein": self.calculate_levenshtein_similarity,
            "damerau_levenshtein": self.calculate_damerau_levenshtein_similarity,
            "jaro_winkler": self.calculate_jaro_winkler_similarity,
            "strcmp95": self.calculate_strcmp95_similarity,
            "needleman_wunsch": self.calculate_needleman_wunsch_similarity,
            "gotoh": self.calculate_gotoh_similarity,
            "smith_waterman": self.calculate_smith_waterman_similarity,
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

    def calculate_gotoh_similarity(self, word1, word2):
        return textdistance.gotoh.normalized_similarity(word1, word2)

    def calculate_smith_waterman_similarity(self, word1, word2):
        return textdistance.smith_waterman.normalized_similarity(word1, word2)
