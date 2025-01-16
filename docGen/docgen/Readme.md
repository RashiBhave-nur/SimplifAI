# DocGen - AI-Powered Automated Documentation Tool

**DocGen** is a versatile tool designed to automatically generate comprehensive documentation for your software projects using AI (powered by GPT-4 or similar models). The tool supports multiple programming languages and can generate detailed README files directly from the source code, whether the project is hosted locally or on GitHub.

## Features

- **AI-Powered Documentation Generation**: Utilizes GPT-4 (or similar models) to generate detailed and structured documentation, including a well-formatted README file for your project.
- **Multi-Language Support**: Automatically parses and documents code written in various programming languages, such as Python, Java, JavaScript, C++, and C#.
- **GitHub Integration**: Clone a GitHub repository and generate documentation for it directly, without needing to download the project manually.
- **Configurable Output**: Specify where the generated documentation should be saved, with a default output path provided.
- **Automated Cleanup**: Automatically cleans up cloned repositories after documentation is generated.

## Installation

1. **Clone the repository to your local machine**:
   ```bash
   git clone https://github.com/enricolacchin/docgen.git
   cd docgen
   ```

2. **Create a virtual environment and install the required dependencies**:
   ```bash
   python -m venv docgen-env
   source docgen-env/bin/activate  # On Windows: docgen-env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   - Rename the file [secret_nokey.json](config/secret_nokey.json) to `secret.json` in the `config` directory with the following content:
   - Replace `"YOUR_OPENAI_API_KEY_HERE"` with your actual OpenAI API key.

## Usage

### Generate Documentation for a Local Project

To generate documentation for a local project, run the following command:

```bash
python src/main.py [PROJECT PATH] --output [DOCUMENTATION PATH]
```

For example:

```bash
python src/main.py ./src --output /docs/documentation.md
```

### Generate Documentation from a GitHub Repository

To generate documentation directly from a GitHub repository, use the repository's URL as the source:

```bash
python src/main.py https://github.com/username/repository --output [DOCUMENTATION PATH] 
```

For example:

```bash
python src/main.py https://github.com/enricolacchin/docgen --output /docs/documentation.md
```

### Options

- `--output`: Specifies the path to the output file where the generated documentation will be saved. If not specified, the default path is `/docs/documentation.md`.

### UML Diagram Generation

*Note: UML diagram generation is not currently implemented in this version of DocGen, but it is planned for future releases.*

## Code Structure

- **`src/code_parser.py`**: Contains the logic for parsing the code in different programming languages and preparing it for documentation.
- **`src/doc_generator.py`**: Interfaces with the OpenAI API to generate a detailed README or other documentation for the project.
- **`src/github_integration.py`**: Handles cloning and cleaning up GitHub repositories, making it easy to generate documentation for projects hosted on GitHub.
- **`src/main.py`**: The main entry point for the tool, managing the workflow of parsing code, generating documentation, and handling output.
- **`config/secret.json`**: Stores the OpenAI API key securely, which is required for generating documentation.

## Roadmap

- **UML Diagram Generation**: Add support for generating UML diagrams to visualize class relationships and other design aspects of the code.
- **Expanded Language Support**: Continue to enhance support for additional programming languages and improve AI-generated documentation accuracy.
- **Advanced AI Capabilities**: Integrate more sophisticated AI models and allow for customization of the generated documentation.
- **Graphical User Interface**: Develop a GUI to make DocGen more accessible, especially for non-technical users.

## Contributing

Contributions are welcome! Whether it's improving the code, expanding language support, or enhancing the AI prompts, your help is appreciated. Please open an issue to discuss any major changes or submit a pull request with your improvements.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License. You are free to share this work with proper attribution, but you may not use it for commercial purposes or distribute derivative works. See the [LICENSE](LICENSE) file for full details.
