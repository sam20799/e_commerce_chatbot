import streamlit as st
from faq import ingest_faq_data, faq_chain
from pathlib import Path
from router import r1
from sql import sql_chain

st.title("🛒 QueryCart — GenAI E-Commerce Chatbot")
st.caption("Ask natural language questions to discover products and get data-grounded answers")

with st.expander("🧠 What does this app do?"):
    st.markdown(
        """
        **QueryCart** is a GenAI-powered e-commerce chatbot that helps you **search products and get answers to product-related questions** using natural language.

        The app combines **LLMs, SQL, and Retrieval-Augmented Generation (RAG)** to ensure responses are **accurate, structured, and grounded in data**.

        **How it works:**
        1. You ask a product-related question (e.g., *“Show me Nike shoes with rating above 4.5”*)
        2. The app identifies whether the query is a **product search** or an **FAQ**
        3. For product searches, the LLM converts the query into **SQL**
        4. For FAQs, relevant information is retrieved using **RAG**
        5. The final response is generated **only from retrieved data**
        """
    )

with st.expander("🗄️ Data source & limitations"):
    st.markdown(
        """
        The product data consists of **publicly available women’s footwear listings.

        ✅ **What works well**
        - Filtering products by brand, price, rating, discount, and reviews
        - Natural language queries mapped to structured SQL
        - Data-grounded answers without hallucinations

        ⚠️ **Limitations**
        - Data is **static** (not real-time or live inventory)
        - Some queries may require more specific filters for best results

        💡 **Tip:**  
        Ask specific questions like *“Top 3 Puma shoes under ₹3000 with rating above 4.5”* for optimal results.
        """
    )


faq_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faq_path)

def ask(query):
    route = r1(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    else:
        return "Route not found"

# st.title("E Commerce Chatbot")

query = st.chat_input("write your query")

if "messages" not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state['messages'].append({"role": "user","content":query})
    response = ask(query)
    response = response.replace("\n", "<br>")
    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)
    st.session_state['messages'].append({"role":"assistant","content":response})