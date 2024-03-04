from strawberry.fastapi import GraphQLRouter

from .schema import schema

router = GraphQLRouter(
    schema
)