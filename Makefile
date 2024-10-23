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

remove-env:
	@if [ -f srcs/.env ]; then \
		echo "🔧 Removing .env file..."; \
		sudo rm -rf srcs/.env > /dev/null; \
		echo "✅ .env file removed successfully."; \
	else \
		echo "🟡 .env file not present."; \
	fi;

# ======================
# Setup and Configurations
# ======================

setup: sudoers redisconf env certs docker

remove-setup: remove-env remove-certs remove-redisconf remove-sudoers

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

docker:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "🟡 Docker is not installed. Installing..."; \
		sudo apt-get update > /dev/null 2>&1; \
		sudo apt-get install -y ca-certificates curl make > /dev/null 2>&1; \
		sudo install -m 0755 -d /etc/apt/keyrings > /dev/null 2>&1; \
		sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc > /dev/null 2>&1; \
		sudo chmod a+r /etc/apt/keyrings/docker.asc > /dev/null 2>&1; \
		echo "deb [arch=$$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $$(. /etc/os-release && echo "$$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 2>&1; \
		sudo apt-get update > /dev/null 2>&1; \
		sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin > /dev/null 2>&1; \
		echo "🔧 Adding ${USER} to the Docker group..."; \
		sudo usermod -aG docker ${USER} > /dev/null 2>&1; \
		echo "✅ ${USER} has been added to the Docker group."; \
		echo "💀 The system will reboot in 10 seconds..."; \
		sleep 10; \
		sudo reboot; \
	else \
		echo "🟡 Docker is already installed."; \
	fi;

redisconf:
	@if ! grep -q "^vm.overcommit_memory = 1" /etc/sysctl.conf; then \
		echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf > /dev/null; \
		sudo sysctl -p > /dev/null 2>&1; \
		echo "✅ Memory Overcommit configuration was added successfully."; \
	else \
		sudo sysctl -p > /dev/null 2>&1; \
		echo "🟡 Memory Overcommit configuration already exists in /etc/sysctl.conf"; \
	fi; \

remove-redisconf:
	@if grep -q "^vm.overcommit_memory = 1" /etc/sysctl.conf; then \
		echo "🔧 Removing Memory Overcommit configuration..."; \
		sudo sed -i '/^vm.overcommit_memory = 1/d' /etc/sysctl.conf > /dev/null 2>&1; \
		sudo sysctl -p > /dev/null 2>&1; \
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

remove-certs:
	@if [ -d srcs/requirements/certs ]; then \
		echo "🔧 Removing certificates..."; \
		sudo rm -rf srcs/requirements/certs > /dev/null; \
		echo "✅ Certificates removed successfully."; \
	else \
		echo "🟡 Certificates not present."; \
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
	@$(MAKE) clean-host

cleandev:
	@printf "🔧 Cleaning development for ${name}...\n"
	@docker compose -f ./srcs/docker-compose-dev.yml down --volumes --rmi local
	@$(MAKE) clean-host

cleanwin:
	@printf "🔧 Cleaning Windows development for ${name}...\n"
	@docker compose -f ./srcs/docker-compose-win.yml down --volumes --rmi local
	@$(MAKE) clean-host

fclean: clean
	@printf "🔧 Full cleaning of ${name}...\n"
	@docker compose -f ./srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
	@$(MAKE) clean-host
	
deepclean: down
	@docker compose -f ./srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
	@$(MAKE) clean-host
	@printf "\n💀 Removing all Docker configurations...\n"
	@docker system prune --all

clean-host: clean-dirs clean-migrations clean-staticfiles stop-redis

clean-dirs:
	@sudo rm -rf ~/data > /dev/null 2>&1

clean-migrations:
	@sudo find . -path '*/migrations/*.py' -not -name '__init__.py' -delete > /dev/null 2>&1

clean-staticfiles:
	@sudo rm -rf ./srcs/app/transcendence/staticfiles > /dev/null 2>&1

stop-redis:
	@sudo systemctl stop redis

# ======================
# Auxiliary Commands
# ======================

re: fclean
	@printf "🔧 Rebuilding ${name}...\n"
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./srcs/docker-compose.yml up -d --build

.PHONY : all build down re clean cleandev cleanwin fclean dev info sudoers remove-sudoers \
	certs env win redisconf remove-redisconf setup remove-setup docker remove-env \
	remove-certs clean-host clean-dirs clean-migrations clean-staticfiles stop-redis