# build stage
FROM python:3.11 AS builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src
COPY tests/ /project/tests
COPY config/ /project/config

WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable


FROM python:3.11

ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs

COPY --from=builder /project/__pypackages__/3.11/bin/* /bin/
