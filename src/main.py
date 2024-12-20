import argparse
import json
import os
from dotenv import load_dotenv # type: ignore
from src.analyzer import Analyzer
from src.openai_assistant import OpenAIAssistant

load_dotenv()

def get_next_report_filename(output_path: str) -> str:
    """
    Generates the next available report filename to avoid overwriting existing reports.
    If 'report.json' exists, it creates 'report_001.json', 'report_002.json', etc.
    """
    base, ext = os.path.splitext(output_path)
    if not os.path.exists(output_path):
        return output_path

    index = 1
    while True:
        new_filename = f"{base}_{index:03d}{ext}"
        if not os.path.exists(new_filename):
            return new_filename
        index += 1

def main():
    parser = argparse.ArgumentParser(description="Code Analysis Tool with OpenAI Integration")
    parser.add_argument("--project-path", type=str, required=True, help="Path to the project directory to analyze")
    parser.add_argument("--tags", type=str, nargs='+', default=["@TODO", "@FIXME", "@REFACTOR", "@IMPROVE", "@OPTIMIZE", "@DEPRECATE", "@REMOVE", "@BUG", "@HACK"],
                        help="Tags to search for in comments")
    parser.add_argument("--output", type=str, default="report.json", help="Output file for the report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Validate project path
    if not os.path.isdir(args.project_path):
        print(f"Error: The project path '{args.project_path}' does not exist or is not a directory.")
        exit(1)

    # Determine the full output path
    output_full_path = os.path.abspath(args.output)

    # Generate the next available report filename
    output_full_path = get_next_report_filename(output_full_path)

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_full_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Perform analysis
    analyzer = Analyzer(project_path=args.project_path, tags=args.tags)
    analyzer.analyze()
    comments = analyzer.get_comments()

    try:
        with open(output_full_path, 'w', encoding='utf-8') as f:
            json.dump(comments, f, indent=4)
        print(f"Analysis complete. Report saved to {output_full_path}")
    except Exception as e:
        print(f"Error writing report to '{output_full_path}': {e}")
        exit(1)

    # Get OpenAI API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set in environment. Please provide it in a .env file.")
        exit(1)

    # Process results with OpenAIAssistant
    assistant = OpenAIAssistant(
        api_key=api_key,
        results_path=output_full_path,
        verbose=args.verbose,
    )
    assistant.process_results()

if __name__ == "__main__":
    main()
