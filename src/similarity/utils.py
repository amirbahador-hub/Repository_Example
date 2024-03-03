import re


def clean_name(name):
    return re.sub("[^a-z0-9-]+", "_", name.strip().lower())
