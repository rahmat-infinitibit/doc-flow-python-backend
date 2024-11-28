import chromadb
from chromadb.config import Settings
from app.config import CHROMA_PERSIST_DIR

class ChromaClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(allow_reset=True)
        )
        
    def get_or_create_collection(self, name: str):
        try:
            collection = self.client.get_collection(name)
        except:
            collection = self.client.create_collection(name)
        return collection 