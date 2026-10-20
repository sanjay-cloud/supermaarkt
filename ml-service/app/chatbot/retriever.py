
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv()

class Retriever:
    def __init__(self, embeddings_model = None, db = None, db_path = None, llm_model = None):
        self.embeddings_model = embeddings_model 
        self.db_path = db_path    
        self.db = db
        self.llm_model = llm_model
        self.conversation_histories = {}
        self.chat_history_message = "Rewrite the current question so it can be understood without the conversation history. " \
        "Use history only to resolve references. If already standalone, return it unchanged. Do not answer the question or add facts. " \
        "Output only the rewritten question."
    
    def retrieve_match(self, query):
        return self.db.similarity_search_with_score(query)


    # def retrieve_match(self, query):
    #     response = self.db.similarity_search_with_score(query)
    #     match = ""
    #     for id,result in enumerate(response):
    #         filename = result[0].metadata["filename"]
    #         page = result[0].metadata["page"]
    #         match += f"\n source {id}: {filename}, page {page} \n {result[0].page_content}"
    #     return match    

    def generate_response(self, og_query, conversation_id):
        current_session = {}
        if conversation_id in self.conversation_histories:
            query = self.reframe_query(og_query, conversation_id)            
            match = self.retrieve_match(query)
            query = self.build_query(match, query) 
        else:    
            match = self.retrieve_match(og_query)
            query = self.build_query(match, og_query)    
        response = self.llm_model.invoke(query)        
        current_session[og_query] = response.content     
        self.conversation_histories.setdefault(conversation_id, []).append(current_session)
        print(response.content)
        return response

    def build_query(self, match, query):
        query = "Question: "+query
        for id,result in enumerate(match):
            filename = result[0].metadata["filename"]
            page = result[0].metadata["page"]
            query += f"\n source {id}: {filename}, page {page} \n {result[0].page_content}"
        return query
    
    def reframe_query(self, query, conversation_id):
        history = "Conversation history:"
        chat_history = self.conversation_histories.get(conversation_id)
        for session in chat_history:
            key, value = next(iter(session.items()))
            history+= f"\nquestion:{key} \nanswer:{value}"
        query = f"{history}\nCurrent Question:\n{query}"
        messages = [
            SystemMessage(content=self.chat_history_message), 
            HumanMessage(content=query),
        ] 
        reframed_query = self.llm_model.invoke(messages).content
        print(f"reframed query: {reframed_query}")
        return reframed_query



if __name__ == "__main__":
    embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf", gpt4all_kwargs={'allow_download':'True'})
    api_key = os.getenv('GEMINI_API_KEY')
    retriever = Retriever(embeddings_model=embedding_model, 
                          db = Chroma(persist_directory = "data/db", embedding_function=embedding_model), llm_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", 
                    google_api_key=api_key, temperature=0.3))
    while True:
        print("Enter your query:")
        query = input()
        retriever.generate_response(query, "111")
    