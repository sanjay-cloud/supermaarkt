from app.chatbot.retriever import Retriever
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_chroma import Chroma
embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf", gpt4all_kwargs={'allow_download':'True'})
retriever = Retriever(embeddings_model=embedding_model, 
                        db = Chroma(persist_directory = "data/db", embedding_function=embedding_model))
def retrieve_matching_doc(query : str):
    
    response  = retriever.retrieve_match(query)
    matches = []
    for id,result in enumerate(response):
        match = {}
        match["id"] = id
        match["filename"] = result[0].metadata["filename"]
        match["page"] = result[0].metadata["page"]
        match["content"] = result[0].page_content

        matches.append(match)
    return matches


retrieve_matching_doc_function = {
    "type": "function",
    "name": "retrieve_matching_doc",
    "description": "Search supermarket policies and procedures, including restocking and stock discrepancies. Returns relevant passages with filenames and page numbers. Does not provide live inventory quantities.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "query to search"},
        },
        "required": ["query"],
    },
}

