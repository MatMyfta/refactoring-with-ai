#!/usr/bin/env bash

# ANSI color codes
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
BLUE='\e[34m'
BOLD='\e[1m'
RESET='\e[0m'

usage() {
    echo -e "${YELLOW}Usage: $0 [-e API_KEY] [project_path]"
    echo -e "  -e API_KEY: Specifies the OpenAI API key to use."
    echo -e "  project_path: Path to the project directory. Defaults to \$(pwd)/your_project if not provided.${RESET}"
    exit 1
}

ENV_API_KEY=""
PROJECT_PATH=""

# Parse options
while getopts ":e:" opt; do
  case $opt in
    e)
      ENV_API_KEY="$OPTARG"
      ;;
    \?)
      usage
      ;;
  esac
done

# Shift parsed options away, leaving a possible project path
shift $((OPTIND - 1))

# Default to current working directory + "/your_project" if no path provided
PROJECT_PATH=${1:-$(pwd)/your_project}

IMAGE_NAME="refactoring_with_ai:latest"

echo -e "${BLUE}${BOLD}➜ Building the Docker image: $IMAGE_NAME ...${RESET}"
docker build -t $IMAGE_NAME .
if [ $? -ne 0 ]; then
    echo -e "${RED}✘ Docker build failed.${RESET}"
    echo -e "${YELLOW}Please check the Dockerfile and the build logs above.${RESET}"
    exit 1
fi

echo -e "${GREEN}✔ Docker image built successfully!${RESET}"
echo -e "${BLUE}➜ Running container with project path: ${BOLD}$PROJECT_PATH${RESET}"

docker run \
    ${ENV_API_KEY:+-e OPENAI_API_KEY="$ENV_API_KEY"} \
    -e HOST_PROJECT_PATH="$PROJECT_PATH" \
    -v "$PROJECT_PATH:/app/project" \
    $IMAGE_NAME \
    --project-path /app/project

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✔ Container finished successfully!${RESET}"
else
    echo -e "${RED}✘ Container run encountered an issue.${RESET}"
fi
