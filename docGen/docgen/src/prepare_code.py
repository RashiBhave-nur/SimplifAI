import json
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from code_parser import parse_code
from github_integration import clone_github_repo, clean_up_clone

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

        all_summaries = {}
        
        for filename, content in code_content.items():
            messages = [
                {
                    "role": "system",
                    "content": self.summary_prompt
                },
                {
                    "role": "user",
                    "content": f"```python\n{content}\n```"
                }
            ]

            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            
            all_summaries[filename] = completion.choices[0].message.content
        
        # Combine all summaries with clear file separation
        combined_summary = "# Project Code Analysis\n\n"
        for filename, summary in all_summaries.items():
            combined_summary += f"\n# File: {filename}\n{summary}\n\n---\n"
        
        return combined_summary

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

if __name__ == '__main__':
    git_repo = 'https://github.com/BastinFlorian/RAG-Chatbot-with-Confluence'
    code = CodeFetcher(git_repo)
    code_content = code.code_content
    
    print(code_content)