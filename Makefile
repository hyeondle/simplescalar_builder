COMPOSEYML = -f ./docker-compose.yml
COMPOSE = docker-compose $(COMPOSEYML)

.PHONY: all
all : set up run

.PHONY: up
up :
	@echo "Starting..."
	$(COMPOSE) up --build -d

.PHONY: down
down :
	@echo "Stopping..."
	$(COMPOSE) down

.PHONY: set
set :
	@echo "Setting up..."
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

.PHONY: run
run :
	@echo "Running..."
	python3 tester.py

.PHONY: help
help :
	@echo "Usage: make [command]"
	@echo ""
	@echo "WARNING: If you are using MacOS, you need to install qemu first."
	@echo "INSTALL COMMAND: brew qemu"
	@echo "WARNING: If you don't have python3, you need to install python3 and requests first."
	@echo "INSTALL COMMAND: brew install python3"
	@echo "INSTALL COMMAND: pip3 install requests"
	@echo ""
	@echo "Commands:"
	@echo "  up        Start the container"
	@echo "  down      Stop the container"
	@echo "  set       Set up the qemu"
	@echo "  run       Run the tester"
	@echo "  help      Show this help message"