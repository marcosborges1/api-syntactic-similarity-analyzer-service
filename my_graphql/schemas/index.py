# my_graphql/schemas/index.py

type_defs = """
type Query {
  getDummyData(input_path: [String!]!): [DummyData!]!
}
type DummyData {
  origin_api: String,
  target_api: String,
  oa_out_attr: String,
  ta_in_attr: String,
  oa_out_attr_parent: String,
  ta_in_attr_parent: String,
  oa_url: String,
  oa_method: String,
  ta_url: String,
  ta_method: String,
  jaro_winkler: Float,
  hamming: Float,
  levenshtein: Float,
  jaccard: Float,
  sorensen: Float,
  ratcliff_obershelp: Float, 
}
"""
