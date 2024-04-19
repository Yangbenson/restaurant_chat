from io import BytesIO
import os

import langchain_openai
import streamlit as st
import asyncio
import threading
from streamlit_js_eval import streamlit_js_eval, get_geolocation
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import ChatUI
from langchain.llms import HuggingFaceHub
from get_restaurant import *



loc_string = ""

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):

    # llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", openai_api_key=os.environ["OPENAI_API_KEY"])
    llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=os.environ["OPENAI_API_KEY"])
    # llm = HuggingFaceHub(repo/_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):

        # if i == 0:
        #     search_result = search(user_question,loc_string)
        #     st.write("Search result:",search_result)
        #
        # 根据 i 的奇偶性决定使用哪个模板
        if i % 2 == 0:
            st.write(ChatUI.user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(ChatUI.bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def fetch_location():

    loc = get_geolocation()
    loc_string = f"{loc['coords']['latitude']}, {loc['coords']['longitude']}"
    st.session_state['location'] = loc_string

    return loc_string


def main():

    st.set_page_config(page_title="Ping Hsien Yang's Portfolio",
                       page_icon="https://i.ibb.co/n74nyd7/restaurant.png")

    st.write(ChatUI.css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Restaurant Chat")
    st.markdown('<span style="font-size:12px"><i>This Chat engine by GPT-3.5</span>', unsafe_allow_html=True)
    user_question = st.text_input(""" Enter a country to see its restaurants:""")

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:

        st.sidebar.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.css">',
            unsafe_allow_html=True)

        # 創建一個包含所有三個連結的HTML片段
        icons_html = f'''
        <div>{ChatUI.linkedin_link}
            {ChatUI.github_link}
            {ChatUI.email_link}</div>
        '''
        # 在側邊欄中顯示圖標
        st.sidebar.markdown(icons_html, unsafe_allow_html=True)

        st.sidebar.write("------------------------")

        # st.markdown('<h1 style="font-size:2em;">Ping Hsien Yang\'s Resume</h1>', unsafe_allow_html=True)
        # st.sidebar.markdown("[Download Resume](https://drive.google.com/file/d/1j-BvvDxjOrhxorORx71gGJv_fW950zBG/view)")


        # When the checkbox is clicked, start fetching the location
        if st.checkbox("Check my location"):
            loc_string =  fetch_location()
            st.write(st.session_state['location'])


        # with st.expander("Expand Resume", expanded=True):
            # st.write(ChatUI.resume4gpt)

        country = st.text_input("Enter a country to see its restaurants:")

        if country:

            search_result = search(f"{country} restaurant", loc_string)
            print(f"{search_result} \n, {loc_string} ")
            # st.write("Search result:", search_result)

            # get the text chunks
            # text_chunks = get_text_chunks(ChatUI.resume4gpt)

            # get prompt data
            text = search_result['gpt_prompt'].tolist()
            print(text)
            # create vector store
            vectorstore = get_vectorstore(text)

            # create conversation chain
            st.session_state.conversation = get_conversation_chain(
                vectorstore)

            print(country)

if __name__ == '__main__':
    main()
