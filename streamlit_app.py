import streamlit as st
import pandas as pd
import numpy as np
import base64

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.agents import create_csv_agent
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(layout="wide", page_title="Spcae bot",
                   page_icon="🚀", theme='dark')
st.title("Space bot 🚀")


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


background_image = 'background.jpg'
base64_image = get_base64_of_bin_file(background_image)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/jpeg;base64,{base64_image}");
background-size: cover;
background-position: center;
background-attachment: fixed;
color: white;
}}

[data-testid="stHeader"] {{
    background: rgba(0, 0, 0, 0);  /* Transparent header */
}}

[data-testid="stSidebar"] {{
    background-color: #333333;  /* Dark sidebar */
}}

p {{
    color: white;  /* Text color */
    font-size: 15px;
    font-family: Arial, sans-serif;
}}
</style>
"""


st.markdown(page_bg_img, unsafe_allow_html=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


@st.cache_data
def load_data():
    return pd.read_csv("exoplanets_cleaned.csv")


loader = CSVLoader('exoplanets_cleaned.csv')
documents = loader.load()
# Create embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.load_local(
    "exoplanets_vectorstore", embeddings=embeddings, allow_dangerous_deserialization=True)


@st.cache_resource
def get_response(query, _chat_history):

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# Create a retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    # Create a prompt template for follow-up
    followup_prompt = ChatPromptTemplate.from_template(
        """
                You are a Space bot specializing in exoplanet discovery.
                You know some exoplanets' features and you can answer questions about them.
                Your main role is to help people understand exoplanets and make them curious about space exploration.
                Your language is as simple and clear as possible.
                You can speak mutliple languages and you can translate between them.
                You can add some scientific terms to support your response.
                Based on the features, you can know if this exoplanet is habitable.
                You learn from the conversation and you can use this knowledge in the future.
                You are friendly and want to know people and remember their names and you are trying to help people to understand exoplanets.
                Try to be more concise in your responses.
                You can give examples from real life to demonstrate the concept.
                You have an csv file where you can search from and provide information to the user.
                Chat history: {_chat_history}
                User question: {question}
            """
    )

# Create the followup chain
    followup_chain = followup_prompt | llm | StrOutputParser()

    # Try to get an answer from the CSV knowledge base
    result = qa_chain({"query": query})
    answer = result['result']

    # If no relevant information found in CSV, use general knowledge
    if "I don't have information" in answer or "I don't know" in answer or "It doesn't contain" or "does not contain" in answer:
        answer = followup_chain.stream(
            {"_chat_history": _chat_history, "question": query})
    else:
        answer = followup_chain.stream(
            {"_chat_history": _chat_history, "question": "Write this with your style:\n" + query})

    return answer


data = load_data()

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Explorer"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("Space Bot"):
            st.markdown(message.content)

user_query = st.chat_input("Ask me anything about exoplanets")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("Explorer"):
        st.markdown(user_query)
    with st.chat_message("Space Bot"):
        with st.spinner("Thinking..."):
            ai_response = get_response(
                user_query, st.session_state.chat_history)
        stream = st.write_stream(ai_response)
    st.session_state.chat_history.append(AIMessage(stream))
