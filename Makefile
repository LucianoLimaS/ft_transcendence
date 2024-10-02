name = ft_transcendence

.DEFAULT_GOAL = all

# Define variáveis para os diretórios dos certificados
CERT_DIR=./srcs/requirements/certs
CERT_KEY=$(CERT_DIR)/key.pem
CERT_CRT=$(CERT_DIR)/cert.pem

all:
	@printf "Launching ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml up -d --build

info:
	@bash ./info.sh

sudoers:
	@sudo echo -ne "Checking Sudo... " || exit 1 && echo OK!
	@echo "$(USER) ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/$(USER)-permissions

remove_sudoers:
	@sudo rm /etc/sudoers.d/$(USER)-permissions
	@echo "Removed sudoers configuration for $(USER)"

certs:
	mkdir -p $(CERT_DIR)
	openssl req -x509 -newkey rsa:4096 -keyout $(CERT_KEY) -out $(CERT_CRT) -days 365 -nodes \
	-subj "/C=BR/ST=RJ/L=Rio/O=MyOrg/OU=IT/CN=localhost"
	echo "✅ SSL Certificates Generated at $(CERT_DIR)"

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
 
.PHONY : all build down re clean fclean dev info sudoers remove-sudoers certs
