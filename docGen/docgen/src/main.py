import json
import os
import sys
import argparse
from code_parser import parse_code
from doc_generator import generate_project_documentation
from github_integration import clone_github_repo, clean_up_clone


def load_api_key():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'secret.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('openai_api_key')
    except FileNotFoundError:
        print("Error: secret.json file not found. Please ensure it exists in the config directory.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: secret.json file is not a valid JSON. Please check the file content.")
        sys.exit(1)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate project documentation using OpenAI.")
    parser.add_argument("source", type=str, help="Path to the project directory or GitHub repository URL.")
    parser.add_argument("--output", type=str, default="/docs/documentation.md",
                        help="Path to the output file (default: /docs/documentation.md).")

    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("Error: API key not found in secret.json.")
        sys.exit(1)

    source = args.source
    output_file = args.output

    clone_dir = None

    # Determine if the source is a directory or a GitHub URL
    if source.startswith("http") or source.startswith("www"):
        # Check if the URL is a GitHub repository
        if "github.com" not in source:
            print("Error: The URL provided is not a valid GitHub repository.")
            sys.exit(1)

        # Clone the GitHub repository
        clone_dir = "cloned_repo"
        source = clone_github_repo(source, clone_dir)

    # if not os.path.isdir(source):
    #     print(f"Error: {source} is not a valid directory.")
    #     sys.exit(1)

    # Parse the code and generate project documentation
    code_content = parse_code(source)
    if not code_content:
        print("No valid code files found to document.")
        sys.exit(1)

    documentation = generate_project_documentation(code_content, api_key)
    if documentation:
        with open(output_file, 'w') as f:
            f.write(documentation)
        print(f"Documentation written to {output_file}")
    else:
        print("Failed to generate documentation.")

    # Clean up cloned repository if applicable
    if clone_dir:
        clean_up_clone(clone_dir)


if __name__ == "__main__":
    main()
