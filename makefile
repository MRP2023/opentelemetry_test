up-zipkin:
	docker-compose up -d --remove-orphans

down-zipkin:
	docker-compose down

build:
	mkdir -p ../opentelemetry_test/zipkin_log_db
	docker-compose build

setup-storage:
	docker volume create zipkin_data

remove-storage:
	docker volume rm zipkin_data

.PHONY: deploy-zipkin undeploy-zipkin setup-storage remove-storage
