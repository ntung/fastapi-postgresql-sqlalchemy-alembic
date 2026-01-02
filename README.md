# Rest API with FastAPI, PostgreSQL, SQLAlchemy, and Alembic

## Overview
In [this tutorial](https://medium.com/codex/fastapi-crud-with-postgresql-using-sqlalchemy-and-alembic-fa9418fead71) we learn to create REST APIs with fastapi. We are going to use:
* `FastApi` for creating APIs
* `PostgreSQL` as a database
* `SQLAlchemy` as an ORM tool
* `Alembic` as a database migration tool

## Required libraries and packages
To follow this tutorial you need to install the following packages:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2 alembic pydantic python-dotenv
```

## Run
To run the FastAPI application, use the following command:
```bash
uvicorn src.main:app --port=8090 --reload
```
or using `start.sh` - the bash wrapper.