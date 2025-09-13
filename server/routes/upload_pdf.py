from fastapi import APIRouter,UploadFile,File
from logger import logger 
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from typing import List



router= APIRouter()

@router.post("/upload_pdfs")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info('Uploading PDF files')
        load_vectorstore(files)
        logger.info('PDF files has been uploaded successfully')
        return {"message":"PDF files has been uploaded successfully"}
    except Exception as e:
        logger.exception('Error in loading into Vector Database')
        return JSONResponse(status_code=500,content={"message": str(e)})