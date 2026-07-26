# RAY-BOT

A simple project to create an AI Agent meant to streamline everyday tasks through the use of local AI models via Ollama.

## Installation

### Requirements
*   Python 3.11+
*   Docker & Docker-Compose

### Setup and Execution

1.  **Create a virtual environment:**
    Open your terminal in the project's root directory and create a Python virtual environment.

    ```bash
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**

    *   **macOS / Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

3.  **Install dependencies:**
    Install the required Python packages using pip.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Start services with Docker:**
    This will start the SearXNG search engine needed for the agent.

    ```bash
    docker compose up -d
    ```

5.  **Run the bot:**
    You can now run the main application.

    ```bash
    python main.py "your prompt here"
    ```
