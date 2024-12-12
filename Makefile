# Image name and tag
IMAGE_NAME = refactoring_with_ai
IMAGE_TAG = latest
CONTAINER_IMAGE = $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: help build test run clean

help:
	@echo "Available targets:"
	@echo "  build     Build the Docker image."
	@echo "  test      Run all tests inside the container (TDD workflow)."
	@echo "  run       Run the main analysis application inside the container."
	@echo "  clean     Remove Python cache files."

build:
	@echo "➜ Building Docker image: $(CONTAINER_IMAGE)"
	docker build -t $(CONTAINER_IMAGE) .
	@echo "✔ Docker image built successfully."

test: build
	@echo "➜ Running tests inside Docker container..."
	docker run --rm $(CONTAINER_IMAGE) pytest --verbose tests/
	@echo "✔ Tests completed."

run: build
	@echo "➜ Running the analyzer inside Docker container..."
	mkdir -p your_project/output
	docker run --rm \
		-v $(PWD)/your_project:/app/project \
		$(CONTAINER_IMAGE) \
		python -m src.main --project-path /app/project --output /app/project/output/report.json
	@echo "✔ Analysis complete. Report saved to your_project/output/report.json"

clean:
	@echo "➜ Cleaning up Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✔ Cleanup done."
