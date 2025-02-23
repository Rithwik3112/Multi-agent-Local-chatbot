# Multi-Agent Local Chatbot

## Overview

The **Multi-Agent Local Chatbot** is an AI-driven chatbot system designed to operate locally, utilizing multiple AI agents to enhance conversational capabilities. This chatbot can handle diverse queries by leveraging different AI models, ensuring accurate and context-aware responses. Additionally, it integrates APIs to fetch real-time data when necessary.

## Features

- **Multi-Agent Architecture:** Uses multiple AI models to process and respond to queries.
- **Real-Time Data Integration:** Connects to APIs for up-to-date information retrieval.
- **Local Execution:** Runs entirely on a local machine with optional cloud-based APIs.
- **Customizable:** Users can modify the AI agents based on their requirements.
- **Scalable:** Supports integration with various machine learning frameworks.
- **Efficient Query Handling:** Routes user queries to the most suitable AI agent for optimal responses.
- **Command Execution:** Supports file and folder operations like creating, deleting, opening, and finding files.
- **WhatsApp Messaging:** Allows sending messages via WhatsApp.
- **Timetable Lookup:** Retrieves class schedules based on queries.
- **Weather Information:** Fetches current weather details.
- **Stock Price Retrieval:** Provides real-time stock prices.

## Installation

### Prerequisites

- Python 3.8+
- Virtual Environment (optional but recommended)
- Required Python libraries (specified in `requirements.txt`)
- Local AI models for chatbot execution
- API keys for real-time data retrieval (if applicable)

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/Multi-agent-Local-chatbot.git
   cd Multi-agent-Local-chatbot
   ```

2. **Create and Activate a Virtual Environment (Optional):**

   ```bash
   python -m venv env
   source env/bin/activate  # On macOS/Linux
   env\Scripts\activate  # On Windows
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Keys (If Required):**
   
   - Store API keys in a `.env` file or `config.json`.
   - Ensure API access for real-time data retrieval.

5. **Run the Chatbot:**

   ```bash
   python main.py
   ```

## Usage

- Start the chatbot by running `main.py`.
- Interact with the chatbot through the terminal or integrate it with a web-based UI.
- Modify configurations in `config.json` to customize chatbot behavior.
- Enable API connections for real-time data fetching.

### Supported Functionalities

- **General Conversation:** AI-driven chatbot for handling natural language queries.
- **File and Folder Operations:** Create, delete, open, and find files or directories.
- **Stock Price Retrieval:** Fetch real-time stock data.
- **Weather Information:** Get current weather details based on public IP location.
- **WhatsApp Messaging:** Send messages via WhatsApp.
- **Timetable Lookup:** Retrieve class schedules based on user queries.

## Configuration

Modify the `config.json` file to adjust settings such as:

- Default AI model
- API keys and endpoints for real-time data
- Response timeout
- Logging preferences

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch.
3. Implement changes and test them locally.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contact

For questions or support, please reach out via email at `your-email@example.com` or open an issue in the repository.

