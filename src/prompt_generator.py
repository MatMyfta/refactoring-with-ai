# src/prompt_generator.py

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
                "⚠️ BUG Detected\n\n"
                "- **File:** `{file}`\n"
                "- **Line:** {line}\n"
                "- **Description:** {description}\n"
                "- **Context:**\n"
                "{code_snippet}\n\n"
                "**Action Required:** Please investigate and fix the bug."
            ),
        },
        "@TODO": {
            "default": (
                "📝 TODO Item\n\n"
                "- **File:** `{file}`\n"
                "- **Line:** {line}\n"
                "- **Description:** {description}\n"
                "- **Context:**\n"
                "{code_snippet}\n\n"
                "**Action Required:** Implement the TODO task."
            ),
        },
        "@REFACTOR": {
            "default": (
                "🔄 Refactoring Suggestion\n\n"
                "- **File:** `{file}`\n"
                "- **Line:** {line}\n"
                "- **Description:** {description}\n"
                "- **Context:**\n"
                "{code_snippet}\n\n"
                "**Action Required:** Refactor the code for better performance or readability."
            ),
        },
        "@IMPROVE": {
            "default": (
                "💡 Improvement Suggestion\n\n"
                "- **File:** `{file}`\n"
                "- **Line:** {line}\n"
                "- **Description:** {description}\n"
                "- **Context:**\n"
                "{code_snippet}\n\n"
                "**Action Required:** Improve the implementation as suggested."
            ),
        },
        "@FIXME": {
            "default": (
                "🔧 FIXME Notice\n\n"
                "- **File:** `{file}`\n"
                "- **Line:** {line}\n"
                "- **Description:** {description}\n"
                "- **Context:**\n"
                "{code_snippet}\n\n"
                "**Action Required:** Address the issue marked by FIXME."
            ),
        },
        "@HACK": {
            "default": (
                "🛠️ HACK Alert\n\n"
                "- **File:** `{file}`\n"
                "- **Line:** {line}\n"
                "- **Description:** {description}\n"
                "- **Context:**\n"
                "{code_snippet}\n\n"
                "**Action Required:** Review and replace the hack with a proper solution."
            ),
        },
        "@GLOBAL": {
            "default": (
                "🌐 Global Configuration Note\n\n"
                "- **File:** `{file}`\n"
                "- **Line:** {line}\n"
                "- **Description:** {description}\n"
                "- **Context:**\n"
                "{code_snippet}\n\n"
                "**Action Required:** Review the global configuration."
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
        # Add more mappings as needed
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
        file_name = os.path.basename(result.get("file", ""))
        line_number = result.get("line_number", "")
        text = result.get("text", "")
        context = result.get("context", [])

        for tag in tags:
            template_dict = self.TAG_TEMPLATES.get(tag)
            if template_dict:
                template = template_dict.get("default")
                if template:
                    # Determine language based on file extension
                    _, ext = os.path.splitext(result["file"])
                    language = self.LANGUAGE_MAP.get(ext.lower(), "Code")
                    # Join context lines to form a code snippet
                    code_snippet = "\n".join(context)
                    # Clean the description by removing the tag prefix
                    description = re.sub(rf'^{re.escape(tag)}\s*:\s*', '', text)
                    prompt = template.format(
                        file=file_name,
                        line=line_number,
                        description=description,
                        language=language,
                        code_snippet=code_snippet
                    )
                    prompts.append(prompt)
            else:
                # Default prompt for unspecified tags
                prompt = (
                    f"🔍 Tag `{tag}` Found\n\n"
                    f"- **File:** `{file_name}`\n"
                    f"- **Line:** {line_number}\n"
                    f"- **Description:** {text}\n\n"
                    f"**Context:**\n"
                    f"{'\n'.join(context)}\n"
                )
                prompts.append(prompt)

        return prompts

    def generate_prompts(self):
        """
        Generates prompts for all analysis results and prints them to the console.
        """
        for result in self.analysis_results:
            prompts = self.generate_prompt(result)
            for prompt in prompts:
                print(prompt)
                print("\n---\n")
                self.prompts.append(prompt)

    def create_prompts(self):
        """
        High-level method to load the report and generate prompts.
        """
        self.load_report()
        self.generate_prompts()
