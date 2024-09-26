name = ft_transcendence

.DEFAULT_GOAL = all

all:
	@printf "Launching ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml up -d --build

build:
	@printf "Building  ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml build

down:
	@printf "Stopping ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down

re: fclean
	@printf "Rebuilding  ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml up -d --build

clean: down
	@printf "Cleaning  ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down
	@docker container prune --force
	@docker image prune --force

fclean: down
	@printf "Clean of all docker configs\n"
	@docker compose -f ./srcs/docker-compose.yml down --volumes
	@docker image prune --all --force
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force
	@sudo rm -rf ~/data
 
.PHONY : all build down re clean fclean
