from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handler import catch_exception_handler
from routes.upload_pdf import router as upload_router
from routes.ask_question import router as ask_router
from routes.testing import router as test_router



app = FastAPI(title="Medical Assistant API",description="API for Medical Assistant Chatbot")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#middleware exception handler
app.middleware("http")(catch_exception_handler)

#routers
#1. upload pdfs
app.include_router(upload_router)
#2. chat with mi-medical assisstant.
app.include_router(ask_router)

app.include_router(test_router)


@app.get("/")
async def root():
    return {"message": "Basic server working!"}
