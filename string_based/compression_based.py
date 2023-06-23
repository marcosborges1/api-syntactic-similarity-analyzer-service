from .string_based import StringBased
import textdistance


class CompressionBased(StringBased):
    def __init__(self, name):
        super().__init__(name)
        self.similarity_measures = [
            #     "arith_ncd",
            #     "rle_ncd",
            "bwtrle_ncd",
            "sqrt_ncd",
            "entropy_ncd",
            "bz2_ncd",
            "lzma_ncd",
            "zlib_ncd",
        ]

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
            "arith_ncd": self.calculate_arith_ncd_similarity,
            "rle_ncd": self.calculate_rle_ncd_similarity,
            "bwtrle_ncd": self.calculate_bwtrle_ncd_similarity,
            "sqrt_ncd": self.calculate_sqrt_ncd_similarity,
            "entropy_ncd": self.calculate_entropy_ncd_similarity,
            "bz2_ncd": self.calculate_bz2_ncd_similarity,
            "lzma_ncd": self.calculate_lzma_ncd_similarity,
            "zlib_ncd": self.calculate_zlib_ncd_similarity,
        }

        if similarity_measure in similarity_methods:
            similarity = similarity_methods[similarity_measure](word1, word2)
            return similarity

        return None

    def calculate_arith_ncd_similarity(self, word1, word2):
        return textdistance.arith_ncd.normalized_similarity(word1, word2)

    def calculate_rle_ncd_similarity(self, word1, word2):
        return textdistance.rle_ncd.normalized_similarity(word1, word2)

    def calculate_bwtrle_ncd_similarity(self, word1, word2):
        return textdistance.bwtrle_ncd.normalized_similarity(word1, word2)

    def calculate_sqrt_ncd_similarity(self, word1, word2):
        return textdistance.sqrt_ncd.normalized_similarity(word1, word2)

    def calculate_entropy_ncd_similarity(self, word1, word2):
        return textdistance.entropy_ncd.normalized_similarity(word1, word2)

    def calculate_bz2_ncd_similarity(self, word1, word2):
        return textdistance.bz2_ncd.normalized_similarity(word1, word2)

    def calculate_lzma_ncd_similarity(self, word1, word2):
        return textdistance.lzma_ncd.normalized_similarity(word1, word2)

    def calculate_zlib_ncd_similarity(self, word1, word2):
        return textdistance.zlib_ncd.normalized_similarity(word1, word2)
