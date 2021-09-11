name := "manage-products-service:1.0"

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## build docker image
	docker build --rm -t ${name} .

fresh-build: ## build docker image without any cache
	docker build --rm --no-cache -t ${name} .

run: ## run app via docker
	docker run -i -t --rm -p 8003:8003 ${name}

all: build run # build and run docker image

create-db: ## create database from sql script
	sqlite3 manage_products/products.db < manage_products/data/schema.sql

virtualenv: ## create virtual environment
	pipenv install

lint: ## format source
	pipenv run black manage_products

test: ## test source
	export PYTHONPATH='./':$(PYTHONPATH) ; \
	pipenv run pytest
