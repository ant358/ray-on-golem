docker-build: ## Build the docker image
	docker build -t rog_3_10_edit .
docker-run: ## Run the docker image
	docker run  -it --name rog_1 -v "$(pwd)":/app rog_3_10_edit bash
docker-exec: ## Run the docker image
	docker exec -it rog_1 bash
docker-stop: ## Stop the docker image
	docker stop rog_1
docker-start: ## Start the docker image
	docker -i start rog_1