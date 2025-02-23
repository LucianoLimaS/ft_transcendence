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
	@bash ./srcs/requirements/tools/info.sh

env:
	@bash ./srcs/requirements/tools/create_env.sh

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

setup: sudoers env certs docker

remove-setup: remove-certs remove-env remove-sudoers

sudoers:
	@echo -ne "✅ Checking sudo... " && sudo -v && echo -ne "OK!\n" || { \
		echo "🟡 Sudo check failed! Please ensure you have sudo privileges."; \
		exit 1; \
	}; \
	if ! sudo grep -q "$(USER) ALL=(ALL:ALL) NOPASSWD: ALL" /etc/sudoers.d/$(USER)-permissions 2>/dev/null; then \
		echo "$(USER) ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/$(USER)-permissions > /dev/null; \
		echo "✅ Sudoers configuration added for $(USER)"; \
	else \
		echo "🟡 Sudoers configuration for $(USER) already exists."; \
	fi;


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
		sudo apt-get install -y ca-certificates curl make gnupg lsb-release > /dev/null 2>&1; \
		sudo install -m 0755 -d /etc/apt/keyrings > /dev/null 2>&1; \
		DISTRO=$$(lsb_release -si); \
		if [ "$$DISTRO" = "Ubuntu" ] || [ "$$DISTRO" = "Linuxmint" ]; then \
			DOCKER_REPO="https://download.docker.com/linux/ubuntu"; \
			CODENAME=$$(lsb_release -c | awk '{print $$2}'); \
			if [ "$$CODENAME" = "xia" ]; then \
				CODENAME="jammy"; \
			fi; \
		elif [ "$$DISTRO" = "Debian" ]; then \
			DOCKER_REPO="https://download.docker.com/linux/debian"; \
			CODENAME=$$(lsb_release -c | awk '{print $$2}'); \
		else \
			echo "❌ Unsupported distribution: $$DISTRO"; \
			exit 1; \
		fi; \
		sudo mkdir -p /etc/apt/keyrings; \
		curl -fsSL $$DOCKER_REPO/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null 2>&1; \
		sudo chmod a+r /etc/apt/keyrings/docker.asc > /dev/null 2>&1; \
		echo "deb [arch=$$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] $$DOCKER_REPO $$CODENAME stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 2>&1; \
		sudo apt-get update > /dev/null 2>&1; \
		sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose > /dev/null 2>&1; \
		echo "🔧 Adding ${USER} to the Docker group..."; \
		sudo usermod -aG docker ${USER} > /dev/null 2>&1; \
		echo "✅ ${USER} has been added to the Docker group."; \
		echo "💀 The system will reboot in 10 seconds..."; \
		sleep 10; \
		sudo reboot; \
	else \
		echo "🟡 Docker is already installed."; \
	fi;

remove-docker:
	@echo "🔧 Checking if Docker is installed..."
	@if systemctl list-units --type=service --all | grep -q docker > /dev/null 2>&1; then \
		echo "🛑 Stopping Docker services..."; \
		sudo systemctl stop docker docker.socket containerd > /dev/null 2>&1 || true; \
	fi; \
	# Remove Docker packages (APT)  
	@if dpkg -l | grep -q docker; then \
		echo "🔧 Removing Docker packages..."; \
		sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-compose docker-compose-plugin docker-buildx-plugin > /dev/null 2>&1; \
	fi; \
	# Remove Snap package (if applicable)  
	@if command -v snap > /dev/null 2>&1 && snap list | grep -q docker; then \
		echo "🔧 Removing Docker from Snap..."; \
		sudo snap remove docker > /dev/null 2>&1; \
	fi; \
	# Clean up dependencies  
	@echo "🔧 Cleaning up leftover packages..."; \
	sudo apt-get autoremove -y > /dev/null 2>&1; \
	sudo apt-get autoclean > /dev/null 2>&1; \
	# Remove Docker files and directories  
	@echo "🔧 Removing Docker files..."; \
	sudo rm -rf /var/lib/docker > /dev/null 2>&1; \
	sudo rm -rf /var/lib/containerd > /dev/null 2>&1; \
	sudo rm -rf /etc/docker > /dev/null 2>&1; \
	sudo rm -rf $$HOME/.docker > /dev/null 2>&1; \
	sudo rm -f /etc/apt/sources.list.d/docker.list > /dev/null 2>&1; \
	sudo rm -f /etc/apt/keyrings/docker.asc > /dev/null 2>&1; \
	echo "✅ Docker has been completely removed from your system."

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
	@if [ ! -f srcs/.env ]; then \
		read -p "Do you want to run the setup? (y/N): " choice && \
		if [ "$$choice" = "y" ] || [ "$$choice" = "Y" ]; then \
			$(MAKE) --no-print-directory setup; \
		fi; \
	fi
	@echo -e "🔧 Launching production for ${name}..."
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="0"/' $(ENV_FILE)
	@sed -i 's/^WINDOWS=.*/WINDOWS="0"/' $(ENV_FILE)
	@docker compose -f ./docker-compose.yml --env-file ./srcs/.env up -d --build

build:
	@echo -e "🔧 Building ${name}..."
	@bash srcs/requirements/tools/make_db_dirs.sh
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		echo "🔧 Building development environment..."; \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env build; \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		echo "🔧 Building windows development environment..."; \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env build; \
	else \
		echo "🔧 Building production environment...\n"; \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env build; \
	fi

dev:
	@if [ ! -f srcs/.env ]; then \
		read -p "Do you want to run the setup? (y/N): " choice && \
		if [ "$$choice" = "y" ] || [ "$$choice" = "Y" ]; then \
			$(MAKE) --no-print-directory setup; \
		fi; \
	fi
	@echo -e "🔧 Launching development for ${name}..."
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="1"/' $(ENV_FILE)
	@sed -i 's/^WINDOWS=.*/WINDOWS="0"/' $(ENV_FILE)
	@docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env up --build

win:
	@if [ ! -f srcs/.env ]; then \
		read -p "Do you want to run the setup? (y/N): " choice && \
		if [ "$$choice" = "y" ] || [ "$$choice" = "Y" ]; then \
			$(MAKE) --no-print-directory setup; \
		fi; \
	fi
	@echo -e "🔧 Launching windows development for ${name}..."
	@bash srcs/requirements/tools/make_db_dirs.sh
	@sed -i 's/^DEBUG=.*/DEBUG="1"/' $(ENV_FILE)
	@sed -i 's/^WINDOWS=.*/WINDOWS="1"/' $(ENV_FILE)
	@docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env up --build

down:
	@echo -e "🔧 Stopping ${name}..."
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		echo "🔧 Stopping development environment..."; \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env down; \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		echo "🔧 Stopping windows development environment..."; \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env down; \
	else \
		echo "🔧 Stopping production environment..."; \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env down; \
	fi

# ======================
# Additional Docker Services
# ======================

service:
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env down --volumes --rmi local $(name); \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env up -d --build $(name); \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env down --volumes --rmi local $(name); \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env up -d --build $(name); \
	else \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env down --volumes --rmi local $(name); \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env up -d --build $(name); \
	fi

restart-service:
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env restart $(name); \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env restart $(name); \
	else \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env restart $(name); \
	fi

restart:
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env restart; \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env restart; \
	else \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env restart; \
	fi

getin:
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env exec -it $(name) sh; \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env exec -it $(name) sh; \
	else \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env exec -it $(name) sh; \
	fi

# ======================
# Cleaning
# ======================

clean:
	@echo -e "🔧 Cleaning ${name}..."
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		echo "🔧 Cleaning development environment..."; \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env down --volumes --rmi local; \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		echo "🔧 Cleaning windows development environment..."; \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env down --volumes --rmi local; \
	else \
		echo "🔧 Cleaning production environment..."; \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env down --volumes --rmi local; \
	fi
	@$(MAKE) --no-print-directory clean-host

fclean:
	@echo -e "🔧 Full cleaning of ${name}..."
	@if [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "0" ]; then \
		echo "🔧 Full cleaning of development environment..."; \
		docker compose -f ./docker-compose-dev.yml --env-file ./srcs/.env down --volumes --rmi all; \
	elif [ "$(shell grep ^DEBUG= ./srcs/.env | cut -d '=' -f2)" = "1" ] && [ "$(shell grep ^WINDOWS= ./srcs/.env | cut -d '=' -f2)" = "1" ]; then \
		echo "🔧 Full cleaning of windows development environment..."; \
		docker compose -f ./docker-compose-win.yml --env-file ./srcs/.env down --volumes --rmi all; \
	else \
		echo "🔧 Full cleaning of production environment..."; \
		docker compose -f ./docker-compose.yml --env-file ./srcs/.env down --volumes --rmi all; \
	fi
	@$(MAKE) --no-print-directory clean-host
	@$(MAKE) --no-print-directory remove-setup

deepclean: fclean
	@echo -e "\n💀 Removing all Docker configurations...\n"
	@docker system prune --all

clean-host: clean-dirs clean-migrations clean-staticfiles clean-logs

clean-dirs:
	@sudo rm -rf ~/data > /dev/null 2>&1

clean-migrations:
	@sudo find . -path '*/migrations/*.py' -not -name '__init__.py' -delete > /dev/null 2>&1

clean-staticfiles:
	@sudo rm -rf ./srcs/app/transcendence/staticfiles/ > /dev/null 2>&1

clean-logs:
	@sudo rm -rf ./srcs/app/transcendence/logs/

# ======================
# Auxiliary Commands
# ======================

re: fclean
	@echo -e "🔧 Rebuilding ${name}..."
	@bash srcs/requirements/tools/make_db_dirs.sh
	@docker compose -f ./docker-compose.yml --env-file ./srcs/.env up -d --build

.PHONY : all build down re clean fclean dev info sudoers remove-sudoers \
	certs env setup remove-setup docker remove-env \
	remove-certs clean-host clean-dirs clean-migrations clean-staticfiles
	restart-service restart win clean-logs