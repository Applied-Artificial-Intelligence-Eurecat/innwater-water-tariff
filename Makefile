local:
	docker compose -f docker-compose-local.yml up --build -d

local-logs:
	docker compose -f docker-compose-local.yml logs -f

local-down:
	docker compose -f docker-compose-local.yml down