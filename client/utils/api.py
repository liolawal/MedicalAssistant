import requests
from config import API_URL



def upload_pdf_api(files):
    file_loads = [("files",(f.name,f.read(),"application/pdf"))for f in files]
    return requests.post(f"{API_URL}/upload_pdfs",files=file_loads)
    


def ask_question(question):
    return requests.post(f"{API_URL}/ask_question", data={'question':question})