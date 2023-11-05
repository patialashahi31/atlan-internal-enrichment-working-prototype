build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

start: build up

stop:
	docker-compose stop

clean: down
	docker-compose rm -f

