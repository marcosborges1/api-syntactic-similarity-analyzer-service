from string_based import EditBased

word_list = [["car", "cat"], ["car", "autombile"], ["apple", "orange"], ["id", "badge"]]

edit_based = EditBased("EditBased")
results = edit_based.analyze(word_list)
print(edit_based.to_string(results))
