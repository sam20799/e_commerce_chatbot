from pathlib import Path
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()
faq_path = Path(__file__).parent / "resources/faq_data.csv"
chroma_client = chromadb.Client()
collection_name_faq = "faqs"
groq_client = Groq()


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

def faq_chain(query):
    result = get_relevant_qa(query)
    context = " ".join([r.get('answer') for r in  result['metadatas'][0]])
    answer = generate_answer(query,context)
    return answer


def generate_answer(query,context):
    prompt = f'''You are a helpful customer support assistant.
    
    Using ONLY the information in the context below, answer the question
    in a clear, friendly, and human-like way.
    
    Guidelines:
    - Use complete sentences
    - You may rephrase and explain
    - Do NOT add new facts
    - If the answer is not in the context, say: "I don't know."
    Question:{query}
    Context:{context}
    '''

    #calling llm
    completion = groq_client.chat.completions.create(#type: ignore
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_completion_tokens=1024,
        top_p=0.9,
        stream=False,
    )
    return completion.choices[0].message.content



if __name__ == "__main__":
    ingest_faq_data(faq_path)
    query = "what's your policy on defective products? "
    # result = get_relevant_qa(query)
    # print(result)
    answer = faq_chain(query)
    print(answer)



