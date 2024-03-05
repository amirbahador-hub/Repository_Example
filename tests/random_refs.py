import uuid
from similarity.utils import clean_name


def random_suffix():
    return uuid.uuid4().hex[:6]

def random_knowledge_base(name=""):
    return clean_name(f"kb_{name}_{random_suffix()}")

def random_content(name=""):
    return clean_name(f"kb_{name}_{random_suffix()}")*10

