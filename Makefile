name = ft_transcendence
all:
	@printf "Launch configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml up -d

build:
	@printf "Building configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml up -d --build

down:
	@printf "Stopping configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml down

re:
	@printf "Rebuild configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml up -d --build

clean: down
	@printf "Cleaning configuration ${name}...\n"
	@docker system prune -a
	@sudo rm -rf data/*

fclean:
	@printf "Total clean of all configurations docker\n"
	@docker stop $$(docker ps -qa)
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force
	@sudo rm -rf ./data/*

.PHONY	: all build down re clean fclean