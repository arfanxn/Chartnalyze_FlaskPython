# Chartnalyze (Flask/Backend)

AI-powered market analysis meets financial education , all in one smart platform.

## Installation

Install all PIP dependencies

```sh
 pip install -r requirements.txt
```

Create environtment file from the `example.env` file

```sh
cp .env.example .env
```

Generate secret key, hash key, or JWT secret key into the `.env` file.

```sh
make generate-secret-key
```

Migrate up/down Chartnalyze's required tables

```sh
make db-upgrade # to migrate up
# or
make db-downgrade # to migrate down
```

## Running

Running the application

```
flask run
# or
flask run --debug --debug # run in debug mode
```

Running the application unit/feature test

```
# The documentation will be there soon...
```

## Docker

You can also deploy to docker container (Dockerizing/Containerizing)

```
# The documentation will be there soon...
```

## Routes

The application routes are documented in the `postman_collection.json` file.

```sh
head postman_collection.json # check the routes documentation
```

## License

MIT && Chartnalyze

**Open Source**
