all:$object

SERVICE?=cookiecutter_fast_api
RELEASE?=$(shell poetry version -s)
BUILD?=$(shell (git rev-parse HEAD) | cut -c1-7)

POD?=$(shell docker ps -q -a)
IMAGES?=$(shell docker images -q)

build:
	docker-compose build --build-arg TAG=$(BUILD) $(SERVICE)

build_no_dev:
	docker-compose build --build-arg TAG=$(BUILD) NO_DEV="true" $(SERVICE)

dev:
	docker-compose up $(SERVICE)

kill:
	docker kill $(POD) || echo "docker kill $(POD)"

delete:
	docker kill $(POD) || echo "docker kill $(POD)"
	docker rm $(POD) || echo "docker rm $(POD)"

clean:
	docker kill $(POD) || echo "docker kill $(POD)"
	docker rm $(POD) || echo "docker rm $(POD)"
	docker rmi $(IMAGES)

exec:
	docker-compose exec $(SERVICE) bash

add:
	docker-compose exec $(SERVICE) poetry add $(package)

add_dev:
	docker-compose exec $(SERVICE) poetry add $(package) --dev

remove:
	docker-compose exec $(SERVICE) poetry remove $(package)

remove_dev:
	docker-compose exec $(SERVICE) poetry remove $(package) --dev

show:
	docker-compose exec $(SERVICE) poetry show --tree

update:
	docker-compose exec $(SERVICE) poetry update

db_new:
	docker-compose exec $(SERVICE) bash -c 'cd database && alembic revision --autogenerate -m "$(message)"'

db_head:
	docker-compose exec $(SERVICE) bash -c 'cd database && alembic upgrade head'

log:
	docker-compose logs $(SERVICE)

image-build:
	docker build -t $(DOCKER_TAG) -f Dockerfile --build-arg TAG=$(BUILD) --build-arg NO_DEV="true" .