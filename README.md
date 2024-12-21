# Simple RAG chatbot ultimatefitness
## pinecone as a vector db, integration with Brevo Webhook, API

This is a basic structure for a ultimatefitness RAG chatbot project designed to interact with Brevo Webhook, API

## Getting Started

1. Create a `.env` file with the following content:
   ```
    OPENAI_API_KEY=
    PINECONE_API_KEY=
    PINECONE_INDEX_NAME=uf-chatbot
    BREVO_API_KEY=
   ```

2. Create a virtual environment:
   ```bash
   virtualenv venv
   ```

3. Install the required packages:
   ```bash
   (venv) pip install -r requirements.txt
   ```

4. To run the UI simply:
   ```bash
   (venv) streamlit run streamlit_main.py
   ```

5. Run the webhook globally:
   ```bash
   (venv) python main.py
   ```

## Getting Started (using Docker)

1. Install docker and docker compose

2. Simply run docker compose:
   ```
   docker compose up -d
   ```