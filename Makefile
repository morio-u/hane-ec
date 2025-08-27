up:
	docker compose up -d --build

down:
	docker compose down $(if $(V),--volumes)

stop:
	docker compose stop

logs:
	docker compose logs -f web

bash:
	docker compose exec web bash

ps:
	docker compose ps