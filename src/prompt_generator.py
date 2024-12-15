import json
import os
from typing import List, Dict, Optional
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptGenerator:
    """
    Generates prompts based on the analysis report.
    """

    # Define prompt templates for different tags and languages
    TAG_TEMPLATES = {
        "@BUG": {
            "default": (
                "Please fix the code below. Provide only the corrected code and no explanations or comments. "
                "Do not include the description of the tag in the comments.\n\n"
                "Code:\n"
                "{code_snippet}"
            ),
        },
        "@TODO": {
            "default": (
                "Please implement the following TODO. Provide only the corrected code and no explanations or comments. "
                "Do not include the description of the tag in the comments.\n\n"
                "Code:\n"
                "{code_snippet}"
            ),
        },
        "@REFACTOR": {
            "default": (
                "Refactor the code below for improved performance or readability. Provide only the refactored code and no explanations or comments. "
                "Do not include the description of the tag in the comments.\n\n"
                "Code:\n"
                "{code_snippet}"
            ),
        },
        "@IMPROVE": {
            "default": (
                "Improve the implementation of the following code. Provide only the improved code and no explanations or comments. "
                "Do not include the description of the tag in the comments.\n\n"
                "Code:\n"
                "{code_snippet}"
            ),
        },
        "@FIXME": {
            "default": (
                "Fix the issue in the following code. Provide only the corrected code and no explanations or comments. "
                "Do not include the description of the tag in the comments.\n\n"
                "Code:\n"
                "{code_snippet}"
            ),
        },
        "@HACK": {
            "default": (
                "Replace the following hack with a proper implementation. Provide only the corrected code and no explanations or comments. "
                "Do not include the description of the tag in the comments.\n\n"
                "Code:\n"
                "{code_snippet}"
            ),
        },
        # Add more tag templates as needed
    }

    # Mapping of file extensions to programming languages for context clarity
    LANGUAGE_MAP = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
    }

    def __init__(self, report_path: str):
        """
        Initializes the PromptGenerator.

        Args:
            report_path (str): Path to the analysis report JSON file.
        """
        self.report_path = report_path
        self.analysis_results: List[Dict] = []
        self.prompts: List[str] = []

    def load_report(self):
        """
        Loads the analysis report from the JSON file.
        """
        if not os.path.exists(self.report_path):
            logger.error(f"Report file '{self.report_path}' does not exist.")
            raise FileNotFoundError(f"Report file '{self.report_path}' does not exist.")

        with open(self.report_path, 'r', encoding='utf-8') as f:
            try:
                self.analysis_results = json.load(f)
                logger.info(f"Loaded {len(self.analysis_results)} comments from report.")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from '{self.report_path}': {e}")
                raise e

    def generate_prompt(self, result: Dict) -> List[str]:
        """
        Generates prompts for each tag in a single analysis result.

        Args:
            result (Dict): A single analysis result dictionary.

        Returns:
            List[str]: A list of generated prompts.
        """
        prompts = []
        tags = result.get("tags", [])
        context = result.get("context", [])

        for tag in tags:
            template_dict = self.TAG_TEMPLATES.get(tag)
            if template_dict:
                template = template_dict.get("default")
                if template:
                    # Join context lines to form a code snippet
                    code_snippet = "\n".join(context)
                    # Generate the prompt
                    prompt = template.format(code_snippet=code_snippet.strip())
                    prompts.append(prompt)
            else:
                # Handle unknown tags gracefully
                logger.warning(f"Unknown tag '{tag}' in result: {result}")

        return prompts

    def generate_prompts(self):
        """
        Generates prompts for all analysis results and stores them.
        """
        for result in self.analysis_results:
            prompts = self.generate_prompt(result)
            for prompt in prompts:
                logger.debug(f"Generated prompt: {prompt}")
                self.prompts.append(prompt)

    def generate_batched_prompt(self, file_path: str, lines: List[int], tags: List[str], context: List[str], full_content: str) -> str:
        """
        Generates a single prompt for a batch of tags in the same file.

        Args:
            file_path (str): Path to the file.
            lines (List[int]): Line numbers of the tags.
            tags (List[str]): List of tags in the file.
            context (List[str]): Context for the tags.
            full_content (str): Full content of the file.

        Returns:
            str: The generated prompt.
        """
        # Example implementation
        tag_list = ", ".join(tags)
        return (f"""The file contains the following tags requiring attention: {tag_list}
            File: {file_path}
            Relevant Lines: {lines}

            Full Content of the File:
            {full_content}

            Instructions:
            1. Provide fixes or improvements for the code where necessary.
            2. Include any necessary explanations only as inline comments within the code itself.
            3. Do not write any additional details or explanations outside of the code.
            4. Once all tasks are complete, remove the comment lines containing the tags that have been addressed.
            5. Respond with only the updated code in the provided language.
        """)


    def create_prompts(self):
        """
        High-level method to load the report and generate prompts.
        """
        self.load_report()
        self.generate_prompts()
