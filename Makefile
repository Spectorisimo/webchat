DC = docker compose
EXEC = docker exec -it
LOGS = docker logs

APP_LOCAL = deploy/docker-compose/app.yaml
STORAGES_LOCAL = deploy/docker-compose/storages.yaml
KAFKA_LOCAL = deploy/docker-compose/kafka.yaml

.PHONY: run-local
run-local:
	${DC} -f ${STORAGES_LOCAL} -f ${KAFKA_LOCAL} -f ${APP_LOCAL} up --build -d

.PHONY: check
check:
	cd backend && pre-commit run --all-files

.PHONY: test
test:
	${EXEC} chat-app pytest -s
