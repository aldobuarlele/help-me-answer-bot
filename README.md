# Help Me Answer - WhatsApp Automation Bot

A Python-based automation tool that connects WhatsApp Web to an LLM (Groq) to automate replies. This project uses Selenium WebDriver for browser interaction and maintains a local SQLite database to store conversation context.


## Features

* **Session Persistence:** Logs in once via QR code; subsequent runs use the stored Chrome session (no need to rescan).
* **Whitelist System:** Only replies to specific contact names defined in the configuration. Ignores all other chats.
* **Context Awareness:** Uses a local database to remember previous interactions with a specific user ID.
* **Human-like Behavior:**
    * Simulates typing with variable delays between keystrokes.
    * Implements "Hit & Run" logic (presses ESC) to reset unread badges for the listener.
    * Handles cooldowns: waits inside the chat for short delays, or marks as read and closes chat for long delays.
* **Robust Selector Strategy:** Uses multi-step XPath strategies to retrieve message text (handles standard text and some rich text formats).

## Prerequisites

* **OS:** macOS / Linux / Windows.
* **Python:** Version 3.10 or higher.
* **Browser:** Google Chrome (Latest version installed).
* **API Key:** Groq API Key (for the LLM engine).

## Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd help-me-answer
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### 1. Environment Variables
Create a `.env` file in the root directory and add your Groq API key:

```ini
GROQ_API_KEY=your_gsk_key_here

