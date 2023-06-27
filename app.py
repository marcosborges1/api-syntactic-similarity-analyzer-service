from utils import Utils
from string_based import (
    EditBased,
    TokenBased,
    SequenceBased,
    CompressionBased,
    PhoneticBased,
    StringBased,
)

word_list = [
    ["car", "cat"],
    ["car", "autombile"],
    ["apple", "orange"],
    ["id", "badge"],
]


# edit_based = EditBased("EditBased")
# results = edit_based.analyze(word_list)
# edit_based.to_string(results)

sb = EditBased("token")
token_results = sb.analyze(word_list)
sb.to_string(token_results)

# df1 = token_based.get_dataframe(token_results)

# edit_based = EditBased("edit")
# edit_results = edit_based.analyze(word_list)
# df2 = edit_based.get_dataframe(edit_results)


# List of DataFrames
# dataframes = [df1, df2]

# merged_pdf = Utils.merge_dataframes(
#     dataframes=dataframes, on_columns=["word1", "word2"]
# )
# print(merged_pdf)
