from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
from ecombot.data_converter import dataconveter

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

def ingestdata(status):
    vstore = AstraDBVectorStore(
        embedding=embedding,
        collection_name="chatbotecomm",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )

    storage = status

    if storage is None:
       docs = dataconveter()
       print(f"Docs to insert: {len(docs)}")
       inserted_ids = []
       BATCH_SIZE = 500  # You can adjust this number
       for i in range(0, len(docs), BATCH_SIZE):
           batch = docs[i:i+BATCH_SIZE]
           try:
               batch_ids = vstore.add_documents(batch)
               inserted_ids.extend(batch_ids)
               print(f"Inserted batch {i//BATCH_SIZE + 1}: {len(batch_ids)} docs")
           except Exception as e:
            print(f"Error inserting batch {i//BATCH_SIZE + 1}:", e)
       return vstore, inserted_ids
    else:
       return vstore, []

if __name__ == '__main__':
    vstore, inserted_ids = ingestdata(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound basshead.")
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")
            

   