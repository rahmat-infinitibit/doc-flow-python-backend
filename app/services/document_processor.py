from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from app.database.chroma_client import ChromaClient
import uuid
from fastapi import HTTPException
import logging
import pypdf
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.chroma_client = ChromaClient()
        self.embeddings = OpenAIEmbeddings()
        self.collection = self.chroma_client.get_or_create_collection("documents")
        
    async def process_document(self, file_path: str):
        try:
            # Verify PDF is valid
            try:
                with open(file_path, 'rb') as file:
                    pypdf.PdfReader(file)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid or corrupted PDF file: {str(e)}"
                )

            # Load PDF using PyPDFLoader instead of UnstructuredPDFLoader
            logger.info(f"Loading PDF from {file_path}")
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            if not documents:
                raise HTTPException(
                    status_code=400,
                    detail="No content could be extracted from the PDF"
                )
            
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            splits = text_splitter.split_documents(documents)
            
            if not splits:
                raise HTTPException(
                    status_code=400,
                    detail="Could not split document content meaningfully"
                )
            
            # Generate unique document ID
            doc_id = str(uuid.uuid4())
            
            # Process and store chunks
            for i, split in enumerate(splits):
                chunk_id = f"{doc_id}_{i}"
                try:
                    self.collection.add(
                        ids=[chunk_id],
                        documents=[split.page_content],
                        metadatas=[{
                            "source": os.path.basename(file_path),  # Store just filename
                            "doc_id": doc_id,
                            "page": split.metadata.get("page", 0),
                            "chunk": i
                        }]
                    )
                except Exception as e:
                    logger.error(f"Error adding chunk {i} to collection: {str(e)}")
                    continue
            
            logger.info(f"Successfully processed document with ID: {doc_id}")
            return doc_id
            
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing document: {str(e)}"
            )