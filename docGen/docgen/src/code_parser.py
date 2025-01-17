import os

# Map of file extensions to programming languages
LANGUAGE_MAP = {
    '.py': 'Python',
    '.java': 'Java',
    '.js': 'JavaScript',
    '.cpp': 'C++',
    '.cs': 'C#',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.html': 'HTML',
    '.css': 'CSS',
    '.sql': 'SQL',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.go': 'Go',
    '.rs': 'Rust',
    '.ts': 'TypeScript',
    '.dart': 'Dart',
    '.scala': 'Scala',
    '.r': 'R',
    '.m': 'MATLAB',
    '.pl': 'Perl',
    '.lua': 'Lua',
    '.sh': 'Shell',
    '.jl': 'Julia',
    '.hs': 'Haskell',
    '.md': 'Markdown',
    # Add more languages as needed
}

def parse_code(directory):
    code_content = {}
    # code_content = []
    if '.py' in directory:
        _, ext = os.path.splitext(directory)
        language = LANGUAGE_MAP.get(ext)
        if language:
            with open(directory, 'r') as f:
                code_content.append(f"\n# {directory}\n\n{f.read()}")
    else:
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)  # Include relative path
                    _, ext = os.path.splitext(file)
                    language = LANGUAGE_MAP.get(ext)
                    if language:
                        with open(file_path, 'r') as f:
                            # code_content.append(f"\n# {file_path}\n\n{f.read()}")
                            code_content[relative_path] = f.read()

        except Exception as e:
            return f"ERROR: {str(e)}"

    return code_content