from redis.asyncio import Redis as AsyncRedis
from redis.commands.json.path import Path
from similarity.domain.exceptions import InvalidKnowledgeBaseName
from similarity.domain.models import KnowledgeBase


class RedisRepository:
    def __init__(self, redis: AsyncRedis):
        self.redis = redis 

    async def add(self, knowledge_base: KnowledgeBase):
        await self.redis.json().set(f"knowledge_bases:{knowledge_base.name}", ".", [])
        return knowledge_base

    async def delete(self, name):
        members = await self._get_by_name(name)
        if not isinstance(members, list):
            raise InvalidKnowledgeBaseName("Knowledge Base Dosen't Exists")
        await self.redis.json().delete(f"knowledge_bases:{name}")
        return name

    async def _get_by_name(self, name: str):
        return await self.redis.json().get(f"knowledge_bases:{name}")