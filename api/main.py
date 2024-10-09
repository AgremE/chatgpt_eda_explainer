from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# Initialize FastAPI app
app = FastAPI(title="EDA Helper with ChatGPT", description="Backend for generating Python scripts for data visualization and EDA using natural language queries.")

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request model for incoming data from user
class RequestData(BaseModel):
    query: str

# Response model for generated Python code
class ResponseData(BaseModel):
    python_code: str

# Define the endpoint for generating Python code
@app.post("/generate_code", response_model=ResponseData)
async def generate_code(request: RequestData):
    try:
        # Generate a response from ChatGPT for the provided query
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can adjust this model name if needed
            messages=[
                {"role": "user", "content": request.query}
            ]
        )
        # Extract the Python code from the response
        generated_code = response.choices[0].message["content"].strip()
        
        return ResponseData(python_code=generated_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health_check")
async def health_check():
    return {"status": "OK"}

# Example usage: Health check route
@app.get("/")
async def root():
    return {"message": "Welcome to EDA Helper with ChatGPT!"}

# To run the FastAPI server, use:
# uvicorn <filename>:app --reload
# Replace <filename> with the actual name of the file.

# FastAPI makes it easy to create interactive API docs via OpenAPI at /docs