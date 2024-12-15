import os
import json
import logging
import openai # type: ignore
from src.prompt_generator import PromptGenerator  # Adjust import path as necessary

class OpenAIAssistant:
    def __init__(self, results_path: str, api_key: str, model: str = "gpt-4", verbose: bool = False):
        self.results_path = results_path
        self.api_key = api_key
        self.output_dir = 'your_project/output'
        self.model = model
        self.verbose = verbose
        self.results = []
        self.batched_prompts = {}
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized OpenAIAssistant with model: {self.model}")

    def load_results(self):
        if not os.path.exists(self.results_path):
            raise FileNotFoundError(f"Results file {self.results_path} does not exist.")
        with open(self.results_path, 'r', encoding='utf-8') as f:
            self.results = json.load(f)
        self.logger.info(f"Loaded results from {self.results_path}")

    def batch_prompts_by_file(self):
        """
        Groups all tags for the same file and generates a single prompt per file.
        """
        for result in self.results:
            file_path = result["file"]
            line_number = result["line_number"]
            tags = result.get("tags", [])
            context = result.get("context", [])

            if file_path not in self.batched_prompts:
                self.batched_prompts[file_path] = {
                    "lines": [],
                    "tags": [],
                    "context": [],
                    "full_content": self._load_file_content(file_path)
                }

            self.batched_prompts[file_path]["lines"].append(line_number)
            self.batched_prompts[file_path]["tags"].extend(tags)
            self.batched_prompts[file_path]["context"].extend(context)

        self.logger.info(f"Batched prompts for {len(self.batched_prompts)} files.")

    def _load_file_content(self, file_path: str) -> str:
        """
        Loads the full content of the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.debug(f"Loaded content from {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Failed to load file content from {file_path}: {e}")
            raise RuntimeError(f"Error reading file {file_path}: {e}")

    def generate_batched_prompts(self):
        """
        Generates prompts for each batch (grouped by file).
        """
        generator = PromptGenerator(self.results_path)
        for file_path, batch in self.batched_prompts.items():
            prompt = generator.generate_batched_prompt(
                file_path=file_path,
                lines=batch["lines"],
                tags=batch["tags"],
                context=batch["context"],
                full_content=batch["full_content"]
            )
            batch["prompt"] = prompt
        self.logger.info("Generated batched prompts for all files.")

    def send_to_openai(self, prompt: str) -> str:
        """
        Sends the given prompt to the OpenAI API and returns the response.
        """
        openai.api_key = self.api_key
        if isinstance(prompt, list):
            # Combine the list into a single string
            prompt = "\n".join(prompt)

        self.logger.info("Sending prompt to OpenAI...")
        try:
            response = openai.Client().chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )

            # Access the response correctly using attributes
            message = response.choices[0].message.content
            self.logger.info("Received response from OpenAI.")
            return message
        except Exception as e:
            error_message = f"Error communicating with OpenAI: {e}"
            self.logger.error(error_message)
            raise RuntimeError(error_message)


    def save_response(self, file_path: str, response: str):
        """
        Saves the API response to a file in the output directory.
        """
        # Ensure the file path is relative to the project root
        relative_path = os.path.relpath(file_path, start="/app/project")
        
        # Map the relative path to the host's output directory
        host_output_path = os.path.join("/app/project/output", relative_path)

        # Ensure the directory structure exists
        os.makedirs(os.path.dirname(host_output_path), exist_ok=True)
        with open(host_output_path, 'w', encoding='utf-8') as f:
            f.write(response)
        self.logger.info(f"Saved response to {host_output_path}")

    def process_results(self):
        """
        Processes results: generates batched prompts, sends them to OpenAI, and saves the responses.
        """
        self.load_results()
        self.batch_prompts_by_file()
        self.generate_batched_prompts()

        for file_path, batch in self.batched_prompts.items():
            prompt = batch["prompt"]
            response = self.send_to_openai(prompt)
            self.save_response(file_path, response)

        self.logger.info("Processing of results completed.")