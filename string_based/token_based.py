from .string_based import StringBased
import textdistance


class TokenBased(StringBased):
    def __init__(self, name, similarity_measures=None):
        super().__init__(name)
        if similarity_measures is None:
            similarity_measures = [
                "jaccard",
                "sorensen_dice",
                "tversky",
                "overlap",
                "cosine",
                "monge_elkan",
                "bag",
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
            "jaccard": self.calculate_jaccard_similarity,
            "sorensen_dice": self.calculate_sorensen_dice_similarity,
            "tversky": self.calculate_tversky_similarity,
            "overlap": self.calculate_overlap_similarity,
            "cosine": self.calculate_cosine_similarity,
            "monge_elkan": self.calculate_monge_elkan_similarity,
            "bag": self.calculate_bag_similarity,
        }

        if similarity_measure in similarity_methods:
            similarity = similarity_methods[similarity_measure](word1, word2)
            return similarity

        return None

    def calculate_jaccard_similarity(self, word1, word2):
        return textdistance.jaccard.normalized_similarity(word1, word2)

    def calculate_sorensen_dice_similarity(self, word1, word2):
        return textdistance.sorensen_dice.normalized_similarity(word1, word2)

    def calculate_tversky_similarity(self, word1, word2):
        return textdistance.tversky.normalized_similarity(word1, word2)

    def calculate_overlap_similarity(self, word1, word2):
        return textdistance.overlap.normalized_similarity(word1, word2)

    def calculate_cosine_similarity(self, word1, word2):
        return textdistance.cosine.normalized_similarity(word1, word2)

    def calculate_monge_elkan_similarity(self, word1, word2):
        return textdistance.monge_elkan.normalized_similarity(word1, word2)

    def calculate_bag_similarity(self, word1, word2):
        return textdistance.bag.normalized_similarity(word1, word2)
