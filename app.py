from string_based import TokenBased

word_list = [["car", "cat"], ["car", "autombile"], ["apple", "orange"], ["id", "badge"]]

# edit_based = EditBased("EditBased")
# results = edit_based.analyze(word_list)
# print(edit_based.to_string(results))

edit_based = TokenBased("token")
results = edit_based.analyze(word_list)
print(edit_based.to_string(results))
