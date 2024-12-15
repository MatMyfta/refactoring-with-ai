import os
import json
import pytest
from unittest.mock import patch
from io import StringIO
from src.prompt_generator import PromptGenerator

@pytest.fixture
def sample_report(tmpdir):
    """
    Creates a sample analysis report JSON file for testing.
    """
    report = [
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
            "file": "/app/project/sample.java",
            "line_number": 9,
            "text": "@HACK: Temporary fix for performance issue",
            "context": [
                "",
                "/*",
                "@HACK: Temporary fix for performance issue",
                "*/",
                "public void process() {"
            ],
            "tags": [
                "@HACK"
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
        },
        {
            "file": "/app/project/sample.js",
            "line_number": 8,
            "text": "@IMPROVE: Add error handling",
            "context": [
                "",
                "/*",
                "@IMPROVE: Add error handling",
                "*/",
                "function divide(a, b) {"
            ],
            "tags": [
                "@IMPROVE"
            ]
        },
        {
            "file": "/app/project/sample.py",
            "line_number": 3,
            "text": "@TODO: Handle negative numbers",
            "context": [
                "",
                "def add(a, b):",
                "# @TODO: Handle negative numbers",
                "return a + b",
                ""
            ],
            "tags": [
                "@TODO"
            ]
        },
        {
            "file": "/app/project/sample.py",
            "line_number": 8,
            "text": "@FIXME: Subtraction logic might be incorrect",
            "context": [
                "def subtract(a, b):",
                "\"\"\"",
                "@FIXME: Subtraction logic might be incorrect",
                "\"\"\"",
                "return a - b"
            ],
            "tags": [
                "@FIXME"
            ]
        }
    ]

    report_path = tmpdir.join("results.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)

    return str(report_path)

def test_generate_prompt_for_bug(sample_report):
    """
    Test that PromptGenerator generates the correct prompt for a @BUG tag.
    """
    prompt_generator = PromptGenerator(report_path=sample_report)
    with open(sample_report, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    bug_result = results[0]  # First entry with @BUG
    expected_prompt = (
        "⚠️ BUG Detected\n\n"
        "- **File:** `sample.java`\n"
        "- **Line:** 3\n"
        "- **Description:** NullPointerException might occur\n"
        "- **Context:**\n\n"
        "public class Sample {\n"
        "// @BUG: NullPointerException might occur\n"
        "public int add(int a, int b) {\n"
        "return a + b;\n\n"
        "**Action Required:** Please investigate and fix the bug."
    )

    generated_prompt = prompt_generator.generate_prompt(bug_result)[0]
    assert generated_prompt == expected_prompt, f"Expected:\n{expected_prompt}\n\nGot:\n{generated_prompt}"

def test_generate_prompt_for_hack(sample_report):
    """
    Test that PromptGenerator generates the correct prompt for a @HACK tag.
    """
    prompt_generator = PromptGenerator(report_path=sample_report)
    with open(sample_report, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    hack_result = results[1]  # Second entry with @HACK
    expected_prompt = (
        "🛠️ HACK Alert\n\n"
        "- **File:** `sample.java`\n"
        "- **Line:** 9\n"
        "- **Description:** Temporary fix for performance issue\n"
        "- **Context:**\n\n"
        "/*\n"
        "@HACK: Temporary fix for performance issue\n"
        "*/\n"
        "public void process() {\n\n"
        "**Action Required:** Review and replace the hack with a proper solution."
    )

    generated_prompt = prompt_generator.generate_prompt(hack_result)[0]
    assert generated_prompt == expected_prompt, f"Expected:\n{expected_prompt}\n\nGot:\n{generated_prompt}"

def test_generate_prompt_with_unspecified_tag(sample_report, tmpdir):
    """
    Test that PromptGenerator generates a default prompt for an unspecified tag.
    """
    # Add an entry with an unspecified tag
    with open(sample_report, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    new_result = {
        "file": "/app/project/sample.rb",
        "line_number": 5,
        "text": "@UNKNOWN: Some unknown tag",
        "context": [
            "",
            "def example_method",
            "# @UNKNOWN: Some unknown tag",
            "puts 'Hello World'",
            "end"
        ],
        "tags": [
            "@UNKNOWN"
        ]
    }
    results.append(new_result)

    with open(sample_report, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    prompt_generator = PromptGenerator(report_path=sample_report)
    default_prompt = prompt_generator.generate_prompt(new_result)[0]
    
    expected_prompt = (
        "🔍 Tag `@UNKNOWN` Found\n\n"
        "- **File:** `sample.rb`\n"
        "- **Line:** 5\n"
        "- **Description:** @UNKNOWN: Some unknown tag\n\n"
        "**Context:**\n"
        "\n"
        "def example_method\n"
        "# @UNKNOWN: Some unknown tag\n"
        "puts 'Hello World'\n"
        "end\n"
    )

    assert default_prompt == expected_prompt, f"Expected:\n{expected_prompt}\n\nGot:\n{default_prompt}"
