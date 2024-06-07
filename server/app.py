from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from src.graphql.query import Query
from src.graphql.mutation import Mutation
from strawberry.asgi import GraphQL

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return "Hello World"

strawberry_app = GraphQL(schema=strawberry.Schema(query=Query,mutation=Mutation), debug=True)

app.add_route('/graphql',strawberry_app)