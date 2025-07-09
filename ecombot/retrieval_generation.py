import os
from dotenv import load_dotenv
import google.generativeai as genai

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

from ecombot.ingest import ingestdata

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Make sure API key is configured correctly
genai.configure(api_key=GOOGLE_API_KEY)

def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    You are an e-commerce assistant with expertise in recommending products and answering customer queries.
    You analyze product titles and reviews to offer helpful, concise, and relevant suggestions.

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    # ✅ Use a supported Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # You can also try gemini-1.5-pro-latest
        temperature=0.7
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

if __name__ == '__main__':
    # ✅ Unpack vectorstore
    vstore, *_ = ingestdata("done")

    chain = generation(vstore)

    
    print(chain.invoke("can you tell me the best bluetooth buds?"))
