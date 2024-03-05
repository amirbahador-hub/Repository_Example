import strawberry
from .query import Query


schema = strawberry.Schema(Query)
