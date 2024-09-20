name = ft_transcendence

containers = app \
			 db  \
			 db_admin \
			 grafana  \
			 promet   \
			 selenium \
			 minio

volumes = ${name}_app_vol \
		  ${name}_db_vol  \
		  ${name}_grafana_vol \
		  ${name}_promet_vol  \
		  ${name}_minio_vol

network = ${name}_net

all:
	@printf "Launching configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml up -d

build:
	@printf "Building configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml up -d --build

down:
	@printf "Stopping configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml down

re:
	@printf "Rebuilding configuration ${name}...\n"
	@docker compose -f ./docker-compose.yml up -d --build

clean: down
	@printf "Cleaning configuration ${name}...\n"
	@docker compose -p ${name} -f ./docker-compose.yml down --volumes --remove-orphans
	@imagens=$$(docker images -f "dangling=true" -q); \
		if [ -n "$$imagens" ]; then \
			docker rmi $$imagens; \
		fi;
	@sudo rm -rf ./data/*

fclean: down
	@printf "Total clean of project ${name}...\n"

	@for volume in ${volumes}; do \
	  if docker volume inspect $$volume > /dev/null 2>&1; then \
	    docker volume rm $$volume; \
	  fi; \
	done

	@if docker network inspect ${network} > /dev/null 2>&1; then \
	  docker network rm ${network}; \
	fi
	@docker volume prune -f
	@sudo rm -rf ./data/*


.PHONY: all build down re clean fclean
