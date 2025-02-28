all: check 
	docker compose up -d --build

setup:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	. .venv/bin/activate && pip install -r requirements.txt

check:
	@docker info > /dev/null 2>&1 || { echo "Docker is not running. Please start Docker and try again."; exit 1; }

re: clean all

reset: check clean
	docker system prune -a -f

remove_volumes: check
	docker volume rm $$(docker volume ls -q)

clean: check
	@docker info > /dev/null 2>&1 || { echo "Docker is not running. Please start Docker and try again."; exit 1; }
	-docker stop $$(docker ps -a -q)
	-docker rm $$(docker ps -a -q)
	-docker rmi $$(docker images -q)
	-$(MAKE) remove_volumes
	-docker network rm $$(docker network ls -q)

.PHONY: all check re reset remove_volumes clean setup
