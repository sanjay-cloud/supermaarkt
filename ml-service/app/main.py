from fastapi import FastAPI

from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from app.api.agent import router as agent_router

app = FastAPI()
app.include_router(agent_router)
from app.chatbot.retriever import Retriever
embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf", gpt4all_kwargs={'allow_download':'True'})
api_key = os.getenv('GEMINI_API_KEY')
retriever = Retriever(embeddings_model=embedding_model, 
                        db = Chroma(persist_directory = "data/db", embedding_function=embedding_model), llm_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", 
                google_api_key=api_key, temperature=0.3))

answer = "The store policy for handling stock includes several key procedures:\n\n*   **Storage Conditions:** Follow approved handling procedures for storage conditions. If these requirements are unknown, employees must ask the manager rather than guessing (Source 0)."+"\n*   **Problem Stock:**"+"\n*   Separate damaged or expired goods from saleable stock (Source 0)."+"\n*   Keep rejected goods separate from saleable stock (Source 3)."+"\n*   Report shortages, excess quantities, damaged goods, and incorrect products to the manager (Source 3)."+"\n*   **Stock Levels and Restocking:**"+"\n*   Inventory quantities and minimum stock levels must be obtained from the inventory system (Source 2)."+"\n*   Identify low stock and prepare restocking requests (Source 2)."+"\n*   No low-stock action is required if stock is greater than the minimum level (Source 1)."
@app.post("/ask")
def bot_ask(query : str, conversation_id : str):
    # return answer
    return retriever.generate_response(query, conversation_id).content