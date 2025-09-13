import os
from fastapi  import APIRouter, Form
from logger import logger
from modules.query_handler import query_chain
from modules.llm import get_llm_chain
from fastapi.responses import JSONResponse
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pinecone import Pinecone

router = APIRouter()

@router.post("/ask_question")
async def ask_question(question:str = Form(...)):
    try:
            
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

        #embddings
        embeddings = GoogleGenerativeAIEmbeddings(model = 'models/embedding-001')
        #initialize pinecone
        index_name = "medical-index"

        vectorstore  = PineconeVectorStore.from_existing_index(index_name=index_name,embedding=embeddings,text_key='text')

        retriever = vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})

        chain = get_llm_chain(retriever)
        result = query_chain(chain,question)

        logger.info('Question has been answered successfully')

        return result

    except Exception as e:
        logger.exception('Error while asking questions')
        return JSONResponse(status_code=500,content={"message": str(e)})


