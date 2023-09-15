# server.py
import uvicorn
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from my_graphql.schemas.index import type_defs
from my_graphql.resolvers.index import resolve_get_dummy_data

query = QueryType()
query.set_field("getDummyData", resolve_get_dummy_data)

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=4003)
