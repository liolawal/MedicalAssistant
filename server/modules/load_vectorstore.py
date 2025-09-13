import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_ENV="us-east-1"
index_name="medical-index"

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

UPLOAD_DIR="./uploaded_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)


# initialize pinecone instance
pc=Pinecone(api_key=PINECONE_API_KEY)
spec=ServerlessSpec(cloud="aws",region="us-east-1")
existing_indexes=[i["name"] for i in pc.list_indexes()]


if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=spec
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)


index=pc.Index(index_name)

# load,split,embed and upsert pdf docs content
def load_vectorstore(uploaded_files):
    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []

    for file in uploaded_files:
        new_path= Path(UPLOAD_DIR) / file.filename
        file_content = file.file.read()
        with open(new_path, "wb") as f:
            f.write(file_content)
        file_paths.append(str(new_path))

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        vectorstore = PineconeVectorStore.from_documents(
            embedding=embed_model,
            documents= chunks,
            ids = ids,
            index_name= index_name,
            text_key = 'text'
        )

        return vectorstore

        #print(f"🔍 Embedding {len(texts)} chunks...")
        #embeddings = embed_model.embed_documents(texts)

        #print("📤 Uploading to Pinecone...")
        #with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            #index.upsert(vectors=zip(ids, embeddings, metadatas))
            #progress.update(len(embeddings))

        print(f"✅ Upload complete for {file_path}")