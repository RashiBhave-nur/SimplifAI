# Dual Audio Processing Pipeline

## Project Title and Overview
**Dual Audio Processing Pipeline**  
This project is a dual-channel audio processing pipeline designed to transcribe, diarize, analyze sentiment, and redact sensitive information from audio files. The main purpose is to allow users to process audio recordings with two speakers, extracting meaningful insights while ensuring privacy through redaction. This pipeline addresses the challenges of understanding conversations in multi-speaker audio files, providing a cohesive output that summarizes the dialogue while highlighting sentiments.

## Features
- **Transcription of Dual Channels**: Transcribes audio from two different channels simultaneously, providing accurate text output for both speakers.
- **Diarization**: Merges and organizes transcribed text by identifying speaker chunks, allowing users to distinguish between different speakers.
- **Sentiment Analysis**: Analyzes transcribed text to extract sentiment, categorizing each speaker's contributions based on emotional tone.
- **Redaction**: Automatically redacts sensitive information from the transcribed text before output, ensuring privacy.
- **Detailed Logging**: Tracks each step in the processing pipeline, including errors, to allow for easy debugging and monitoring.
- **Output Generation**: Generates a structured JSON file that details every step of the audio processing, summarizing results for user reference.

## Installation
1. **Prerequisites**: Ensure Python 3.7 or higher is installed on your system.
2. **Clone the repository**: 
   ```bash
   git clone https://github.com/username/dual-audio-pipeline.git
   cd dual-audio-pipeline
   ```
3. **Install Required Packages**: Use pip to install the necessary dependencies.
   ```bash
   pip install torch pydub asyncio
   ```
4. **Configure Environment**: Set up any necessary environmental variables or configurations required for audio processing, if applicable.
5. **Run the Application**: You can now run the application using:
   ```bash
   python main.py path_to_your_audio_file.wav
   ```

## Usage
To use the Dual Audio Processing Pipeline, simply provide the path to your stereo audio file when running the script. For example:
```bash
python main.py /path/to/audio_file.wav
```
Upon completion, the final transcribed, diarized, and redacted text will be output to the console along with a JSON file detailing the processing steps and results.

## Code Structure
- **`main-dual.py`**: The main script that orchestrates the entire audio processing pipeline.
- **`transcription.py`**: Contains the `TranscriptionService` which is responsible for handling audio transcription.
- **`redaction.py`**: Includes functions to redact sensitive information from the transcribed text.
- **`utils.py`**: Provides utility functions for logging, audio file processing, and data manipulation.
- **`sentiment.py`**: Module to determine sentiment labels from the transcribed text.
- **`api_endpoints.py`**: Contains functions for handling API calls relevant to the processing status and submissions.

### Main Components
1. **Pipeline Initialization**: 
   - The `init_pipeline_data()` function sets up a structure to track the processing steps and outputs.
  
2. **Step Tracking Functions**:
   - `set_step_start()`, `set_step_end()`, and `set_step_error()` manage the logging of each processing step.

3. **run_dual_pipeline()**: 
   - The main asynchronous function that runs the end-to-end processing pipeline:
     - Creates an initial call log via `create_initial_call`.
     - Separates audio channels with `separate_channels`.
     - Transcribes audio from both channels using `TranscriptionService`.
     - Merges and diarizes the transcribed text.
     - Conducts sentiment analysis on the processed chunks.
     - Redacts sensitive information using the `redact_text` function.
     - Generates a final output in JSON format and cleans up temporary files.

4. **CLI Entry Point**:
   - The script's entry point checks for the provided audio file and initiates the pipeline. 

### Pipeline Flow
- **Initialization**: Starts by creating a structured data object to monitor progress.
- **Transcription**: Handles the transcription of both audio channels in parallel.
- **Diarization**: Processes the transcription to format sentences by speaker turns.
- **Sentiment Analysis**: Evaluates the sentiment of each speaker's words and records it in the output.
- **Redaction**: Filters out any sensitive information before finalizing the output.
- **Completion**: Logs the completion and cleans up temporary files, returning the output text to the console.

With this structure, the code is well-organized and modular, simplifying maintenance and updates. The detailed JSON logs also provide useful insights for any future enhancement or debugging efforts.