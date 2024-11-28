from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from app.database.chroma_client import ChromaClient
from typing import List, Tuple

class ChatService:
    def __init__(self):
        self.chroma_client = ChromaClient()
        self.collection = self.chroma_client.get_or_create_collection("documents")
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0)
        
    async def get_response(self, message: str) -> Tuple[str, List[str]]:
        # Search relevant documents
        results = self.collection.query(
            query_texts=[message],
            n_results=3,
            include=["documents", "metadatas"]
        )
        
        # Extract references
        references = []
        for metadata in results["metadatas"][0]:
            if metadata["source"] not in references:
                references.append(metadata["source"])
        
        # Generate response using context
        context = "\n".join(results["documents"][0])
        prompt = f"""Based on the following context, answer the user's question. 
        If the answer cannot be found in the context, say so.
        
        Context: {context}
        
        Question: {message}"""
        
        response = self.llm.predict(prompt)
        
        return response, references 