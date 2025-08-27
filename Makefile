up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f web

bash:
	docker compose exec web bash

ps:
	docker compose ps