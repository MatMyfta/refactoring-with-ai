# Makefile

# Image name and tag
IMAGE_NAME = refactoring_with_ai
IMAGE_TAG = latest
CONTAINER_IMAGE = $(IMAGE_NAME):$(IMAGE_TAG)

# Default project directory
PROJECT_DIR ?= your_project

.PHONY: help build test run run-prompts clean

help:
	@echo "Available targets:"
	@echo "  build         Build the Docker image."
	@echo "  test          Run all tests inside the container (TDD workflow)."
	@echo "  run           Run the main analysis application inside Docker."
	@echo "                - Generates analysis report: results.json"
	@echo "  run-prompts   Run the analysis and generate prompts inside Docker."
	@echo "                - Generates analysis report: results.json"
	@echo "                - Prints prompts to the console."
	@echo "  clean         Remove Python cache files."

build:
	@echo "➜ Building Docker image: $(CONTAINER_IMAGE)"
	docker build --no-cache -t $(CONTAINER_IMAGE) .
	@echo "✔ Docker image built successfully."

test: build
	@echo "➜ Running tests inside Docker container..."
	docker run --rm $(CONTAINER_IMAGE) python -m pytest --verbose tests/
	@echo "✔ Tests completed."

run: build
	@echo "➜ Running the analyzer inside Docker container..."
	mkdir -p $(PROJECT_DIR)/output
	docker run --rm \
		-v $(PWD)/$(PROJECT_DIR):/app/project \
		$(CONTAINER_IMAGE) \
		python -m src.main --project-path /app/project --output /app/project/output/results.json
	@echo "✔ Analysis complete. Report saved to $(PROJECT_DIR)/output/results.json"

run-prompts: build
	@echo "➜ Running the analyzer and generating prompts inside Docker container..."
	mkdir -p $(PROJECT_DIR)/output
	docker run --rm \
		-v $(PWD)/$(PROJECT_DIR):/app/project \
		$(CONTAINER_IMAGE) \
		python -m src.main --project-path /app/project --output /app/project/output/results.json --generate-prompts
	@echo "✔ Analysis complete. Report saved to $(PROJECT_DIR)/output/results.json"
	@echo "✔ Prompts have been generated and printed to the console."

clean:
	@echo "➜ Cleaning up Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✔ Cleanup done."
