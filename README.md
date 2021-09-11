# Instructions

This part of the interview process allows us to learn more about your software engineering and web development skills. Below is a description of a CRUD API that manages products, keeps track of their pricing and their view counts. You are given a boilerplate application with parts that are incomplete or not working as expected. The task is to add features to the application, adapt some parts of it and come prepared at the next interview with suggestions on how to improve it.

The boilerplate application has some basic components set up: a Product model with a database connection and some functionality in the controllers. We would like you to do the following:

- Add an API to get a single product
- Add an API to delete a single product
- Finish the implementation for fetching the currency conversion

When a single product is requested, all fields of that product are returned and the view-count for that product is incremented. The request can optionally specify a currency, in which case the price should be converted to the requested currency before being returned. We need to support the following currencies:

- USD (default)
- CAD
- EUR
- GBP

The latest exchange rates are retrieved from the public API https://currencylayer.com/. Tests are optional but we would like to hear from you how would you design such tests at the interview.

Files to work on:

- [Products API](src/manage_products/api/products.py)
- [Products Service](src/manage_products/services/product.py)
- [Currency Service](src/manage_products/services/currency.py)

## How to Run

Within the `src` directory, you'll find a `Makefile` which will allow you to build and run this application locally.

```sh
λ  pwd
interview-boilerplate-python/src

λ  make
build                build docker image
create-db            create database from sql script
fresh-build          build docker image without any cache
help                 Show this help
run                  run app via docker
```

Please create the database via `make create-db` command before getting started.
