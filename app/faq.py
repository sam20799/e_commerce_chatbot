from pathlib import Path
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

faq_path = Path(__file__).parent / "resources/faq_data.csv"
chroma_client = chromadb.Client()
collection_name_faq = "faqs"

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def ingest_faq_data(path):
   if collection_name_faq not in  [c.name for c in chroma_client.list_collections()]:
        #initializing vector database
        print("Ingesting FAQ data into Chroma Database")
        collection = chroma_client.get_or_create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )

        # convert data into df so that we can insert it into database
        df = pd.read_csv(path)

        #insert data into vector database
        docs = df['question'].tolist()
        metadata = [{'answer': ans} for ans in df['answer'].tolist()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
        print(f"FAQ data successfully ingested in {collection_name_faq} chroma collection")
   else:
        print(f"{collection_name_faq} already exists.")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(name=collection_name_faq)
    result = collection.query(
        query_texts = query,
        n_results=2
    )
    return result


if __name__ == "__main__":
    ingest_faq_data(faq_path)
    query = "what's your policy on defective products? "
    ans = get_relevant_qa(query)
    print(ans)