IMAGE_NAME=url_lal_app
COMMON_DOCKER_OPTIONS=--env-file .env \
		-v $(PWD)/app:/app/src \


.PHONY=build run inter check_env_file

check_env_file:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found!"; \
		exit 1; \
	fi
	@if ! grep -q "PGPASS=" .env; then \
		echo "Error: PGPASS not found in .env file!"; \
		exit 1; \
	fi
	@if ! grep -q "USER=" .env; then \
		echo "Error: USER not found in .env file!"; \
		exit 1; \
	fi

build: 
	docker build . -t $(IMAGE_NAME)

run: check_env_file build
	docker run -p 8501:8501 \
		$(COMMON_DOCKER_OPTIONS) \
		$(IMAGE_NAME)

inter: check_env_file build
	docker run -it \
		$(COMMON_DOCKER_OPTIONS) \
		$(IMAGE_NAME) \
		/bin/bash

