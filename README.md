# # Customized Chatbot
A powerful chatbot application built using FastAPI, LangChain, Gradio, and Ollama, with integrated support for document processing and conversational AI over official U.S. Federal Registry documents.

# Overview
This project demonstrates a robust chatbot implementation that integrates:

FastAPI for API backend

Ollama (running llama3:8b) for inference

LangChain for document retrieval & prompt engineering

Gradio for a user-friendly interface

MySQL as the backend database

Additionally, it performs a full ETL (Extract, Transform, Load) pipeline by migrating and processing JSON data from the U.S. Federal Registry API.

📘 API Reference: Federal Register Developer Docs

# Features
 LangChain Integration
Smart document retrieval and contextual response generation.

# LLaMA 3 (8B) via Ollama
Efficient, locally hosted language model integration using llama3:8b.

# ETL Pipeline
JSON data from the Federal Register API is cleaned, processed, and stored into a MySQL database.

# SQL + Summarization Prompt Chaining
Dual prompt mechanism to generate SQL from natural language and then summarize the results.

# Gradio Interface
Clean and interactive web UI for seamless chatbot experience.

#⚙ Prerequisites
* Python 3.9+

* MySQL database (credentials stored in .env)

* Dependencies listed in requirements.txt:

* fastapi

* uvicorn

* langchain

* langchain-community

* langchain-core

* gradio

* python-dotenv

# 🛠️ Installation
# 1. Clone the repository
```bash
git clone https://github.com/jeevvanth/Customized_Chatbot.git
cd Customized_Chatbot
```

# 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

# 3. Install dependencies
```bash
pip install -r requirements.txt
```

# 🚦 Usage
▶️ Run the FastAPI Server
bash
Copy
Edit
cd chatbot
python main.py
📡 API Endpoints
POST /chat
Accepts a natural language query and returns a chatbot response.
Internally uses:

A SQL Prompt to extract query

A Summary Prompt to present user-friendly output

# 🖼️ Interface
Launch the Gradio-based web UI to interact with the chatbot in real-time.

# Docker ( Experimental)
A Dockerfile is included for containerization. However, MySQL integration inside Docker is not fully stable yet.

🛠️ Status: Under development — fix for MySQL Docker connectivity pending.

 To-Do / Improvements
Fix Docker-based MySQL connection

Add user authentication to the interface

Enhance prompt templates for more accurate SQL generation

Add support for batch queries and file uploads

Credits
This chatbot integrates:

LangChain

Ollama

Gradio

FastAPI

Contact
Built with  by Jeevanth Bheeman
Feel free to raise an issue or PR for improvements!

