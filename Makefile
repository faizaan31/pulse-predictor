SHELL := /bin/bash

init:
	cp .env.example .env

up:
	docker compose up --build

down:
	docker compose down -v

test:
	pytest -q
