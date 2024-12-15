import os
import json
import pytest
from unittest.mock import patch, MagicMock
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

def test_assistant_loads_results(sample_results):
    """
    Test that the Assistant correctly loads analysis results from the JSON file.
    """
    assistant = Assistant(results_path=sample_results)
    assistant.load_results()
    assert len(assistant.results) == 2
    assert assistant.results[0]["file"] == "/app/project/sample.java"
    assert assistant.results[1]["tags"] == ["@REFACTOR"]

@patch('src.openai_assistant.OpenAIAssistant.send_prompt')
def test_assistant_generate_and_print_prompts(mock_send_prompt, sample_results):
    """
    Test that the Assistant generates and prints prompts correctly.
    """
    # Mock the OpenAIAssistant.send_prompt method to prevent actual API calls
    mock_send_prompt.return_value = {
        'choices': [{'message': {'content': 'Mocked response for prompt.'}}]
    }

    assistant = Assistant(results_path=sample_results, openai_api_key="dummy_api_key")
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
        import re
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

def test_assistant_send_prompts_to_api(sample_results):
    """
    Test that the Assistant sends prompts to the API and writes responses correctly.
    """
    # Mock the OpenAIAssistant.send_prompt method to prevent actual API calls
    mock_response = {
        'choices': [{'message': {'content': 'Mocked response for prompt.'}}]
    }

    with patch('src.openai_assistant.OpenAIAssistant.send_prompt', return_value=mock_response) as mock_send_prompt:
        assistant = Assistant(results_path=sample_results, openai_api_key="dummy_api_key")
        assistant.load_results()

        # Run the method to send prompts to the API
        assistant.send_prompts_to_api()

        # Ensure send_prompt was called twice (once for each prompt)
        assert mock_send_prompt.call_count == 2

        # Check the content of responses.json
        output_dir = os.path.dirname(assistant.results_path)
        responses_path = os.path.join(output_dir, "responses.json")
        assert os.path.exists(responses_path), "responses.json was not created."

        with open(responses_path, 'r', encoding='utf-8') as f:
            responses = json.load(f)

        assert len(responses) == 2, "Number of responses does not match number of prompts."
        for response in responses:
            assert "file" in response
            assert "line_number" in response
            assert "tag" in response
            assert "description" in response
            assert "response" in response
            assert response["response"] == "Mocked response for prompt."
