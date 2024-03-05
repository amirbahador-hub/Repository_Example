import requests
from lib.config import get_config


def post_to_add_knowledge_base(name):
    url = get_config("app_url")
    r = requests.post(
        f"{url}/knowledge_base", json={"name": name}
    )
    return r


def delete_to_remove_knowledge_base(name):
    url = get_config("app_url")
    r = requests.delete(
        f"{url}/knowledge_base", json={"name": name}
    )
    return r

def post_to_add_document(name, content):
    url = get_config("app_url")
    r = requests.post(
        f"{url}/knowledge_base/{name}/document", json={"content": content}
    )
    return r

def get_similarity(name, content):
    url = get_config("app_url")
    r = requests.get(
        f"{url}/knowledge_base/{name}/document/?q={content}"
    )
    return r


