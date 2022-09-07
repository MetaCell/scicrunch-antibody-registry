ARG CLOUDHARNESS_BASE

FROM $CLOUDHARNESS_BASE

USER root

RUN pip install --upgrade pip
RUN pip install psycopg2-binary

WORKDIR /
COPY . .

CMD python3 ingest.py

