FROM node:lts AS frontend_build

env NEXT_TELEMETRY_DISABLED=1

WORKDIR /src

COPY frontend/package.json .
COPY frontend/package-lock.json .
RUN npm ci

COPY frontend/components components
COPY frontend/pages pages
COPY frontend/util util
#COPY frontend/next.config.js .
RUN npm run export && ls -Ahl /src/out

FROM python:3.9

WORKDIR /backend

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/firewatch_server firewatch_server
COPY backend/sample_conf.yaml /conf/firewatch.yaml

COPY --from=frontend_build /src/out/ /static/

ENV STATIC_DIR=/static CONF=/conf/firewatch.yaml

CMD ["python3", "-m", "firewatch_server"]
