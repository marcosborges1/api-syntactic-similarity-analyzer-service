# server.py
import os
import uvicorn
from dotenv import load_dotenv
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from my_graphql.schemas.index import type_defs
from my_graphql.resolvers.index import resolve_syntactic_similarities

# Load dotenv
load_dotenv()
query = QueryType()
query.set_field("getSyntacticSimilarities", resolve_syntactic_similarities)

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=os.getenv("PORT"))
