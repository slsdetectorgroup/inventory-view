#Configuration
HOST := 127.0.0.1
PORT := 8000
INV_PATH := ../inventory/

# Find OS and ARCH to download the correct micromamba
OSNAME := $(shell uname -s)
ifeq (${OSNAME}, Linux)
	OS := linux
else ifeq (${OSNAME}, Darwin)
	OS := osx
endif
ARCH := $(shell uname -m)
ifeq (${ARCH}, x86_64)
	ARCH := 64
endif

export GIT_INVENTORY_PATH=${INV_PATH}

default: dev

.bin/micromamba: ## download micromamba
	mkdir -p .bin
	cp etc/.mambarc .bin/.mambarc
	curl -Ls https://micro.mamba.pm/api/micromamba/${OS}-${ARCH}/latest | tar -xvj --strip-components=1 -C .bin bin/micromamba

.bin/envs/inventory: .bin/micromamba ## create micromamba env
	.bin/micromamba --no-env -r ${PWD}/.bin create -f etc/environment.yml

clean: ## delete micromamba env
	rm -rf .bin/

dev: .bin/envs/inventory ## [DEFAULT] run server id development mode
	.bin/envs/inventory/bin/uvicorn main:app --port ${PORT} --reload --host ${HOST}

start: .bin/envs/auth ## start server in daemon mode
	.bin/envs/inventory/bin/gunicorn main:app --bind ${HOST}:${PORT} --worker-class uvicorn.workers.UvicornWorker --daemon

stop: ## stop server runnig in daemon mode
	etc/stop.sh ${PORT}

help: # from compiler explorer
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'