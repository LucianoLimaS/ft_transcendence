# ======================
# Project and Main Files
# ======================

name = ft_transcendence
ENV_FILE = ./srcs/.env
SHELL := /bin/bash
.DEFAULT_GOAL = all

# ======================
# Scripts
# ======================

info:
	@bash ./info.sh

env:
	@bash ./create_env.sh

# ======================
# Setup and Configurations
# ======================

setup: sudoers redisconf env certs

remove-setup: remove-redisconf
	@if [ -d srcs/requirements/certs ]; then \
		echo "🔧 Removing certificates..."; \
		sudo rm -rf srcs/requirements/certs > /dev/null; \
		echo "✅ Certificates removed successfully."; \
	else \
		echo "🟡 Certificates not present."; \
	fi;

	@if [ -f srcs/.env ]; then \
		echo "🔧 Removing .env file..."; \
		sudo rm -rf srcs/.env > /dev/null; \
		echo "✅ .env file removed successfully."; \
	else \
		echo "🟡 .env file not present."; \
	fi;

	@$(MAKE) remove-sudoers > /dev/null || true

sudoers:
	@echo -ne "✅ Checking sudo... " && \
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
		echo "✅ Sudoers configuration removed for $(USER)"; \
	else \
		echo "🟡 Sudoers configuration for $(USER) not present."; \
	fi;

redisconf:
	@if ! grep -q "^vm.overcommit_memory = 1" /etc/sysctl.conf; then \
		echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf > /dev/null; \
		echo "✅ Memory Overcommit configuration added successfully."; \
	else \
		echo "🟡 Memory Overcommit configuration is already present in /etc/sysctl.conf"; \
	fi; \
	sudo sysctl -p > /dev/null 2>&1; \
	echo "✅ Memory Overcommit configured." > /dev/null

remove-redisconf:
	@if grep -q "^vm.overcommit_memory = 1" /etc/sysctl.conf; then \
		echo "🔧 Removing Memory Overcommit configuration..."; \
		sudo sed -i '/^vm.overcommit_memory = 1/d' /etc/sysctl.conf; \
		sudo sysctl -p; \
		echo "✅ Memory Overcommit configuration removed."; \
	else \
		echo "🟡 Memory Overcommit configuration not present."; \
	fi;

# ======================
# SSL Certificates
# ======================

CERT_DIR=./srcs/requirements/certs
CERT_KEY=$(CERT_DIR)/key.pem
CERT_CRT=$(CERT_DIR)/cert.pem

certs:
	@if [ -f $(CERT_CRT) ] && [ -f $(CERT_KEY) ]; then \
		echo "🟡 Certificates already present."; \
	else \
		mkdir -p $(CERT_DIR) && \
		openssl req -x509 -newkey rsa:4096 -keyout $(CERT_KEY) -out $(CERT_CRT) -days 365 -nodes \
		-subj "/C=BR/ST=RJ/L=Rio/O=MyOrg/OU=IT/CN=localhost" 2>/dev/null; \
		echo "✅ SSL Certificates generated at $(CERT_DIR)"; \
	fi;

# ======================
# Docker Services
# ======================

all:
	@printf "🔧 Launching ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="0"/' $(ENV_FILE)
	@docker compose -f ./srcs/docker-compose.yml up -d --build

build:
	@printf "🔧 Building ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml build

dev:
	@printf "🔧 Launching development for ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="1"/' $(ENV_FILE)
	@docker compose -f ./srcs/docker-compose-dev.yml up --build

win:
	@printf "🔧 Launching development for Windows: ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="1"/' $(ENV_FILE)
	@docker compose -f ./srcs/docker-compose-win.yml up --build

down:
	@printf "🔧 Stopping ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down

# ======================
# Additional Docker Services
# ======================

service:
	@docker compose -f ./srcs/docker-compose.yml down --volumes --rmi local $(name) 
	@docker compose -f ./srcs/docker-compose.yml up -d --build $(name)

getin:
	@docker compose -f ./srcs/docker-compose.yml exec -it $(name) sh 

# ======================
# Cleaning
# ======================

clean: cleandev cleanwin
	@printf "🔧 Cleaning ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down --volumes --rmi local
	@sudo find . -path '*/migrations/*.py' -not -name '__init__.py' -delete
	@sudo rm -rf ~/data 

cleandev:
	@printf "🔧 Cleaning development for ${name}...\n"
	@docker compose -f ./srcs/docker-compose-dev.yml down --volumes --rmi local
	@sudo rm -rf ~/data
	@sudo find . -path '*/migrations/*.py' -not -name '__init__.py' -delete
	@sudo rm -rf ./srcs/app/transcendence/staticfiles

cleanwin:
	@printf "🔧 Cleaning Windows development for ${name}...\n"
	@docker compose -f ./srcs/docker-compose-win.yml down --volumes --rmi local
	@sudo rm -rf ~/data
	@sudo find . -path '*/migrations/*.py' -not -name '__init__.py' -delete
	@sudo rm -rf ./srcs/app/transcendence/staticfiles

fclean: clean
	@printf "🔧 Full cleaning of ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
	@sudo rm -rf ~/data
	@sudo find . -path '*/migrations/*.py' -not -name '__init__.py' -delete
	@sudo rm -rf ./srcs/app/transcendence/staticfiles

deepclean: down
	@docker compose -f ./srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
	@sudo rm -rf ~/data
	@sudo find . -path '*/migrations/*.py' -not -name '__init__.py' -delete
	@sudo rm -rf ./srcs/app/transcendence/staticfiles
	@printf "\n💀 Removing all Docker configurations...\n"
	@docker system prune --all

# ======================
# Auxiliary Commands
# ======================

re: fclean
	@printf "🔧 Rebuilding ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml up -d --build

.PHONY : all build down re clean cleandev cleanwin fclean dev info sudoers remove-sudoers certs env win redisconf remove-redisconf setup remove-setup
