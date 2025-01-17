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
        print(source)
        self.output = output
        self.code_content = self.load_code_content()

    def load_code_content(self):
        # Determine if the source is a directory or a GitHub URL
        if self.source.startswith("http") or self.source.startswith("www"):
            # Check if the URL is a GitHub repository
            if "github.com" not in self.source:
                return "ERROR: The URL provided is not a valid GitHub repository."

            # Clone the GitHub repository
            clone_dir = "./cloned_repo"
            self.source = clone_github_repo(self.source, clone_dir)

            # Clean up cloned repository if applicable
            if clone_dir:
                clean_up_clone(clone_dir)

        if not os.path.isdir(self.source):
            return f"ERROR: {self.source} is not a valid directory."

        # Parse the code and generate project documentation
        code_content = parse_code(self.source)
        if "ERROR" in code_content:
            return f"ERROR: {code_content['ERROR']}."
        if not code_content:
            return "ERROR: No valid code files found."

        return code_content

class Model():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("ERROR: OpenAI API key not found.")
            sys.exit(1)

        self.client = OpenAI()
        with open('./system_prompt.txt') as f:
            self.system_prompt = f.read()
        
    def generate_detailed_summary(self, code_content):
        """Generate detailed summaries for each file with focus on UML/MMD requirements"""
        
        single_file_prompt = """Analyze the following code file and provide a detailed technical summary focused on UML and diagram requirements.
        Structure your analysis in this exact format:

        ## Class Diagram Elements
        ```json
        {
            "classes": [
                {
                    "name": "ClassName",
                    "attributes": ["attribute1: type", "attribute2: type"],
                    "methods": ["method1(param: type): return_type", "method2(): void"],
                    "inherits_from": "ParentClass",
                    "implements": ["Interface1", "Interface2"]
                }
            ],
            "relationships": [
                {
                    "from": "ClassA",
                    "to": "ClassB",
                    "type": "inheritance|composition|aggregation|association",
                    "label": "optional relationship description"
                }
            ]
        }
        ```

        ## Sequence Flow
        ```json
        {
            "interactions": [
                {
                    "from": "ComponentA",
                    "to": "ComponentB",
                    "method": "methodName()",
                    "description": "what this interaction does"
                }
            ]
        }
        ```

        ## Dependencies
        ```json
        {
            "external": ["import1", "import2"],
            "internal": ["module1", "module2"],
            "environment_vars": ["VAR1", "VAR2"]
        }
        ```

        ## Methods Detail
        ```json
        {
            "method_name": {
                "inputs": ["param1: type", "param2: type"],
                "output": "return_type",
                "description": "what the method does",
                "calls": ["other_method1", "other_method2"]
            }
        }
        ```

        Ensure all JSON is valid and properly formatted for direct parsing.
        """
        
        all_summaries = {}
        
        for filename, content in code_content.items():
            messages = [
                {
                    "role": "system",
                    "content": single_file_prompt
                },
                {
                    "role": "user",
                    "content": f"```python\n{content}\n```"
                }
            ]

            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            
            all_summaries[filename] = completion.choices[0].message['content']
        
        # Combine all summaries with clear file separation
        combined_summary = "# Project Code Analysis\n\n"
        for filename, summary in all_summaries.items():
            combined_summary += f"\n# File: {filename}\n{summary}\n\n---\n"
        
        return combined_summary

    def generate_high_level_design(self, detailed_summary):
        """Generate high-level design based on the detailed summary"""
        design_prompt = """Based on the following detailed code summary, generate a comprehensive design document that includes both high-level and low-level design aspects. Format your response in markdown with emphasis on visual representation.

        # High-Level Design
        1. System Architecture Overview
           ```mermaid
           graph TD
               [Create a system architecture diagram showing main components and their relationships]
           ```

        2. Component Interactions
           ```mermaid
           sequenceDiagram
               [Create a sequence diagram showing key interactions between components]
           ```

        3. Data Flow
           ```mermaid
           flowchart LR
               [Create a data flow diagram showing how data moves through the system]
           ```

        # Low-Level Design
        1. Class Structure
           ```mermaid
           classDiagram
               [Create a detailed class diagram showing:
                - Class attributes
                - Methods
                - Relationships
                - Inheritance hierarchies]
           ```

        2. Module Dependencies
           ```mermaid
           graph LR
               [Create a dependency graph showing module relationships]
           ```

        Format the response as a structured technical design document using markdown and mermaid diagrams for visual representation.
        """
        
        messages = [
            {
                "role": "system",
                "content": design_prompt
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
        
        return completion.choices[0].message['content']

    def __call__(self, code, chat_history):
        client = OpenAI()
        
        messages = [
            {
                "role": "system",
                "content": self.system_prompt + f"\n\n{code}"
            }
        ]

        for msg in chat_history:
            messages.append({
                "role": msg.get("role"),
                "content": msg.get("content")
            })

        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages
        )

        return completion.choices[0].message['content']

if __name__ == '__main__':
    git_repo = 'https://github.com/BastinFlorian/RAG-Chatbot-with-Confluence'
    code = CodeFetcher(git_repo)
    code_content = code.code_content
    
    print(code_content)