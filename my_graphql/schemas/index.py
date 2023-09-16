# my_graphql/schemas/index.py

type_defs = """
type Query {
  getSyntacticSimilarities(path: String!, ranking:String!, threshold: Float!, k: Int!): [SyntacticSimilarities]
}
type SyntacticSimilarities {
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
  major_rank: Float, 
  gini: Float, 
  avg_rank: Float, 
  prediction: Float
}
"""



