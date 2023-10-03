# API Syntactic Similarity Analyzer (ASSA)

## Overview

ASSA is a pivotal component of the `Agape ` approach that deeply analyzes datasets from [API Dataset Generator (ASSA)](https://github.com/marcosborges1/api-dataset-generator-service). ASSA stands as the centerpiece of the Agape approach, meticulously analyzing datasets produced by ADG. It yields a comprehensive spectrum of outputs including similarity metrics, associated rankings, auxiliary calculations, and evaluations, see Figure below.

<img src="/images/assa_dataset.png" height="300"/>

Detailed descriptions of those outputs follow below.

### Similarity metrics - String Similarity Algorithms

- **Hamming**: this method calculates distance by overlapping two strings of the same size and identifying the positions where they differ.

- **Levensthein**: measures distance by determining the transformations needed to convert one string to another, using operations such as character insertion, deletion, and replacement.

- **Jaro_Winkler**: utilizes a prefix scale, awarding higher scores to strings that have matching characters within a specified distance and in the same sequence. The more characters that match from the beginning, the higher the resulting index.

- **Jaccard**: a statistical approach that evaluates both the similarity and diversity between two defined sets.

- **Sorensen**: quantifies the similarity between two sets of tokens.

- **Ratcliff-Obershelp**: computes similarity based on 2 times the number of intersecting tokens, divided by the total length of both tokens.

### Associated Rankings

There are two key associated rankings:

1. **avg_rank**: Derived from the mean of the metrics from the string similarity algorithms.
2. **major_rank**: Constituted by the maximum index of the similarity algorithm for a given tuple in the dataset.

### Auxiliary Calculation

- **Gini Index**: Deployed to gauge the equality behavior of the majority of the similarity algorithms.

### Evaluations

1. **Prediction**: This binary recommendation system suggests integration point tuples, using values of `0` (Not Recommended) and `1` (Recommended). The threshold for prediction is determined by one of the ranking metrics, which can be fine-tuned based on the dataset.
2. **Correct**: These are the true values or templates. They can be inputted either before predictions, especially if the composition points are already known, or during predictions, where API experts evaluate the sensibility of each prediction.

The evaluations enable the calculation of:

- **Precision**
- **Accuracy**
- **Recall**

### Visualizations

ASSA supports the creation of visualization aids such as:

- Correlation Charts
- Boxplots

## Algorithm

The ASSA's core is based on the algorithm described below.

<img src="/images/assa_algorithm.png" height="300"/>

## Implementation Details

Constructed using Python, the ASSA service is a lightweight, dynamic, and web-compatible solution. The choice of language complements the ASSA algorithm's versatility and caters to the overarching requirements of the System of Systems context, as described within the Agape approach.

## Setup

Before running the application, make sure to install the required dependencies. You can install them using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

Before you start the ASSA, be sure to start it.

```bash
python server.py
```

Access the ASSA from the GraphQL endpoint:

```bash
http://localhost:4002/graphql
```

**Note**:

- The default PORT is _4002_, but can be change for your convenience.
- This project heavily relies on GraphQL, a powerful query language for APIs, and a server-side runtime for executing those queries with your existing data. If you're unfamiliar with GraphQL or wish to dive deeper, you can [learn more about GraphQL here](https://graphql.org/).

## References

- **Agape Approach**: As the Agape approach is being validated through conferences and journals, updates will be periodically provided here. Once the validation process concludes and findings are published, a direct link to the paper will be shared in this section for easy accessibility.

## Project Status

The ASSA, currently in the evolutionary phase, functions as a proof of concept. It is actively undergoing improvements and changes to refine its capabilities and more effectively meet new requirements.

## Author

**Marcos Borges**  
PhD Student at Federal University of Ceará, Brazil  
Email: [marcos.borges@alu.ufc.br](mailto:marcos.borges@alu.ufc.br)

## Contributing

Community-driven improvements are always welcome. If you're looking to contribute, feel free to raise pull requests. For more significant changes or additions, it's recommended to open an issue first for discussions.

## License

[MIT](https://choosealicense.com/licenses/mit/)
