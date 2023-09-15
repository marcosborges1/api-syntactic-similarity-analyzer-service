# my_graphql/resolvers/index.py

# from utils import Utils
# from string_based import (
#     EditBased,
#     TokenBased,
#     SequenceBased,
#     CompressionBased,
#     PhoneticBased,
#     StringBased,
# )

# word_list = [
#     ["car", "cat"],
#     ["car", "autombile"],
#     ["apple", "orange"],
#     ["id", "badge"],
# ]


# edit_based = EditBased("EditBased")
# results = edit_based.analyze(word_list)
# edit_based.to_string(results)

# sb = EditBased("token")
# token_results = sb.analyze(word_list)
# sb.to_string(token_results)

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

import pandas as pd
import numpy, json


def default_metrics():
    return [
        "hamming",
        "levenshtein",
        "jaro_winkler",
        "jaccard",
        "sorensen",
        "ratcliff_obershelp",
    ]


def compute_average_rank(dataset, metrics: list() = default_metrics()):
    avg_ranks = []
    for index, row in dataset.iterrows():
        array_metrics = []
        for metric in metrics:
            array_metrics.append(row[metric])
        avg_ranks.append(
            numpy.average(
                # [
                #     row["hamming"],
                #     row["levenshtein"],
                #     row["jaro_winkler"],
                #     row["jaccard"],
                #     row["sorensen"],
                #     row["ratcliff_obershelp"],
                # ]
                array_metrics
            )
        )

    dataset["avg_rank"] = avg_ranks

    return dataset


def compute_major_rank(dataset, metrics: list() = default_metrics()):
    major_ranks = []
    for index, row in dataset.iterrows():
        array_metrics = []
        for metric in metrics:
            array_metrics.append(row[metric])
        major_ranks.append(
            numpy.max(
                # [
                #     row["hamming"],
                #     row["levenshtein"],
                #     row["jaro_winkler"],
                #     row["jaccard"],
                #     row["sorensen"],
                #     row["ratcliff_obershelp"],
                # ]
                array_metrics
            )
        )

    dataset["major_rank"] = major_ranks

    return dataset


def compute_gini_rank(dataset, metrics: list() = default_metrics()):
    gini_ranks = []
    all_ranks = numpy.array([])
    for index, row in dataset.iterrows():
        array_metrics = []
        for metric in metrics:
            array_metrics.append(row[metric])
        all_ranks = array_metrics

        # [
        #     row["hamming"],
        #     row["levenshtein"],
        #     row["jaro_winkler"],
        #     row["jaccard"],
        #     row["sorensen"],
        #     row["ratcliff_obershelp"],
        # ]
        length = len(all_ranks)
        all_ranks = numpy.power(numpy.divide(all_ranks, len(all_ranks)), 2.0)  # type: ignore
        # gini_ranks.append(1.0 - numpy.sum(all_ranks))
        gini_ranks.append(numpy.sum(all_ranks))

    dataset["gini"] = gini_ranks

    return dataset


def load_dataset(path):
    return pd.read_csv(path, index_col=None, header=0, delimiter=",")


def load_dataset_by_api(path: str, api_o, api_t):
    dataset = load_dataset(path)

    return dataset[
        (dataset["Origin API (OA)"] == api_o) & (dataset["Target API (TA)"] == api_t)
    ]


def do_show_top_ordered_by_rank(
    dataset, by_param=["avg_rank"], ascending_param=False, top=15
):
    # dataset = load_dataset()
    new_dataset = compute_average_rank(compute_gini_rank(compute_major_rank(dataset)))
    new_dataset = new_dataset[new_dataset["oa_out_attr"] == new_dataset["ta_in_attr"]]
    sorted_dataset = new_dataset.sort_values(
        by=by_param, ascending=ascending_param
    ).head(top)
    return sorted_dataset


# api_o, api_t, title_each_rank = common_info_api("CFQ v1.0", "NF Mirror v1.0")

# my_top, my_columns = common_data(10, default_columns(), with_y=True)
# dataset = load_dataset_by_api(
#     f"../data/cartesian_products_{identification}_fields.csv", api_o, api_t
# )


# dataset_by_rank["y_true"] = correct_y(my_y_true, my_top)
# dataset_by_rank["y_pred"] = dataset_by_rank.apply(
#     lambda dt: y_pred(dt[my_metric], my_threshold), axis=1
# )
# pre, rec, acc = calculate_metrics(dataset_by_rank)  # metrics

# selected_columns = dataset_by_rank[["sorensen", "jaro_winkler", "avg_rank"]]
# json_string = selected_columns.to_json(orient="records")

# # Parse the JSON string to a Python structure
# data_for_graphql = json.loads(json_string)

# print(data_for_graphql)

# print(dataset_by_rank[["gini", "avg_rank"]])

# df = pd.DataFrame(dummy_data)
# print(df)


async def resolve_get_dummy_data(_, info, input_path):
    dataset = await load_dataset(input_path)
    print(dataset)
    return []
    my_metric = "avg_rank"
    my_y_true = [2, 3, 4]
    my_threshold = 0.4
    my_top = 10
    # my_columns = default_columns(my_metric)
    my_columns = [
        "oa_out_attr",
        "ta_in_attr",
        "oa_out_attr_parent",
        "ta_out_attr_parent",
        "jaro_winkler",
        "sorensen",
        "ratcliff_obershelp",
    ]
    dataset_by_rank = do_show_top_ordered_by_rank(
        dataset, by_param=[my_metric], ascending_param=False, top=my_top
    )
    json_string = dataset_by_rank.to_json(orient="records")
    return json.loads(json_string)
