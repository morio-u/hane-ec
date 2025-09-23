DC = docker compose

up:
	$(DC) up -d

build:
	$(DC) build

down:
	$(DC) down

down-vol:
	$(DC) down --volumes

start:
	$(DC) start

stop:
	$(DC) stop

logs:
	$(DC) logs -f web

bash:
	$(DC) exec web bash

ps:
	$(DC) ps