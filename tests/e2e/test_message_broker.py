import pytest
from . import api_client, redis_client
from ..random_refs import random_content, random_knowledge_base
import json
import uuid
from tenacity import Retrying, stop_after_delay


@pytest.mark.usefixtures("restart_api")
@pytest.mark.usefixtures("restart_redis_pubsub")
def test_happy_path_returns_200_and_get_similarity():
    knowledge_base = random_knowledge_base()
    content = random_content()
    r= api_client.post_to_add_knowledge_base(knowledge_base)
    assert r.status_code == 201
    assert r.ok
    assert r.json() == knowledge_base
    r= api_client.post_to_add_document(knowledge_base,content)
    subscription = redis_client.subscribe_to("document.*")

    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
        r= api_client.post_to_add_document(knowledge_base,content)
        with attempt:
            message = subscription.get_message(timeout=1)
            if message:
                messages.append(message)
                print(messages)
            data = json.loads(messages[-1]["data"])
            assert data["content"] == content
            assert data["name"] == knowledge_base 

    assert r.status_code == 201
    assert r.ok
    assert isinstance(uuid.UUID(r.json()), uuid.UUID)

