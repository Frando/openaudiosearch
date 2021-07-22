<h1 align="center">Open Audio Search</h1>
<div align="center">
 <strong>
    A full text search engine with automatic speech recognition for podcasts
  </strong>
</div>

<br />

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Docs: Rust](https://img.shields.io/badge/Docs-Rust-blue.svg)](https://openaudiosearch.github.io/openaudiosearch/doc/oas_core/)


## What is it?

**Open Audio Search** uses automatic speech recognition to extract text from audio, which is then indexed in a search engine to enable recommendation of similiar broadcasts to users.  
With **Open Audio Search**, we want to make the archives of community media, radio stations, podcasts searchable and discoverable, through open source tech and APIs.


## Main Features

* *Core backend* written in [Rust](https://rust-lang.org), providing a REST API and managing the indexing pipeline
* *Document database* using [CouchDB](https://couchdb.apache.org/)
* *Full-text search* using [Elasticsearch Community Edition](https://www.elastic.co/downloads/elasticsearch-oss)
* *Web user interface* using [React](https://reactjs.org/)
* *Task queue* with tasks written in [Python](https://python.org) (using [Celery](https://docs.celeryproject.org/) and [Redis](https://redis.io/))
* *Automatic Speech Recognition* using [Vosk toolkit](https://alphacephei.com/vosk/) ([Kaldi](http://kaldi-asr.org/) under the hood)


## Install & run with Docker

This project includes a Dockerfile to build a docker image for the backend and worker. It also includes a `docker-compose.yml` file to easily launch OAS together with Elastic Search and Redis.

To get started, install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/). You'll need a quite recent version of both.

Then, run the following commands:
```sh
git clone https://github.com/arso-project/open-audio-search
cd open-audio-search
docker-compose build
docker-compose up
```

It takes a little while for Elastic to start up. Then, the OAS user interface and API are available at [`http://localhost:8080`](http://localhost:8080).

For the speech recognition to work, you'll need to download the models. Run this command once, it will download the models into the `./data/oas` volume:
```sh
docker-compose exec backend python download_models.py
```

Elastic Search wants quite a lot of free disc space. If the threshold is not met, it refuses to do anything. Run the script at `oas_worker/scripts/elastic-disable-threshold.sh` to disable the disc threshold (does not persist across Elastic restarts):
``` sh
docker-compose exec backend bash scripts/elastic-disable-threshold.sh
```

## Run locally for developing

To run OAS locally for developing or testing you should install the following requirements beforehand:
- For the core: [Rust](https://rust-lang.org), which is most easily installed with [Rustup](https://rustup.rs/).
- For the worker: [Python 3](https://python.org) and [poetry](https://python-poetry.org/docs/). Also requires [ffmpeg](https://www.ffmpeg.org/).
- For the frontend: [Node.js](https://nodejs.org/en/) and npm or yarn

*Clone this repository*
```sh
git clone https://github.com/openaudiosearch/openaudiosearch
```

*Start CouchDB, Elastisearch and Redis via Docker*
```sh
docker-compose -f docker-compose.dev.yml up
```

*Build an run the core*
```sh
cargo run -- run
```

*Run the frontend in development mode* 
```sh
cd frontend
yarn
yarn start
```

*Run the worker*
```sh
cd oas_worker
poetry install
./start-worker.sh
```

The live-reloading UI development server serves the UI at [http://localhost:4000](http://localhost:4000).
The OAS API is served at [http://localhost:8080](http://localhost:8080/). 
REST API docs are automatically generated and served at [http://localhost:8080/swagger-ui](http://localhost:8080/swagger-ui)

### Development tips and tricks

Have a look at the [development guide](./docs/development.md).

## Configuration

*TODO: This is partly outdated and needs to be updated. The `oas` CLI help list supported options and their corresponding environment variables*

OAS is configured through environment variables. ~~If a `.env` file is present in the directory from which oas_worker is started the variables from there will be used. To customize the configuration, copy [`.env.default`](`oas_worker/.env.default`) in the `oas_worker` folder to `.env` and adjust the values.~~

|variable|default|description|
|-|-|-|
|`STORAGE_PATH`|`./data/oas`|Storage path for models, cached files and other assets|
|`FRONTEND_PATH`|`./frontend/dist`|Path to the built frontend that will be served at `/`|
|`HOST`|`0.0.0.0`|Interface for the HTTP server to bind to|
|`PORT`|`8080`|Port for HTTP server to listen on|
|`REDIS_URL`|`redis://localhost:6379/0`|URL to Redis server|
|`ELASTIC_URL`|`http://localhost:9200/`|URL to Elastic server (trailing slash is required)|
|`ELASTIC_INDEX`|`oas`|Name of the Elastic Search index to be created and used|
|`OAS_DEV`||If set to `1`: Enable development mode (see [Development guide](./docs/development.md)|


## License
[AGPL v3](LICENSE)


## Documentation
The official documentation is hosted on tbd.


## Discussion and Development
Most development discussions take place on github in this repo. Further, tbd.


## Contributing to Open Audio Search

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Code of conduct, tbd.
