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
    postgresql-client nginx supervisor \
    && apt-get clean

WORKDIR ${APP_DIR}
RUN mkdir -p ${APP_DIR}/static/www

COPY backend/requirements.txt ${APP_DIR}
RUN --mount=type=cache,target=/root/.cache python -m pip install --upgrade pip && pip install -r requirements.txt --prefer-binary

COPY backend/setup.py ${APP_DIR}
RUN python3 -m pip install -e .

COPY backend ${APP_DIR}
RUN python3 manage.py collectstatic --noinput

COPY --from=frontend /app/dist ${APP_DIR}/www
ENV DJANGO_SETTINGS_MODULE=portal.settings
# COPY default nginx configuration
COPY deploy/resources/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 8000
COPY deploy/resources/supervisord.properties /etc/supervisor/conf.d/supervisord.properties

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.properties"]