from typing import Annotated, NewType
from uuid import UUID
from fastapi import Query

import annotated_types as at


DocumentId = NewType("DocumentId", UUID)
LongStr = Annotated[str, at.Len(1, 32768)]
KnowledgeBaseName = Annotated[
    str, Query(min_length=3, max_length=50, regex="^[a-z0-9_]+$")
]
