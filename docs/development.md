# Development setup

Follow everything in [./install.md](install.md)

Create a `.env` file with a suitable config.


## Start Open Audio Search Demo

Build and start frontend:
```
cd frontend
yarn
yarn build
yarn start
```

Start server:
```
cd oas_core
python server.py
```

Start worker:
```
cd oas_core
python worker.py
```

Open demo in browser at [http://localhost:8080/ui/index.html](http://localhost:8080/ui/index.html)


## App Development

### Development mode

The server can be reloaded automatically when application code changes. You can enable it by setting the `oas_dev` env config, or starting the server with `OAS_DEV=1 server.py`.

### Frontend development

#### Requirements

You need Node.js and npm or yarn. yarn is recommended because it's much faster.

On Debian based systems use the following to install both Node.js and yarn:
```bash
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn nodejs
```

#### Development

For development `webpack-dev-server` is included. In this folder, run `yarn` to install all dependencies and then `yarn start` to start the live-reloading development server. Then open the UI at [http://localhost:4000](http://localhost:4000). In development mode, the UI expects a running oas_core server at `http://localhost:8080`.

#### Deployment

Make sure to run `yarn build` in this directory after pulling in changes. The `oas_core` server serves the UI at `/ui` from the `dist/` folder in this directory. 


### Inspect the Redis databaes

[`redis-commander`](https://www.npmjs.com/package/redis-commander) is a useful tool to inspect the Redis database. 

```bash
# install redis-commander
yarn global add redis
# or: npm install -g redis

# start redis-commander
redis-commander
```

Now, open your browser at [http://localhost:8081/](http://localhost:8081/)


### ASR Evaluation

Start worker:  
```
cd oas_core
python worker.py
```

Run transcription using ASR engine in another Terminal:
```
cd oas_core
(Optional, download models) python task-run.py download_models
python task-run.py asr --engine ENGINE [--language LANGUAGE] --file_path FILE_PATH [--help]
(e.g). python task-run.py asr --engine vosk --file_path ../examples/frn-leipzig.wav
```
