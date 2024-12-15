import json
import os
from typing import List, Dict, Optional
from src.prompt_generator import PromptGenerator # type: ignore
from src.openai_assistant import OpenAIAssistant
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Assistant:
    """
    Assistant class responsible for reading analysis results, generating prompts, and interacting with the OpenAI Assistant API.
    """

    def __init__(self, results_path: str, openai_api_key: Optional[str] = None):
        """
        Initializes the Assistant.

        Args:
            results_path (str): Path to the analysis results JSON file.
            openai_api_key (Optional[str]): API key for OpenAIAssistant. If provided, enables sending prompts to the Assistant API.
        """
        self.results_path = results_path
        self.results: List[Dict] = []
        self.prompt_generator = PromptGenerator(report_path=self.results_path)
        self.openai_assistant = OpenAIAssistant(api_key=openai_api_key) if openai_api_key else None

    def load_results(self):
        """
        Loads the analysis results from the JSON file.
        """
        if not os.path.exists(self.results_path):
            logger.error(f"Results file '{self.results_path}' does not exist.")
            raise FileNotFoundError(f"Results file '{self.results_path}' does not exist.")

        with open(self.results_path, 'r', encoding='utf-8') as f:
            try:
                self.results = json.load(f)
                logger.info(f"Loaded {len(self.results)} results from '{self.results_path}'.")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from '{self.results_path}': {e}")
                raise e

    def generate_and_print_prompts(self):
        """
        Generates and prints prompts for each analysis result.
        """
        for result in self.results:
            prompts = self.prompt_generator.generate_prompt(result)
            for prompt in prompts:
                print(prompt)
                print("\n---\n")

    def send_prompts_to_api(self):
        """
        Sends generated prompts to the OpenAI Assistant API and writes the responses to 'responses.json'.
        """
        if not self.openai_assistant:
            logger.warning("OpenAIAssistant is not configured. Skipping API prompt sending.")
            return

        responses = []
        for result in self.results:
            prompts = self.prompt_generator.generate_prompt(result)
            for prompt in prompts:
                try:
                    response = self.openai_assistant.send_prompt(prompt)
                    # Extract relevant information from the response
                    content = response['choices'][0]['message']['content'].strip()
                    response_entry = {
                        "file": result.get("file", ""),
                        "line_number": result.get("line_number", ""),
                        "tag": result.get("tags", []),
                        "description": result.get("text", ""),
                        "response": content
                    }
                    responses.append(response_entry)
                    logger.info(f"Received response for file {response_entry['file']} at line {response_entry['line_number']}.")
                except Exception as e:
                    logger.error(f"Failed to get response for prompt: {prompt}\nError: {e}")
                    response_entry = {
                        "file": result.get("file", ""),
                        "line_number": result.get("line_number", ""),
                        "tag": result.get("tags", []),
                        "description": result.get("text", ""),
                        "response": f"Error: {e}"
                    }
                    responses.append(response_entry)

        # Define the path for responses.json
        output_dir = os.path.dirname(self.results_path)
        responses_path = os.path.join(output_dir, "responses.json")

        # Write responses to responses.json
        try:
            with open(responses_path, 'w', encoding='utf-8') as f:
                json.dump(responses, f, indent=4)
            logger.info(f"Responses have been written to '{responses_path}'.")
        except Exception as e:
            logger.error(f"Error writing responses to '{responses_path}': {e}")
            raise e
