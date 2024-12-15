# tests/test_assistant.py

import os
import re
import json
import pytest
from unittest.mock import patch
from io import StringIO
from src.assistant import Assistant

@pytest.fixture
def sample_results(tmpdir):
    """
    Creates a sample results.json file for testing.
    """
    results = [
        {
            "file": "/app/project/sample.java",
            "line_number": 3,
            "text": "@BUG: NullPointerException might occur",
            "context": [
                "",
                "public class Sample {",
                "// @BUG: NullPointerException might occur",
                "public int add(int a, int b) {",
                "return a + b;"
            ],
            "tags": [
                "@BUG"
            ]
        },
        {
            "file": "/app/project/sample.js",
            "line_number": 3,
            "text": "@REFACTOR: Improve performance",
            "context": [
                "",
                "function multiply(a, b) {",
                "// @REFACTOR: Improve performance",
                "return a * b;",
                "}"
            ],
            "tags": [
                "@REFACTOR"
            ]
        }
    ]

    results_path = tmpdir.join("results.json")
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    return str(results_path)

@pytest.fixture
def sample_results_with_multiple_tags(tmpdir):
    """
    Creates a sample results.json file with multiple tags in a single comment for testing.
    """
    results = [
        {
            "file": "/app/project/sample.java",
            "line_number": 10,
            "text": "@BUG: NullPointerException might occur @TODO: Add logging",
            "context": [
                "",
                "public int calculate(int a, int b) {",
                "// @BUG: NullPointerException might occur @TODO: Add logging",
                "return a + b;",
                "}"
            ],
            "tags": [
                "@BUG",
                "@TODO"
            ]
        }
    ]

    results_path = tmpdir.join("results_multiple_tags.json")
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    return str(results_path)

def test_assistant_loads_results(sample_results):
    """
    Test that the Assistant correctly loads analysis results from the JSON file.
    """
    assistant = Assistant(results_path=sample_results)
    assistant.load_results()
    assert len(assistant.results) == 2
    assert assistant.results[0]["file"] == "/app/project/sample.java"
    assert assistant.results[1]["tags"] == ["@REFACTOR"]

import re
from io import StringIO
from unittest.mock import patch

def test_assistant_generate_and_print_prompts(sample_results):
    """
    Test that the Assistant generates and prints prompts correctly.
    """
    assistant = Assistant(results_path=sample_results)
    assistant.load_results()

    expected_prompts = [
        """⚠️ BUG Detected

        - **File:** `sample.java`
        - **Line:** 3
        - **Description:** NullPointerException might occur
        - **Context:**

        public class Sample {
        // @BUG: NullPointerException might occur
        public int add(int a, int b) {
        return a + b;

        **Action Required:** Please investigate and fix the bug.""",
        """🔄 Refactoring Suggestion

        - **File:** `sample.js`
        - **Line:** 3
        - **Description:** Improve performance
        - **Context:**

        function multiply(a, b) {
        // @REFACTOR: Improve performance
        return a * b;
        }

        **Action Required:** Refactor the code for better performance or readability."""
    ]

    with patch('sys.stdout', new=StringIO()) as fake_out:
        assistant.generate_and_print_prompts()
        output = fake_out.getvalue().strip().split('\n\n---\n\n')

        # Normalize whitespace in generated and expected prompts
        def normalize(text):
            return re.sub(r'\s+', ' ', text.strip())

        output_normalized = [normalize(o.replace('---', '')) for o in output]
        expected_normalized = [normalize(e) for e in expected_prompts]

        # Compare lengths
        assert len(output_normalized) == len(expected_normalized), \
            f"Expected {len(expected_prompts)} prompts, got {len(output_normalized)}"

        # Compare each prompt
        for i, (generated, expected) in enumerate(zip(output_normalized, expected_normalized)):
            assert generated == expected, (
                f"Prompt {i+1} does not match.\n\n"
                f"Expected:\n{expected}\n\n"
                f"Got:\n{generated}"
            )
