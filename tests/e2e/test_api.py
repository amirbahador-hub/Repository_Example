import pytest
import uuid
from ..random_refs import random_content, random_knowledge_base
from . import api_client


@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_add_knowledge_base():
    knowledge_base = random_knowledge_base()
    r= api_client.post_to_add_knowledge_base(knowledge_base)
    assert r.status_code == 201
    assert r.ok
    assert r.json() == knowledge_base
    
@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_202_and_remove_knowledge_base():
    knowledge_base = random_knowledge_base()
    r= api_client.post_to_add_knowledge_base(knowledge_base)
    assert r.ok
    assert r.json() == knowledge_base
    r= api_client.delete_to_remove_knowledge_base(knowledge_base)
    assert r.ok
    assert r.status_code == 202

@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_add_document():
    knowledge_base = random_knowledge_base()
    r= api_client.post_to_add_knowledge_base(knowledge_base)
    assert r.status_code == 201
    assert r.ok
    assert r.json() == knowledge_base
    r= api_client.post_to_add_document(knowledge_base,random_content())
    assert r.status_code == 201
    assert r.ok
    assert isinstance(uuid.UUID(r.json()), uuid.UUID)