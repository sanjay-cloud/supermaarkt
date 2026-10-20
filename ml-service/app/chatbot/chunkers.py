import spacy
from sklearn.cluster import KMeans
import numpy as np
from pathlib import Path
import json
import utils.file_utils as file_utils
import utils.json_utils as json_utils
import pypdf

class Chunkers:
    def __init__(self, input_folder, output_folder, output_format = ".json", chunking_type = None, embedding_model = None, num_clusters = 3):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.output_format = output_format
        self.embedding_model = embedding_model
        self.num_clusters = num_clusters
        self.supported_formats = [".pdf"]
        self.chunking_type = self.fixed_chunking  
        file_utils.create_dir(self.output_folder)

    def start(self):
        chunk_data = []
        folder = Path(self.input_folder)
        for file_path in folder.iterdir():
            data = {}
            if file_path.is_file() and Path(file_path).suffix in self.supported_formats:
                file_name = file_path.name
                text_list = self.getPdfText(file_path)
                chunk_list = self.chunking_type(text_list=text_list)
                data["filename"] = file_name
                data["chunks"] = chunk_list
                chunk_data.append(data) 
        json_utils.save_json(json_file=Path(self.output_folder)/"chunks.json", json_data=chunk_data)   
    

    def fixed_chunking(self, text_list, chunk_size = 25):  
        chunks = []
        chunk_id = 0
        for page, text in enumerate(text_list):  
            for i in range(0, len(text), chunk_size):
                chunks.append(              
                    {"id" : chunk_id,
                    "text" : " ".join(text[i : i+chunk_size]),
                    "page" : page+1} 
                )
                chunk_id+=1
        print(chunks)    
        return chunks
    def getPdfText(self, filepath):
        reader = pypdf.PdfReader(filepath)
        text_list = []
        for id, page in enumerate(reader.pages):
            print(f"page numbe {id}")
            text_list.append(page.extract_text().encode("ascii", errors="ignore").decode("ascii").split())
        return text_list


    def sentence_chunking(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.text)
        return [sent.text for sent in doc.sents]
  

if __name__ == "__main__":
    chunker = Chunkers(input_folder="data/documents", output_folder="data/chunks")
    chunker.start()