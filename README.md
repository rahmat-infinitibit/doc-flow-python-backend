# RAG System with ChromaDB

A powerful RAG (Retrieval-Augmented Generation) system backend that processes PDFs containing text, images, diagrams, and mathematical content. The system allows users to upload documents and chat with them using natural language queries.

## Features

- PDF document processing (text, images, diagrams, math)
- Vector storage using ChromaDB
- Natural language querying
- Reference tracking for responses
- REST API interface
- Chat API and history features
- Database initialization

## Technology Stack

### Core Dependencies

1. **FastAPI (0.104.1)**
   - High-performance web framework for building APIs
   - Automatic API documentation
   - Modern Python type hints support

2. **Uvicorn (0.24.0)**
   - ASGI server implementation
   - Required to run FastAPI applications
   - Supports hot reloading during development

3. **LangChain (0.0.350)**
   - Framework for developing LLM applications
   - Provides document loading and processing capabilities
   - Handles text splitting and embedding generation

4. **ChromaDB (0.4.22)**
   - Vector database for storing document embeddings
   - Efficient similarity search
   - Persistent storage support

5. **CrewAI (0.11.0)**
   - AI agent framework for specialized content processing
   - Handles complex document understanding tasks
   - Supports multi-agent collaboration

### Document Processing

6. **PyPDF (3.17.1)**
   - PDF processing library
   - Extracts text and metadata from PDFs

7. **Unstructured (0.10.30)**
   - Advanced document processing
   - Handles various document formats
   - Extracts text from images and diagrams

8. **OpenAI (1.3.7)**
   - Provides embedding generation
   - Powers the chat completion functionality

### Utilities

9. **Python-Multipart (0.0.6)**
   - Handles file uploads in FastAPI
   - Processes form data

10. **Python-Dotenv (1.0.0)**
    - Loads environment variables
    - Manages configuration securely

11. **Matplotlib (3.8.2)**
    - Handles mathematical plots and diagrams
    - Supports image processing

12. **Python-Magic (0.4.27)**
    - File type detection
    - Ensures proper file handling

## Common Setup Issues

### PowerShell Virtual Environment Activation Error

If you encounter this error when activating the virtual environment in PowerShell:
```powershell
.\venv\Scripts\activate : File [...]\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

Fix it by:
1. Open PowerShell as Administrator
2. Run: `Set-ExecutionPolicy RemoteSigned`
3. Confirm with 'Y' when prompted
4. Try activating the virtual environment again: `.\venv\Scripts\activate`

### ChromaDB Import Error

If you see: `Import "chromadb.config" could not be resolved`, ensure ChromaDB is properly installed:
```bash
# Install ChromaDB
pip install chromadb

# Or upgrade to latest version if already installed
pip install --upgrade chromadb
```

## Project Structure

```
rag_backend/
├── .env 
```

## Setup and Running the Application

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application
```bash
# Make sure you're in the project root directory
python -m uvicorn app.main:app --reload --port 8000
```

The API will be running at: `http://localhost:8000`
API Documentation will be available at: `http://localhost:8000/docs`

## Testing with Postman

### 1. Upload Document API
**Endpoint**: `POST http://localhost:8000/documents/upload`

Setup in Postman:
1. Create new request
2. Set method to `POST`
3. Enter URL: `http://localhost:8000/documents/upload`
4. In the "Body" tab:
   - Select "form-data"
   - Add key: `file` (Type: File)
   - Click "Select Files" and choose your PDF

Example Response:
```json
{
    "message": "Document processed successfully",
    "document_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Chat API
**Endpoint**: `POST http://localhost:8000/chat/chat`

Setup in Postman:
1. Create new request
2. Set method to `POST`
3. Enter URL: `http://localhost:8000/chat/chat`
4. In the "Headers" tab:
   - Add: `Content-Type: application/json`
5. In the "Body" tab:
   - Select "raw"
   - Select "JSON"
   - Enter your query:
```json
{
    "message": "What are the main points discussed in the document?"
}
```

Example Response:
```json
{
    "response": "Based on the document, the main points discussed are...",
    "references": [
        "path/to/your/uploaded/document.pdf"
    ]
}
```

## Chat API and History Features

### Initialize Database
Before using the chat features, you need to initialize the database:
```bash
# Navigate to the project directory
cd python-backend

# Initialize the database
python -m app.database.init_db
```

### Chat API Endpoints

1. Start a New Chat
```http
POST /chat
Content-Type: application/json

{
    "message": "Your message here",
    "title": "Optional chat title"  // Optional
}

Response:
{
    "response": "Assistant's response",
    "references": ["reference1", "reference2"],
    "chat_id": "unique-chat-id"
}
```

2. Continue Existing Chat
```http
POST /chat
Content-Type: application/json

{
    "message": "Your follow-up message",
    "chat_id": "previous-chat-id"
}
```

3. View Chat History
```http
GET /chat/history

Response:
[
    {
        "chat_id": "unique-chat-id",
        "title": "Chat Title",
        "last_message": "Last message in the chat",
        "timestamp": "2024-01-01T12:00:00"
    }
]
```

4. View Messages from Specific Chat
```http
GET /chat/{chat_id}/messages

Response:
[
    {
        "role": "user",
        "content": "User message",
        "timestamp": "2024-01-01T12:00:00"
    },
    {
        "role": "assistant",
        "content": "Assistant response",
        "timestamp": "2024-01-01T12:00:01"
    }
]
```

### Features
- Persistent chat history across sessions
- Unique chat IDs for conversation tracking
- Optional chat titles for better organization
- Timestamp tracking for all messages
- Role-based message storage (user/assistant)
- References tracking for responses

## Testing Flow Example

1. **First, upload a document**:
   ```
   POST http://localhost:8000/documents/upload
   Body (form-data):
   file: sample.pdf
   ```

2. **Then, chat with the uploaded document**:
   ```
   POST http://localhost:8000/chat/chat
   Body (raw JSON):
   {
       "message": "What is this document about?"
   }
   ```

3. **Ask specific questions**:
   ```
   POST http://localhost:8000/chat/chat
   Body (raw JSON):
   {
       "message": "What does the document say about [specific topic]?"
   }
   ```

## Sample Test Files

For testing, try uploading these types of PDFs:
1. Text-heavy documents (e.g., research papers)
2. Documents with images and diagrams
3. Technical documents with mathematical formulas
4. Mixed content documents

## Troubleshooting Common API Issues

### Upload API Issues

1. **File Upload Fails**
   - Check if file is PDF format
   - Ensure file size is reasonable (< 10MB recommended)
   - Verify form-data key is exactly "file"

2. **Processing Error**
   - Check if PDF is corrupted
   - Ensure PDF is not password protected
   - Verify OpenAI API key is valid

### Chat API Issues

1. **No Response**
   - Verify document was successfully uploaded first
   - Check if query is clear and specific
   - Ensure OpenAI API key has sufficient credits

2. **Empty References**
   - Confirm document was properly processed
   - Try uploading document again
   - Check ChromaDB persistence directory exists

## API Response Codes

- `200`: Successful operation
- `400`: Bad request (invalid input)
- `422`: Validation error
- `500`: Server error

## Monitoring

- Check the terminal running the server for logs
- API documentation at `/docs` shows real-time request/response examples
- ChromaDB stores data in `./chroma_db` directory

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Installation Guidelines

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (venv)

### Common Installation Issues and Solutions

1. **Dependency Conflicts**
   ```bash
   # If you see conflicts between openai and langchain-openai:
   pip uninstall openai langchain-openai
   pip install "openai>=1.6.1,<2.0.0"
   pip install langchain-openai==0.0.2
   ```

2. **PDF Processing Dependencies**
   
   On Windows:
   ```bash
   # Install Poppler for PDF processing
   # Option 1: Using chocolatey
   choco install poppler

   # Option 2: Manual installation
   # Download from: http://blog.alivate.com.au/poppler-windows/
   # Add the bin folder to your PATH
   ```

   On Ubuntu/Debian:
   ```bash
   sudo apt-get update
   sudo apt-get install -y poppler-utils
   ```

   On MacOS:
   ```bash
   brew install poppler
   ```

3. **ChromaDB Installation Issues**
   ```bash
   # If ChromaDB fails to install:
   pip uninstall chromadb
   pip install chromadb==0.4.22 --no-cache-dir
   ```

4. **Virtual Environment Issues**

   If you encounter issues with the virtual environment:
   ```bash
   # Remove existing environment
   # Windows:
   deactivate
   rm -r venv
   # Unix/MacOS:
   deactivate
   rm -rf venv

   # Create fresh environment
   python -m venv venv

   # Activate environment
   # Windows:
   .\venv\Scripts\activate
   # Unix/MacOS:
   source venv/bin/activate

   # Upgrade pip
   python -m pip install --upgrade pip

   # Install requirements
   pip install -r requirements.txt
   ```

5. **Windows-Specific Issues**

   If you get "running scripts is disabled" error:
   ```powershell
   # Run PowerShell as Administrator and execute:
   Set-ExecutionPolicy RemoteSigned
   # Confirm with 'Y' when prompted
   ```

6. **Permission Issues**
   
   If you encounter permission errors:
   ```bash
   # Windows (Run as Administrator):
   pip install --user -r requirements.txt

   # Unix/MacOS:
   sudo pip install -r requirements.txt
   ```

### Post-Installation Verification

1. **Verify Dependencies**
   ```bash
   pip list
   ```

2. **Test PDF Processing**
   ```bash
   # Create a test directory
   mkdir test_files
   
   # Try processing a simple PDF
   curl -o test_files/test.pdf https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
   ```

3. **Verify ChromaDB**
   ```python
   # In Python interpreter
   import chromadb
   client = chromadb.PersistentClient()
   # Should create ./chroma_db directory
   ```

### Directory Structure After Installation

```
rag_backend/
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
├── venv/                # Virtual environment
├── chroma_db/           # ChromaDB storage
└── app/                 # Application code