# server.py
import os
import uvicorn
from dotenv import load_dotenv
from ariadne import QueryType
from ariadne.asgi import GraphQL
from my_graphql.schemas.index import type_defs
from my_graphql.resolvers.index import resolve_syntactic_similarities,resolve_api_intergration_points
from ariadne.contrib.federation import make_federated_schema

# Load dotenv
load_dotenv()
query = QueryType()
query.set_field("getSyntacticSimilarities", resolve_syntactic_similarities)
query.set_field("getAPIIntegrationPoints", resolve_api_intergration_points)

schema = make_federated_schema(type_defs, query)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    # uvicorn.run(app, host="localhost", port=int(os.getenv("PORT")))
    uvicorn.run("server:app", host="localhost", port=int(os.getenv('PORT')), reload=True)
