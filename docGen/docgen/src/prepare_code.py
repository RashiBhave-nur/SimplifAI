import json
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from code_parser import parse_code
from github_integration import clone_github_repo, clean_up_clone
import re

class CodeFetcher():
    def __init__(self, source, output="./docs/documentation.md"):
        self.code_content = None
        self.source = source
        self.output = output
        self.clone_dir = False
        self.code_content = self.load_code_content()

    def load_code_content(self):
        # Determine if the source is a directory or a GitHub URL
        if self.source.startswith("http") or self.source.startswith("www"):
            # Check if the URL is a GitHub repository
            if "github.com" not in self.source:
                return "ERROR: The URL provided is not a valid GitHub repository."

            # Clone the GitHub repository
            self.clone_dir = "cloned_repo"
            self.source = clone_github_repo(self.source, self.clone_dir)

        if not os.path.isdir(self.source):
            return f"ERROR: {self.source} is not a valid directory."

        # Parse the code and generate project documentation
        code_content = parse_code(self.source)
        if "ERROR" in code_content:
            return f"ERROR: {code_content['ERROR']}."
        if not code_content:
            return "ERROR: No valid code files found."

        # Clean up cloned repository if applicable
        if self.clone_dir:
            clean_up_clone(self.clone_dir)
        return code_content

class Model():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("ERROR: OpenAI API key not found.")
            sys.exit(1)

        self.client = OpenAI()

        # Load the prompts
        with open('./system_prompt.txt') as f:
            self.system_prompt = f.read()
            
        with open('./summary_prompt.txt') as f:
            self.summary_prompt = f.read()
            
        with open('./hld_prompt.txt') as f:
            self.hld_prompt = f.read()

    def generate_detailed_summary(self, code_content):
        """
        Generate a detailed summary of all files in the codebase
        
        Args:
            code_content (dict): Dictionary where keys are filenames and values are file contents
                                Example: {"path/to/file.py": "def main():..."}
        """
        try:
            # Process all files in the batch together
            files_content = ""
            for filename, content in code_content.items():
                files_content += f"\nFile: {filename}\n```python\n{content}\n```\n"

            messages = [
                {
                    "role": "system",
                    "content": self.summary_prompt
                },
                {
                    "role": "user",
                    "content": files_content
                }
            ]

            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            
            # Extract JSON sections from the response
            response_text = completion.choices[0].message.content
            
            # Find and parse each JSON section
            json_sections = {}
            current_section = None
            json_content = []
            
            for line in response_text.split('\n'):
                if '```json' in line:
                    current_section = True
                    json_content = []
                elif '```' in line and current_section:
                    current_section = False
                    if json_content:
                        section_json = json.loads('\n'.join(json_content))
                        json_sections.update(section_json)
                elif current_section:
                    json_content.append(line)
            
            return json_sections
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {}
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {}

    def generate_high_level_design(self, detailed_summary):
        """Generate high-level design based on the detailed summary"""

        messages = [
            {
                "role": "system",
                "content": self.hld_prompt
            },
            {
                "role": "user",
                "content": f"Code Summary:\n{detailed_summary}"
            }
        ]

        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        return completion.choices[0].message.content

    def __call__(self, code, chat_history):
        client = OpenAI()
        
        messages = [
            {
                "role": "system",
                "content": self.system_prompt + f"\n\n{code}"
            },
            {
                "role": "user",
                "content": chat_history
            }
        ]

        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages
        )

        return completion.choices[0].message.content

    def filter_important_files(self, code_content):
        """Filter out non-essential files for high-level design"""
        # Patterns for files to exclude
        exclude_patterns = [
            # Documentation files
            r'README\.md$',
            r'CHANGELOG\.md$',
            r'LICENSE$',
            r'CONTRIBUTING\.md$',
            r'docs/.*$',
            
            # Configuration files
            r'\.gitignore$',
            r'\.env.*$',
            r'requirements\.txt$',
            r'setup\.py$',
            r'setup\.cfg$',
            r'pyproject\.toml$',
            r'package\.json$',
            r'package-lock\.json$',
            r'Pipfile$',
            r'Pipfile\.lock$',
            r'poetry\.lock$',
            
            # Test files
            r'test_.*\.py$',
            r'.*_test\.py$',
            r'tests/.*$',
            r'__tests__/.*$',
            
            # Build and cache files
            r'build/.*$',
            r'dist/.*$',
            r'\.cache/.*$',
            r'__pycache__/.*$',
            r'\.pytest_cache/.*$',
            r'\.coverage$',
            r'coverage\.xml$',
            
            # IDE and editor files
            r'\.vscode/.*$',
            r'\.idea/.*$',
            r'\.vs/.*$',
            r'\.DS_Store$',
            
            # Static and media files
            r'static/.*\.(css|js|jpg|jpeg|png|gif|svg)$',
            r'media/.*$',
            r'assets/.*$',
            
            # Migration files
            r'migrations/.*$',
            
            # Log files
            r'.*\.log$',
            r'logs/.*$'
        ]
        
        filtered_content = {}
        for filename, content in code_content.items():
            # Include file if it doesn't match any exclude pattern
            if not any(re.search(pattern, filename) for pattern in exclude_patterns):
                filtered_content[filename] = content
                
        return filtered_content

    def batch_process_files(self, code_content, batch_size=3):
        """Split files into manageable batches"""
        items = list(code_content.items())
        return [
            dict(items[i:i + batch_size])
            for i in range(0, len(items), batch_size)
        ]

    def combine_summaries(self, summaries):
        """Combine multiple summaries into a single coherent summary"""
        combined = {
            "classes": [],
            "relationships": [],
            "interactions": [],
            "dependencies": {
                "external": set(),
                "internal": set(),
                "environment_vars": set()
            }
        }
        
        for summary in summaries:
            try:
                # Extract classes and relationships
                if "classes" in summary:
                    combined["classes"].extend(summary["classes"])
                if "relationships" in summary:
                    combined["relationships"].extend(summary["relationships"])
                
                # Extract interactions
                if "interactions" in summary:
                    combined["interactions"].extend(summary["interactions"])
                
                # Extract dependencies
                if "dependencies" in summary:
                    deps = summary["dependencies"]
                    combined["dependencies"]["external"].update(deps.get("external", []))
                    combined["dependencies"]["internal"].update(deps.get("internal", []))
                    combined["dependencies"]["environment_vars"].update(deps.get("environment_vars", []))
            except (KeyError, TypeError) as e:
                print(f"Error processing summary: {e}")
                continue
        
        # Convert sets back to lists
        combined["dependencies"]["external"] = list(combined["dependencies"]["external"])
        combined["dependencies"]["internal"] = list(combined["dependencies"]["internal"])
        combined["dependencies"]["environment_vars"] = list(combined["dependencies"]["environment_vars"])
        
        return json.dumps(combined, indent=2)

if __name__ == '__main__':
    git_repo = 'https://github.com/BastinFlorian/RAG-Chatbot-with-Confluence'
    code = CodeFetcher(git_repo)
    code_content = code.code_content
    
    print(code_content)