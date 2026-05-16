from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

import os

from pdf_utils import extract_text_from_pdf
from qa_engine import (
    store_document,
    answer_question
)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# -----------------------------------
# Upload PDF
# -----------------------------------

@app.post("/upload")

async def upload_pdf(
    file: UploadFile = File(...)
):

    try:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as f:

            f.write(await file.read())

        pdf_text = extract_text_from_pdf(
            file_path
        )

        if not pdf_text.strip():

            return {
                "message": "No text found in PDF"
            }

        store_document(pdf_text)

        return {
            "message": "PDF uploaded successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# -----------------------------------
# Ask Question
# -----------------------------------

@app.post("/ask")

async def ask_question_api(
    question: str = Form(...)
):

    try:

        answer = answer_question(question)

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }
