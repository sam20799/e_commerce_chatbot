import streamlit as st
from faq import ingest_faq_data, faq_chain
from pathlib import Path
from router import r1
from sql import sql_chain


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

st.title("E Commerce Chatbot")

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