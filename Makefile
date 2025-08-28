.PHONY: build run stop logs test lint sbom

build:
	docker compose build --no-cache

run:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f --tail=200

test:
	pytest -q

lint:
	flake8 gateway services common || true

sbom:
	bash scripts/generate_sbom.sh
