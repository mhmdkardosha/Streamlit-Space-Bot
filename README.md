# ExoBot 🚀

ExoBot is an interactive Streamlit chatbot designed to answer questions about exoplanets. It leverages generative AI and a CSV knowledge base to provide informative, friendly, and concise responses about exoplanet discovery and features.

## Features

- Conversational chatbot interface about exoplanets
- Uses Google Gemini (via `langchain-google-genai`) for AI responses
- Retrieves facts from a local CSV file (`exoplanets_cleaned.csv`)
- Supports follow-up questions and remembers chat history
- Multilingual and can translate between languages
- Customizable UI with a background image

## Requirements

- Python 3.8+
- See [`requirements.txt`](requirements.txt) for all dependencies

## Installation

1. Clone this repository:

    ```powershell
    git clone https://github.com/mhmdkardosha/Explanets-space-bot
    cd Exoplanets-space-bot
    ```

2. Install dependencies:

    ```powershell
    pip install -r requirements.txt
    ```

3. Add your `.env` file with necessary API keys (e.g., for Google Generative AI).

4. Ensure `exoplanets_cleaned.csv` and `background.jpg` are present in the project directory.

## Usage

Run the Streamlit app:

```powershell
streamlit run streamlit_app.py
```

Open the provided local URL in your browser to interact with ExoBot.

## Project Structure

- `streamlit_app.py` — Main application code
- `exoplanets_cleaned.csv` — Exoplanet data source
- `background.jpg` — Background image for UI
- `requirements.txt` — Python dependencies

## How It Works

- Loads exoplanet data and creates vector embeddings for retrieval.
- Uses a retrieval QA chain to answer questions from the CSV.
- Falls back to generative AI for general or follow-up questions.
- Maintains chat history for context-aware responses.

## License

MIT License

---

#### Made for NASA Space Apps Cairo Hackathon
