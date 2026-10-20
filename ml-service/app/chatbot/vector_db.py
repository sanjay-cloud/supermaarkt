from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
import utils.json_utils as json_utils
class Vector_DB:
    def __init__(self, embeddings_model = None, vector_db = None, data_path = None, db_path = None):
        self.embeddings_model =  embeddings_model
        self.data_path = data_path
        self.db_path = db_path
        self.vector_db = vector_db


    def load_documents(self, chunk_file):
        chunk_json = json_utils.load_json(chunk_file)
        text_list = []
        metadata_list=[]
        ids = []
        for chunks in chunk_json:
            for chunk in chunks["chunks"]:
                text_list.append(chunk["text"])
                metadata_list.append({
                    "id":chunk["id"],
                    "filename":chunks["filename"],
                    "page":chunk["page"]
                })     
                ids.append(chunks["filename"]+":"+str(chunk["id"])) 
        return text_list, metadata_list, ids

    def save_to_chroma(self, chunks_list: list[str], metadata_list : list[object], ids : list[str]):
        self.vector_db.from_texts(chunks_list, self.embeddings_model, persist_directory=self.db_path, metadatas = metadata_list, ids = ids)



    def create_vector_db(self):
        texts_list, metadata_list, ids = self.load_documents(self.data_path)
        self.save_to_chroma(texts_list, metadata_list, ids)
    


if __name__ == "__main__":
    embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf", gpt4all_kwargs={'allow_download':'True'})
    vector = Vector_DB(embeddings_model=embedding_model, vector_db= Chroma(),data_path="data/chunks/chunks.json", db_path="data/db")
    vector.create_vector_db()