# src/assistant.py

import json
import os
from typing import List, Dict
from src.prompt_generator import PromptGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Assistant:
    """
    Assistant class responsible for reading analysis results and generating prompts.
    """

    def __init__(self, results_path: str):
        """
        Initializes the Assistant.

        Args:
            results_path (str): Path to the analysis results JSON file.
        """
        self.results_path = results_path
        self.results: List[Dict] = []
        self.prompt_generator = PromptGenerator(report_path=self.results_path)

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
