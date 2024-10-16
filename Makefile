name = ft_transcendence

ENV_FILE = ./srcs/.env

SHELL := /bin/bash

.DEFAULT_GOAL = all

# Define variáveis para os diretórios dos certificados
CERT_DIR=./srcs/requirements/certs
CERT_KEY=$(CERT_DIR)/key.pem
CERT_CRT=$(CERT_DIR)/cert.pem

all:
	@printf "🔧 Launching ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="0"/' $(ENV_FILE)
	@docker compose -f ./srcs/docker-compose.yml up -d --build

info:
	@bash ./info.sh

env:
	@bash ./create_env.sh

sudoers:
	@echo -ne "✅ Checking Sudo... " && \
	if sudo -v; then \
		echo "OK!"; \
		if ! sudo grep -q "$(USER) ALL=(ALL:ALL) NOPASSWD: ALL" /etc/sudoers.d/$(USER)-permissions 2>/dev/null; then \
			echo "$(USER) ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/$(USER)-permissions > /dev/null; \
			echo "✅ Sudoers configuration added for $(USER)"; \
		else \
			echo "🟡 Sudoers configuration for $(USER) already exists."; \
		fi; \
	else \
		echo "🟡 Sudo check failed! Please ensure you have sudo privileges."; \
		exit 1; \
	fi

remove-sudoers:
	@if [ -f /etc/sudoers.d/$(USER)-permissions ]; then \
		sudo rm /etc/sudoers.d/$(USER)-permissions; \
		echo "✅ Removed sudoers configuration for $(USER)"; \
	else \
		echo "🟡 Sudoers configuration for $(USER) not present."; \
	fi;

setup: sudoers redisconf env certs

remove-setup: remove-redisconf
	@if [ -d srcs/requirements/certs ]; then \
		echo "🔧 Removing certs..."; \
		sudo rm -rf srcs/requirements/certs > /dev/null; \
		echo "✅ Certs removed successfully."; \
	else \
		echo "🟡 Certs not present."; \
	fi;

	@if [ -f srcs/.env ]; then \
		echo "🔧 Removing .env file..."; \
		sudo rm -rf srcs/.env > /dev/null; \
		echo "✅ .env file removed successfully."; \
	else \
		echo "🟡 .env file not present."; \
	fi;

	@$(MAKE) remove-sudoers > /dev/null || true

redisconf:
	@if ! grep -q "^vm.overcommit_memory = 1" /etc/sysctl.conf; then \
		echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf > /dev/null; \
		echo "✅ Memory Overcommit configuration added successfully."; \
	else \
		echo "🟡 Memory Overcommit configuration is already present in /etc/sysctl.conf"; \
	fi; \
	sudo sysctl -p > /dev/null 2>&1; \
	echo "✅ Memory Overcommit configured to allow always." > /dev/null

remove-redisconf:
	@if grep -q "^vm.overcommit_memory = 1" /etc/sysctl.conf; then \
		echo "🔧 Removing Memory Overcommit configuration from the host..."; \
		sudo sed -i '/^vm.overcommit_memory = 1/d' /etc/sysctl.conf; \
		sudo sysctl -p; \
		echo "✅ Memory Overcommit configuration removed."; \
	else \
		echo "🟡 Memory Overcommit configuration not present."; \
	fi;

certs:
	@if [ -f srcs/requirements/certs/cert.pem ] && [ -f srcs/requirements/certs/key.pem ]; then \
		echo "🟡 Certs already present."; \
	else \
		mkdir -p $(CERT_DIR) && \
		openssl req -x509 -newkey rsa:4096 -keyout $(CERT_KEY) -out $(CERT_CRT) -days 365 -nodes \
		-subj "/C=BR/ST=RJ/L=Rio/O=MyOrg/OU=IT/CN=localhost" 2>/dev/null; \
		echo "✅ SSL Certificates Generated at $(CERT_DIR)"; \
	fi;

service:
	@docker compose -f ./srcs/docker-compose.yml down --volumes --rmi local $(name) 
	@docker compose -f ./srcs/docker-compose.yml up -d --build $(name)

getin:
	@docker compose -f ./srcs/docker-compose.yml exec -it $(name) sh 

dev:
	@printf "🔧 Launching development ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="1"/' $(ENV_FILE)
	@docker compose -f ./srcs/docker-compose-dev.yml up --build

win:
	@printf "🔧 Launching development ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="1"/' $(ENV_FILE)
	@docker compose -f ./srcs/docker-compose-win.yml up --build
	
build:
	@printf "🔧 Building  ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml build

down:
	@printf "🔧 Stopping ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down

re: fclean
	@printf "🔧 Rebuilding  ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml up -d --build

clean: cleandev cleanwin
	@printf "🔧 Cleaning  ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down --volumes --rmi local
	@sudo rm -rf ~/data 

cleandev:
	@printf "🔧 Cleaning  ${name}...\n"
	@docker compose -f ./srcs/docker-compose-dev.yml down --volumes --rmi local
	@sudo rm -rf ~/data
	@sudo rm -rf ./srcs/app/transcendence/staticfiles

cleanwin:
	@printf "🔧 Cleaning  ${name}...\n"
	@docker compose -f ./srcs/docker-compose-win.yml down --volumes --rmi local
	@sudo rm -rf ~/data
	@sudo rm -rf ./srcs/app/transcendence/staticfiles

fclean: clean
	@printf "🔧 Cleaning of all ${name} configs\n"
	@docker compose -f ./srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
	@sudo rm -rf ~/data
 
deepclean: down
	@printf "🔧 Cleaning of all docker configs\n"
	@docker compose -f ./srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
	@sudo rm -rf ~/data
	@docker system prune --all

.PHONY : all build down re clean cleandev cleanwin fclean dev info sudoers remove-sudoers certs env win daph redisconf remove-redisconf setup remove-setup
