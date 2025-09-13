from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI



from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

os.environ['DEEPSEEK_API_KEY'] = DEEPSEEK_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
 

def get_llm_chain(retriever):
    llm = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.5-flash", temperature=0)
                    

    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
                    template="""You are **MediBot**, an AI-powered assistant trained to help users understand medical documents and health-related questions.

            Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

            ---

            🔍 **Context**:
            {context}

            🙋‍♂️ **User Question**:
            {question}

            ---

            💬 **Answer**:
            - Respond in a calm, factual, and respectful tone.
            - Use simple explanations when needed.
            - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
            - Do NOT make up facts.
            - Do NOT give medical advice or diagnoses.
            """ )
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_prompt}
    )

    return chain
    