# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import base64
# import os
# from pathlib import Path

# app = FastAPI()

# # Allow all CORS (for local testing)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Directory to save uploaded files
# UPLOAD_DIR = "uploads"
# Path(UPLOAD_DIR).mkdir(exist_ok=True)

# # Request model
# class FileUploadRequest(BaseModel):
#     filename: str
#     content_type: str
#     base64_file: str

# @app.post("/summarizer")
# async def upload_base64(file_data: FileUploadRequest):
#     try:
#         print(file_data.filename)
#         file_path = os.path.join(UPLOAD_DIR, file_data.filename)

#         # Decode and save file
#         with open(file_path, "wb") as f:
#             f.write(base64.b64decode(file_data.base64_file))

#         # Simulate processing
#         extracted_text = f"Saved file: {file_path}\nContent-Type: {file_data.content_type}\n"
#         extracted_text += f"(First 100 bytes shown)\n\n"
#         with open(file_path, "rb") as f:
#             extracted_text += repr(f.read(100))

#         return {"text": extracted_text}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


############################################

from fastapi import FastAPI, Request,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
import uuid
import os
from dotenv import load_dotenv
from process import Response

load_dotenv()

os.makedirs("/tmp/huggingface_cache", exist_ok=True)
os.environ["HF_HOME"] = "/tmp/huggingface_cache"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated storage
uploaded_docs = {}

class UploadRequest(BaseModel):
    filename: str
    filedata: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatBot(BaseModel):
    text :str
    token:str

def verify_token(token: str):
    if token != os.getenv("VERIFICATION_TOKEN"):
        raise HTTPException(status_code=401, detail="Token not matched")
    return True

@app.get("/")
async def home():
    return {"message": "Test OK..."}

@app.post("/chatbot")
async def chatbot(req:ChatBot):
    query = req.text
    token = req.token
    if not query or not token:
        raise HTTPException(status_code=400, detail="No text provided")
    verify_token(token=token)
    res = Response().chatbot(query=query)
    return {"result":res}


@app.post("/upload")
async def upload_file(req: UploadRequest):
    session_id = str(uuid.uuid4())
    decoded_data = base64.b64decode(req.filedata)
    # Save to disk or memory (or pass to RAG pipeline)
    uploaded_docs[session_id] = decoded_data
    print(session_id)
    return {"success": True, "session_id": session_id}

@app.post("/chat")
async def chat(req: ChatRequest):
    pdf_data = uploaded_docs.get(req.session_id)
    if not pdf_data:
        return {"reply": "Session not found."}

    # TODO: RAG logic here (e.g., extract text, run through embedding + LLM)
    dummy_answer = f" Nice Mocked answer for: '{req.message}'"
    return {"reply": dummy_answer}
