IMAGE_NAME = refactoring_with_ai
IMAGE_TAG = latest
CONTAINER_IMAGE = $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: help build test run clean

help:
	@echo "Available targets:"
	@echo "  build     Build the Docker image."
	@echo "  test      Run all tests inside the container (TDD workflow)."
	@echo "  run       Run the main analysis application inside Docker."
	@echo "  clean     Remove Python cache files."

build:
	@echo "➜ Building Docker image: $(CONTAINER_IMAGE)"
	docker build --no-cache -t $(CONTAINER_IMAGE) .
	@echo "✔ Docker image built successfully."

test: build
	@echo "➜ Running tests inside Docker container..."
	docker run --rm $(CONTAINER_IMAGE) python -m pytest --verbose tests/
	@echo "✔ Tests completed."

run: build
	@mkdir -p your_project/output
	docker run --rm \
		-v $(PWD)/your_project:/app/project \
		--env-file .env \
		$(CONTAINER_IMAGE) \
		python -m src.main --project-path /app/project --output /app/project/output/report.json --verbose


clean:
	@echo "➜ Cleaning up Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✔ Cleanup done."
