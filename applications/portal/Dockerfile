ARG CLOUDHARNESS_DJANGO

FROM node:20 as frontend

ENV APP_DIR=/app

WORKDIR ${APP_DIR}
COPY frontend/package.json ${APP_DIR}
COPY frontend/yarn.lock ${APP_DIR}
RUN yarn install --frozen-lockfile --timeout 60000

COPY frontend ${APP_DIR}
RUN yarn build

#####

FROM $CLOUDHARNESS_DJANGO

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_DIR}
RUN mkdir -p ${APP_DIR}/static/www

COPY backend/requirements.txt ${APP_DIR}
RUN --mount=type=cache,target=/root/.cache python -m pip install --upgrade pip && pip install -r requirements.txt --prefer-binary

COPY backend/setup.py ${APP_DIR}
RUN python3 -m pip install -e .

COPY backend ${APP_DIR}
RUN python3 manage.py collectstatic --noinput

COPY --from=frontend /app/dist ${APP_DIR}/static/www
ENV DJANGO_SETTINGS_MODULE=portal.settings
ENTRYPOINT uvicorn --workers ${WORKERS} --host 0.0.0.0 --port ${PORT} main:app
