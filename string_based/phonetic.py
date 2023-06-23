from .string_based import StringBased
import textdistance


class PhoneticBased(StringBased):
    def __init__(self, name):
        super().__init__(name)
        self.similarity_measures = ["mra", "editex"]

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
            "mra": self.calculate_mra_similarity,
            "editex": self.calculate_editex_similarity,
        }

        if similarity_measure in similarity_methods:
            similarity = similarity_methods[similarity_measure](word1, word2)
            return similarity

        return None

    def calculate_mra_similarity(self, word1, word2):
        return textdistance.mra.normalized_similarity(word1, word2)

    def calculate_editex_similarity(self, word1, word2):
        return textdistance.editex.normalized_similarity(word1, word2)
