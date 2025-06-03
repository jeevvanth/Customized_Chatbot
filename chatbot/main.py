from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from uvicorn import run
import pymysql
import json
from config import password,hostname,username,database
from datetime import date, datetime
import os


# host = os.getenv("HOST", "127.0.0.1")
connection = pymysql.connect(host=hostname,
                             port=3306,
                             user=username,
                             password=password,
                             database=database)

app=FastAPI()

cursor = connection.cursor()

class UserInput(BaseModel):
    question:str

schema_prompt=f"""
Database schema:
- notices(document_number, title,type,abstract,html_url,pdf_url,public_inspection_pdf_url,publication_date,excerpts)
-agencies(id,document_number,raw_name,name,url,json_url,parent_id,slug)
"""

llm=Ollama(model="llama3:8b")

sql_prompt=PromptTemplate(input_variables=["schema","question"],
                          template="""
You are an expert SQL assistant. Use the database schema below to write a SQL query that answers the question.
Respond only with JSON like: {{ "sql": "<SQL_QUERY>" }}

Schema:
{schema}

Question:
{question}
"""
)

sql_chain=LLMChain(llm=llm,prompt=sql_prompt)

summary_prompt=PromptTemplate(input_variables=["schema","question"],
                              template="""    
You are a helpful assistant. Based on the question and the SQL query result, return a clear,readable summary by you.

Question: {question}
Results: {result_json}

Answer:
                              
""")

summary_chain=LLMChain(llm=llm,prompt=summary_prompt)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}



@app.post("/chat")
async def chat(user_input: UserInput):  # Let FastAPI parse the request
    try:
        sql_response=dict()

        question = user_input.question  # Access the field correctly

        sql_response = sql_chain.invoke({
            "schema": schema_prompt,
            "question": question,
        })
        print("Raw SQL query:",sql_response)

        # Parse SQL response
        try:

            if isinstance(sql_response, dict) and "text" in sql_response:
                sql_text = sql_response["text"].strip()

                # Check if the text is a JSON string (e.g., '{"sql": "SELECT ..."}')
                if sql_text.startswith("{") and sql_text.endswith("}"):
                    sql_dict = json.loads(sql_text)  # Parse JSON
                    sql_query = sql_dict["sql"]
                else:
                    # Assume the response is already the SQL query
                    sql_query = sql_text
            else:
                raise ValueError("Unexpected SQL response format")

            print("Final SQL Query:", sql_query)  # Debug

            # Execute SQL
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]
            print("Final SQL Results:", results)

            def json_serializer(obj):
                if isinstance(obj, (date, datetime)):
                    return obj.isoformat()  # Convert to ISO-format string (e.g., "2023-12-31")
                raise TypeError(f"Type {type(obj)} not serializable")

            # Generate summary
            summary_response = summary_chain.invoke({
                "question": question,
                "result_json": json.dumps(results, indent=2,default=json_serializer),
            })
            print("Summary Result:", summary_response["result_json"])

            return {"summary": summary_response["result_json"]}

        except Exception as ex:
            raise HTTPException(status_code=400, detail=f"Errors: {str(ex)}")

    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Exception: {str(ex)}")




# async def chat(request: UserInput):
#     question=request.question
#
#     sql_response=sql_chain.invoke({
#         "schema":schema_prompt,
#         "question":question,
#     })
#
#     try:
#        sql_dict=json.loads(sql_response)
#        sql_query=sql_dict["sql"]
#
#     except Exception as ex:
#         raise HTTPException(status_code=400,detail=f"Failed parsing SQL response Json:{ex}")
#
#     try:
#         cursor.execute(sql_query)
#         rows=cursor.fetchall()
#         columns=[desc[0] for desc in cursor.description]
#         results=[dict(zip(columns,row)) for row in rows]
#
#     except Exception as ex:
#         raise HTTPException(status_code=400,detail=f"SQL query failed: {ex}")
#
#     summary_response=summary_chain.invoke({
#         "question":question,
#         "result_json":json.dumps(results,indent=2),
#     })
#
#     return summary_response

if __name__ == "__main__":
    run(app,host="127.0.0.1", port=8000, reload=False)


