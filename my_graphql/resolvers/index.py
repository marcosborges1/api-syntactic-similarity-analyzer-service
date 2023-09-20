import numpy
import pandas
import json
from scipy import stats
from IPython.display import display, HTML
from sklearn.metrics import (
    precision_score,
    recall_score,
    accuracy_score,
    confusion_matrix,
)
from mlxtend.plotting import plot_confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

import httpx


def default_columns(ranking=""):
    return [
        "oa_out_attr",
        "ta_in_attr",
        "oa_out_attr_dt",
        "ta_in_attr_dt",
        "oa_out_attr_parent",
        "ta_in_attr_parent",
        # "correct",
        "prediction",
        "gini",
        # "hamming","levenshtein","jaro_winkler","jaccard","sorensen","ratcliff_obershelp",
        ranking
    ]

def default_metrics(): 
    return [
        "hamming",
        "levenshtein",
        "jaro_winkler",
        "jaccard",
        "sorensen",
        "ratcliff_obershelp"
    ]

def precision_at_k(correct, y_score, k, pos_label=1):
    from sklearn.utils import column_or_1d
    from sklearn.utils.multiclass import type_of_target

    correct_type = type_of_target(correct)
    if not (correct_type == "binary"):
        raise ValueError("correct must be a binary column.")

    # Makes this compatible with various array types
    correct_arr = column_or_1d(correct)
    y_score_arr = column_or_1d(y_score)

    correct_arr = correct_arr == pos_label

    desc_sort_order = numpy.argsort(y_score_arr)[::-1]
    correct_sorted = correct_arr[desc_sort_order]
    y_score_sorted = y_score_arr[desc_sort_order]

    true_positives = correct_sorted[:k].sum()

    return true_positives / k


def load_dataset(path="../data/result.csv"):
    return pandas.read_csv(path, index_col=None, header=0, delimiter=",")


def load_dataset_by_api(path: str, api_o, api_t):
    dataset = load_dataset(path)

    return dataset[
        (dataset["origin_api"] == api_o) & (dataset["target_api"] == api_t)
    ]


def compute_average_rank(dataset, metrics:list()=default_metrics()):
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

# https://www.learnbymarketing.com/481/decision-tree-flavors-gini-info-gain/
# https://www.learndatasci.com/glossary/gini-impurity/
def compute_gini_rank(dataset, metrics:list()=default_metrics()):
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


def my_max(ranks):
    return max(ranks)


def compute_major_rank(dataset, metrics:list()=default_metrics()):
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


def do_show_top_ordered_by_rank(
    dataset, by_param=["avg_rank"], ascending_param=False, top=15
):
    
    # dataset = load_dataset()
    new_dataset = compute_average_rank(compute_gini_rank(compute_major_rank(dataset)))
    new_dataset = new_dataset[new_dataset["oa_out_attr_dt"] == new_dataset["ta_in_attr_dt"]]
    sorted_dataset = new_dataset.sort_values(
        by=by_param, ascending=ascending_param
    ).head(top)
    return sorted_dataset
    # print(display(HTML(sorted_dataset.to_html(columns=my_columns))))
    # print(display(HTML(sorted_dataset.to_html(columns=my_columns, max_rows=top))))

def do_show_top_ordered_best_metrics_by_rank(
    dataset, metrics:list=default_metrics(), by_param=["avg_rank"], ascending_param=False, top=15
):
    # dataset = load_dataset()
    new_dataset = compute_average_rank(compute_gini_rank(compute_major_rank(dataset, metrics),metrics),metrics)
    new_dataset = new_dataset[new_dataset["oa_out_attr_dt"] == new_dataset["ta_in_attr_dt"]]
    sorted_dataset = new_dataset.sort_values(
        by=by_param, ascending=ascending_param
    ).head(top)
    return sorted_dataset

def correct(y_array_correct, top):
    my_list = []
    for i in range(top):
        my_list.append(1 if i in y_array_correct else 0)
    return numpy.asarray(my_list)


def prediction(rank, threshold, ascending_param=False):
    if not ascending_param:
        return 1 if rank > threshold else 0
    else:
        return 1 if rank < threshold else 0


def common_data(top: int, columns: list, with_y=False):
    my_top = top
    my_columns = columns
    if with_y:
        my_columns.append("correct")
        my_columns.append("prediction")
    return (my_top, my_columns)


def common_info_api(api_o: str, api_t: str):
    title_each_rank = f"{api_o}->{api_t}"
    return api_o, api_t, title_each_rank

def recommend_items_from_dataset(dataset, metric: str, thereshold: float):
    return dataset[(dataset[metric].astype("float") > thereshold)]


def name_by_extense(metric):
    return f"({' '.join(metric.split('_')).capitalize()})"


def calculate_metrics(dataset):
    pre = precision_score(dataset["correct"], dataset["prediction"],zero_division=1)
    rec = recall_score(dataset["correct"], dataset["prediction"],zero_division=1)
    acc = accuracy_score(dataset["correct"], dataset["prediction"])
    return pre, rec, acc

def display_dataset(dataset, columns, title=""):
    display(HTML(f"<h3>{title}</h3> {dataset.to_html(columns=columns)}"))


def display_box_plot(dataset, title:str):
    # dataset = load_dataset()
    display(HTML(f"<b>{title} - Box Plot</b>"))
    dataset = compute_average_rank(compute_gini_rank(compute_major_rank(dataset)))
    metrics = [
        "hamming",
        "levenshtein",
        "jaro_winkler",
        "jaccard",
        "sorensen",
        "ratcliff_obershelp",
    ]
    boxplot = dataset.boxplot(column=metrics, rot=45)


def display_confusion_matrix(dataset, title:str, figsize: tuple = (3, 3)):
    display(HTML(f"<b>{title} - Confusion Matrix</b>"))
    y = numpy.flip(confusion_matrix(dataset["correct"], dataset["prediction"]))
    fig, ax = plot_confusion_matrix(
        conf_mat=y, show_absolute=True, show_normed=True, colorbar=True, figsize=figsize
    )
    plt.show()

def display_correlation(dataset, title:str):
    display(HTML(f"<b>{title} - Correlation</b>"))
    metrics = [
        "hamming",
        "levenshtein",
        "jaro_winkler",
        "jaccard",
        "sorensen",
        "ratcliff_obershelp",
    ]
    corr = dataset[metrics].corr()
    sns.heatmap(
        corr,
        xticklabels=corr.columns,
        yticklabels=corr.columns,
        annot=True,
        cmap="Blues",
    )
    plt.show()

def display_metrics(dataset, title:str):
    display(HTML(f"<b>{title} - Metrics</b>"))
    fig, ax = plt.subplots(facecolor=("#ffffff"))
    # dataset.reset_index(drop=True, inplace=True)
    # dataset.index = dataset.index + 1
    
    dataset["mean"] = dataset[
        [
            "hamming",
            "levenshtein",
            "jaro_winkler",
            "jaccard",
            "sorensen",
            "ratcliff_obershelp",
        ]
    ].mean(numeric_only=True, axis=1)
    # dataset["major"] = dataset[
    #     [
    #         "hamming",
    #         "levenshtein",
    #         "jaro_winkler",
    #         "jaccard",
    #         "sorensen",
    #         "ratcliff_obershelp",
    #     ]
    # ].max(numeric_only=True, axis=1)
    ax.plot(
        dataset.index, dataset["hamming"], color="#dedbd2", marker=".", label="hamming"
    )
    ax.plot(
        dataset.index,
        dataset["levenshtein"],
        color="#a2d2ff",
        marker=".",
        label="levenshtein",
    )
    ax.plot(
        dataset.index,
        dataset["jaro_winkler"],
        color="#f72585",
        marker=".",
        label="jaro_winkler",
    )
    ax.plot(
        dataset.index, dataset["jaccard"], color="#00bbf9", marker=".", label="jaccard"
    )
    ax.plot(
        dataset.index,
        dataset["sorensen"],
        color="#57cc99",
        marker=".",
        label="sorensen",
    )
    ax.plot(
        dataset.index,
        dataset["ratcliff_obershelp"],
        color="#9f86c0",
        marker=".",
        label="haratcliff_obershelpmming",
    )
    # if(title=="Avg Rank"):
    ax.plot(
        dataset.index,
        dataset["mean"],
        color="gray",
        marker=".",
        label="Mean",
        linestyle="--",
    )
    # elif(title=="Major Rank"):
    #     ax.plot(
    #         dataset.index,
    #         dataset["major"],
    #         color="red",
    #         marker=".",
    #         label="Major",
    #         linestyle="--",
    #     )
    ax.set_xticks(range(1,len(dataset)+1))
    y_ticks = numpy.arange(0, 1.1, 0.1)
    ax.set_yticks(y_ticks)

    ax.set_xlabel("Index")
    ax.set_ylabel("Values of String Similarity Algorithms")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.465, -0.15),
        fancybox=True,
        shadow=False,
        ncol=4,
        fontsize=8,
    )
    plt.show()


# def resolve_syntactic_similarities(data_url, metric, threshold, api_o, api_t, top):
# def resolve_generate_dataset(_, info, input_file_path):
def resolve_syntactic_similarities(_, info, path, ranking, threshold, k):
    """
    Resolves syntactic similarities based on the provided parameters.

    Parameters:
    - path (str): URL to load the dataset from
    - ranking (str): ranking name (e.g., "avg_rank")
    - threshold (float): Threshold value for predictions
    - top (int): Number of top items to show

    Returns:
    - json_array (str): JSON representation of the dataset_by_rank
    """
    
    # Load dataset
    dataset = load_dataset(path)

    # Process dataset
    dataset_by_rank = do_show_top_ordered_by_rank(
        dataset, by_param=[ranking], ascending_param=False, top=k
    )
    
    # Uncomment the line below if you decide to use the 'correct' method in the future
    # dataset_by_rank["correct"] = correct(my_y_true, top)
    
    # Add predictions to the dataset
    dataset_by_rank["prediction"] = dataset_by_rank.apply(
        lambda dt: prediction(dt[ranking], threshold), axis=1
    )

    dataset_by_rank = dataset_by_rank.drop(columns=['index'])

    # Convert the dataset to a JSON array
    result = dataset_by_rank.to_json(orient="records")

    data_for_graphql = json.loads(result)

    return data_for_graphql

# Usage example:
# result = resolve_syntactic_similarities(None,None, "http://localhost:4002/data/path_to_output.csv", "avg_rank", 0.4, 10)

async def resolve_api_intergration_points(_, info, apiList, ranking, threshold, k):
    
    ase_service_endpoint = "http://localhost:4001/"
    adg_service_endpoint = "http://localhost:4002/"

    async with httpx.AsyncClient() as client:
        # Call the first microservice
        response1 = await client.post(f"{ase_service_endpoint}graphql", json={
            "query": """
            query($apiList: [inputAPI]) {
                getExtractedApiList(apiList: $apiList) {
                    generatedExtractedFile
                }
            }
            """,
            "variables": {
                "apiList": apiList
            }
        })
        
        generatedExtractedFile = response1.json()["data"]["getExtractedApiList"]["generatedExtractedFile"]

        # Call the second microservice
        response2 = await client.post(f"{adg_service_endpoint}", json={
            "query": """
            query($generatedExtractedFile: String!) {
                generateDataset(generatedExtractedFile: $generatedExtractedFile) {
                    generatedDatasetFile
                }
            }
            """,
            "variables": {
                "generatedExtractedFile": generatedExtractedFile
            }
        })
        generatedDatasetFile = response2.json()["data"]["generateDataset"]["generatedDatasetFile"]

        return {

            "generatedExtractedFile": f"Available at: {generatedExtractedFile}" ,
            "generatedDatasetFile": f"Available at: {generatedDatasetFile}", 
            "syntactic":resolve_syntactic_similarities(_, info, generatedDatasetFile, ranking, threshold, k)

        }

