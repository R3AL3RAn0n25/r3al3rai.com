# R3AL3R AI Voice Assistant

This project implements a voice assistant for the R3AL3R AI. The assistant can be activated by voice and can perform various tasks.

## Project Structure

- `main.py`: The main entry point for the application.
- `AI_Core_Worker/R3AL3RAI/`: This directory contains the voice assistant code.
  - `voice_assistant.py`: The main file for the voice assistant.
  - `requirements.txt`: The dependencies for the voice assistant.

## How to Run

1. **Install Dependencies:**
   Install the required Python packages using pip:
   ```bash
   pip install -r AI_Core_Worker/R3AL3RAI/requirements.txt
   ```
   **Note:** `pyaudio` might require special installation steps depending on your operating system. Please refer to the PyAudio documentation for more information.

2. **Run the Application:**
   Execute the `main.py` script to start the voice assistant:
   ```bash
   python main.py
   ```

## How to Use

- The default wake word is "realer".
- Once the assistant is running, you can say "realer" followed by a command.
- For example, you can say "realer, list files" to list the files in the current directory.
- You can change the wake word by saying "realer, set wake word to [new wake word]".

## "Jarvis Mode"

The voice assistant has an "idle chatter" feature that makes it feel more like a companion. Every 2 minutes, the assistant will say "Systems nominal. Standing by." to let you know it's still there.
