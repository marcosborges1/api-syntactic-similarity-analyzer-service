from abc import ABC, abstractmethod
from .string_based import StringBased
import textdistance


class EditBased(StringBased):
    def hamming_distance(self, word1, word2):
        return textdistance.hamming.normalized_similarity(word1, word2)

    def mlipns_distance(self, word1, word2):
        return textdistance.mlipns.normalized_similarity(word1, word2)

    def levenshtein_distance(self, word1, word2):
        return textdistance.levenshtein.normalized_similarity(word1, word2)

    def damerau_levenshtein_distance(self, word1, word2):
        return textdistance.damerau_levenshtein.normalized_similarity(word1, word2)

    def jaro_winkler_similarity(self, word1, word2):
        return textdistance.jaro_winkler.normalized_similarity(word1, word2)

    def strcmp95_similarity(self, word1, word2):
        return textdistance.strcmp95.normalized_similarity(word1, word2)

    def needleman_wunsch_similarity(self, word1, word2):
        return textdistance.needleman_wunsch.normalized_similarity(word1, word2)

    def smith_waterman_similarity(self, word1, word2):
        return textdistance.smith_waterman.normalized_similarity(word1, word2)

    def analyze(self, word1, word2, methods):
        results = {}
        for method in methods:
            method_name = method.lower()
            if hasattr(self, method_name + "_distance"):
                similarity = getattr(self, method_name + "_distance")(word1, word2)
                results[method] = similarity
        return results
