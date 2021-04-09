# frontend-build: build frontend with yarn
FROM node:14-alpine as frontend-build
WORKDIR /build
COPY /frontend /build
RUN yarn && yarn run build

# poetry-build: export poetry deps to requirements.txt
# this is seperate from backend-build so that poetry deps don't end
# among the python modules that will be copied to the final image
FROM python:3.9.0-slim as poetry-build
RUN python -m pip install -U pip poetry
WORKDIR /build
COPY oas_core/pyproject.toml pyproject.toml
COPY oas_core/poetry.lock poetry.lock
RUN poetry export -f requirements.txt --without-hashes -o /build/requirements.txt

# backend-build: install all python deps from requirements.txt to /build/pip
FROM python:3.9.0-slim as backend-build
RUN apt-get update && apt-get install -q -y gcc
WORKDIR /build
COPY --from=poetry-build /build/requirements.txt .
RUN pip install --prefix="/build/pip" --no-warn-script-location -r requirements.txt

# python-base: base image with a few utilities installed
FROM python:3.9.0-slim as python-base
RUN apt-get update && apt-get install -q -y wget curl xz-utils iputils-ping iproute2

# ffmpeg-build: download ffmpeg-static
# (this adds only 73MB to the final image, vs 350MB for ffmpeg via apt)
FROM python-base as ffmpeg-build
WORKDIR /build
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz && \
  tar xf ffmpeg-release-amd64-static.tar.xz --strip-components=1

# build main image
FROM python-base
COPY --from=backend-build /build/pip/ /usr/local
COPY --from=ffmpeg-build /build/ffmpeg /usr/local/bin/ffmpeg
COPY --from=frontend-build /build/dist /app/frontend/dist
COPY /oas_core /app/oas_core
WORKDIR /app/oas_core
ENV STORAGE_PATH="/data"
CMD ["python", "server.py"]
