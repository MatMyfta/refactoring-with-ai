# Refactoring with AI

Refactoring with AI is a powerful tool designed to analyze your codebase, detect code smells, and suggest improvements using OpenAI's advanced language models. By leveraging automated analysis and intelligent prompt generation, this tool helps developers maintain high-quality code, reduce technical debt, and enhance overall code performance and readability.

## Features

- **Code Analysis**: Scans your codebase for specific tags indicating areas that need attention, such as `@TODO`, `@REFACTOR`, `@BUG`, and more.
- **AI-Powered Suggestions**: Uses OpenAI's models to generate actionable code improvements based on detected code smells.
- **Customizable Tags**: Easily configure which tags to look for during analysis.
- **Verbose Logging**: Provides detailed logs for better traceability and debugging.
- **Dockerized Setup**: Simplifies environment setup and ensures consistency across different development environments.
- **Automated Reporting**: Generates reports of detected issues and the corresponding AI-generated fixes.

## Getting Started

Follow these instructions to set up and run **Refactoring with AI** on your local machine.

## Prerequisites

**Docker**: Ensure Docker is installed on your system. Download Docker
**Make**: Install make for managing build and run commands. GNU Make Installation
**Python 3.8+**: Required for running the analysis scripts. Download Python
**OpenAI API Key**: Sign up for an API key from OpenAI.

## Installation

1. Clone the Repository

```bash
git clone https://github.com/yourusername/refactoring-with-ai.git
cd refactoring-with-ai
Set Up Environment Variables
```

2. Create a .env file in the root directory and add your OpenAI API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

Important: Ensure that .env is listed in your .gitignore to prevent accidental commits of sensitive information.

3. Install Dependencies

The project uses Docker to manage dependencies. Build the Docker image using the provided Makefile:

```bash
make build
Configuration
```

## Customizing Tags

By default, Refactoring with AI looks for the following tags in your code comments:

- `@TODO`
- `@FIXME`
- `@REFACTOR`
- `@IMPROVE`
- `@OPTIMIZE`
- `@DEPRECATE`
- `@REMOVE`
- `@BUG`
- `@HACK`

To customize or add more tags, modify the `--tags` argument when running the tool or adjust the Analyzer class in `src/analyzer.py`.

## Prompt Templates
The PromptGenerator class in src/prompt_generator.py defines how prompts are structured for different tags. You can modify these templates to better suit your needs or to enhance the AI's responses.

Usage
Makefile Commands
The project utilizes a Makefile to streamline common tasks. Below are the primary commands:

Build the Docker Image

```bash
make build
```

Run Tests

```bash
make test
```

Run the Analysis Tool

```bash
make run
```

Clean Up Cache Files

```bash
make clean
```

## Running the Tool

### Ensure Your Project is Ready

Place the codebase you wish to analyze inside the your_project directory. For example:

```bash
refactoring-with-ai/
├── your_project/
│   ├── src/
│   ├── tests/
│   ├── example_code_smells.py
│   ├── exampleCodeSmells.js
│   └── ExampleCodeSmells.java
├── Dockerfile
├── Makefile
├── requirements.txt
├── .env
└── README.md
```

### Run the Analysis

Execute the following command to perform the analysis, generate prompts, send them to OpenAI, and save the responses:

```bash
make run
```

What Happens:

- Builds the Docker image if not already built.
- Runs the Docker container with the necessary environment variables.
- Analyzes the codebase in your_project for specified tags.
- Generates prompts based on detected code smells.
- Sends prompts to the OpenAI API for suggestions.
- Saves the AI-generated fixes in your_project/output.
- View the Results

After successful execution, navigate to your_project/output to find the updated files with AI suggestions incorporated.

```bash
your_project/
├── output/
│   ├── example_code_smells.py
│   ├── exampleCodeSmells.js
│   └── ExampleCodeSmells.java
```

## Project Structure

```bash
refactoring-with-ai/
│
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
├── .env
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── analyzer.py
│   ├── openai_assistant.py
│   └── prompt_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_openai_assistant.py
│   └── test_prompt_generator.py
├── your_project/
│   ├── src/
│   ├── tests/
│   ├── example_code_smells.py
│   ├── exampleCodeSmells.js
│   ├── ExampleCodeSmells.java
│   └── output/
│       ├── example_code_smells.py
│       ├── exampleCodeSmells.js
│       └── ExampleCodeSmells.java
```

### Key Directories and Files

- **Dockerfile**: Defines the Docker image, including dependencies and environment setup.
- **Makefile**: Contains commands for building, testing, running, and cleaning the project.
- **src/**: Source code for the analysis tool.
  - **main.py**: Entry point of the application.
  - **analyzer.py**: Handles scanning of code files for tags.
  - **openai_assistant.py**: Manages communication with OpenAI API.
  - **prompt_generator.py**: Generates prompts based on analysis results.
- **tests/**: Contains unit and integration tests.
- **your_project/**: Placeholder for the user's codebase to be analyzed.
  - **output/**: Directory where AI-generated fixes are saved.
- **docs/**: Documentation assets like screenshots.
- **.env**: Environment variables file (should include `OPENAI_API_KEY`).

## How It Works

1. **Tag Detection**: The Analyzer scans through your codebase in your_project, looking for predefined tags such as @TODO and `@REFACTOR` in comments that indicate areas needing improvement.
2. **Prompt Generation**: For each detected tag, the PromptGenerator creates a structured prompt that includes the file's full content and the specific lines where issues are found. The prompt is engineered to instruct OpenAI to provide only the improved code with inline comments, without any additional explanations.
3. **Batch Processing**: To optimize performance and reduce costs, the tool batches multiple tags within the same file into a single prompt, minimizing the number of API calls to OpenAI.
4. **AI Interaction**: The OpenAIAssistant sends these prompts to OpenAI's GPT-4 model, which processes the requests and generates code improvements.
5. **Saving Responses**: The AI-generated fixes are saved back into the your_project/output directory, maintaining the original file structure.
6. **Logging**: Detailed logs are maintained to trace the analysis process, making it easier to debug and understand the tool's operations.

## Testing

The project includes a suite of unit and integration tests to ensure reliability and correctness.

### Running Tests

Build the Docker Image

```bash
make build
```

Execute Tests Inside the Docker Container

```bash
make test
```

This command runs all tests located in the tests/ directory using pytest.

## Contributing

Contributions are welcome! Please follow these guidelines to help us improve the project.

### How to Contribute

1. Fork the Repository: Click the "Fork" button at the top-right corner of the repository page to create your own copy.
2. Clone Your Fork

```bash
git clone https://github.com/MatMyfta/refactoring-with-ai.git
cd refactoring-with-ai
```

3. Create a New Branch

```bash
git checkout -b feature/your-feature-name
```

4. Make Your Changes: Implement your feature or fix the issue.
5. Run Tests: Ensure all tests pass before committing.

```bash
make test
```

6. Commit Your Changes

```bash
git commit -m "Add feature: Your Feature Description"
```

7. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

8. Create a Pull Request: Navigate to your fork on GitHub and click the "Compare & pull request" button. Provide a clear description of your changes.

## Code of Conduct

Please adhere to the Contributor Covenant code of conduct when participating in this project.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **OpenAI** for providing the GPT-4 API used in this project.
- **Docker** for containerizing the application.
- **Make** for simplifying build and run commands.
- **pytest** for the testing framework.
