import openai


def generate_project_documentation(code_content, api_key):
    """
    Generates a clean and detailed README for the entire project using the OpenAI GPT-4 API.

    Parameters:
    - code_content (str): The combined code content of the project.
    - api_key (str): The API key for OpenAI.

    Returns:
    - str: Generated README text, formatted and ready to be used as a markdown file.
    """
    openai.api_key = api_key

    # Create a detailed and clean prompt for GPT-4
    prompt = (
        "You are an expert technical writer. Generate a detailed, well-structured, and clean Documentation file for the following software project. "
        "The Documentation should be directly usable as a markdown file without additional markdown formatting or unnecessary sections. "
        "The Documentation should include the following sections:\n\n"
        "1. Project Title and Overview: A clear and concise title for the project, followed by an overview that explains what the project does, its purpose, and the problem it aims to solve.\n\n"
        "2. Features: A detailed list and description of all the main features of the project, explaining how each feature benefits the user.\n\n"
        "3. Installation: Step-by-step instructions on how to install the project, including any prerequisites, dependencies, and configurations required. "
        "These instructions should be comprehensive enough for someone with basic knowledge of the technology stack to follow.\n\n"
        "4. Usage: Detailed examples of how to use the project, covering common use cases and important configurations.\n\n"
        "5. Code Structure: An explanation of the codebase structure, including the purpose of key directories and files. Detail how the main components interact, and provide an overview of the core classes, functions, or modules.\n\n"
        "Here is the relevant code from the project:\n\n"
        f"{code_content}\n\n"
        "Please analyze this code to generate a detailed line by line code explanation based documentation explaining each line of the code that accurately reflects the project's purpose, structure, and functionality."
    )

    # Call to OpenAI API using ChatCompletion with GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    documentation = response.choices[0].message['content'].strip()
    return documentation
    