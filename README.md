# Customized_Chatbot
Chatbot using Ollama ,Langchain , Gradio and FastApi

So This project implements the chatbot application with an help of FastApi, Ollama, Gradio and Langchain , as we know the purpose of each thing which i have used in this project to this chatbot successfully 

I have performed the data pipeline technique inorder to do the data migration from json to database and have taken the json from following website 

https://www.federalregister.gov/developers/documentation/api/v1#/Federal%20Register%20Documents/get_documents__format_ 
This is USA federal registry data API which contains executive documents and other registry related data.
You can see the ETL opertion on these data and for database i have used 

# Feature
   * LangChain integration for document retrieval and processing.
   * Invoking ollama with help of langchain framework.
   * model which have used is llama3:8b it is good and efficient
   * Database that high recommand was mysql and tried it was fine do etl
   * Used Gradio for interface for the application

# Prerequisites
  * Python 3.9+
  * mysql configuration credential are in .env file
  * Required python packages:FastApi,uvicorn,langchain-core,langchain,langchain-community,python-dotenv,gradio 

# Installation
 1.Clone the repository:
    git clone https://github.com/jeevvanth/Customized_Chatbot.git
                 cd Customized_Chatbot

  2. Create Virtual Environment:
     python -m venv venv
                 source venv/bin/activate
  3. For Installing Dependencies:
      pip install -r requirements.txt

# Usage
  1. Start the FastApi Server
     cd chatbot
             python main.py

  2. Available End points
      *Post (/chat):Questioning the chatbot where we are using two prompts one is for sqlprompt which extract the sql query from the model and gives to the                             summaryprompt of the same model.
        
# Try Not to Use
   So I have Containerized with the help of docker so in this i had a minor issue msql connection ie., I had problem in running mysql in the docker container So I future will rectify it 
  

