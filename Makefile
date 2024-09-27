name = ft_transcendence

.DEFAULT_GOAL = all

all:
	@printf "Launching ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml up -d --build

dev:
	@printf "Launching development ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose-dev.yml up --build

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
	@docker compose -f ./srcs/docker-compose.yml down --volumes --rmi local
	@sudo rm -rf ~/data

fclean: down
	@printf "Clean of all docker configs\n"
	@docker compose -f ./srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
	@sudo rm -rf ~/data
 
.PHONY : all build down re clean fclean dev
