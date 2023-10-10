from io import BytesIO
import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import ChatUI
from langchain.llms import HuggingFaceHub

benson_resume = """
Benson (Ping Hsien) Yang\n

EXPERIENCE

Market Analyst | Python, SQL\n
ARCADIA MOTOR CO., LTD. | Taipei, Taiwan
 

June 2020 - August 2021
 
•	Extracted key metrics from SQL databasesPerformed advanced analysis using Python, leading to the identification of emerging market trends and insights into user behavior, resulting in a 15% increase in marketing efficiency\n
•	Work closely with cross-functional teams, including sales, product, and technology teams, to ensure accuracy and viability of market insights and make data-based strategic recommendations to drive business growth.
 
Software Engineer | VB, Javascript, MYSQL\n
ChainSea Information Integration Co., Ltd | Taipei, Taiwan
 
September 2018 - September 2019
 
•	Performed proactive and ad-hoc product analyses to identify key customer needs and create cyber security through new product features.\n
•	Reviewed, modified, and implemented A/B tests for unit and integration assessments to enhance the Bank's software quality and reliability.

EDUCATION
 
August 2022 - May 2024

Master of Science in Business Analytics\n
Hofstra University | Hempstead,NY\n
•	GPA : 4.0, Graduate Excellence Award Recipient

August 2016 - May 2020\n

Bachelor in Information Management\n
National Taipei University of Business | Taipei, Taiwan

PROJECTS

Quantium Virtual Project from Forage| R, Tableau	August 2023 - August 2023\n
Conducted advanced data analysis on transaction and purchase behavior data. Utilized tools Tableau and R for data visualization, statistical modeling, and data processing, producing clear and concise reports for Quantium.\n

Slide Assistant by Open AI| Python, MySQL	June 2023 - August 2023\n
Utilized Python programming and the latest GPT model, designed innovative and user-friendly presentation scripts that generate interfaces and help users improve their presentations.\n

E-commercial Website Scraping and Analysis | Python, MySQL	August 2022 - November 2022\n
Used Python to collect data on the website and inserted it into a database built on the AWS EC2 server, analyzed each dataset's correlation, and visualized it in several charts. Finally, used LSTM Neural Networks to predict the market.

KEY SKILLS

Software / Programming: Python, R, Matlab, Swift, EXCEL\n
Data Stack: SQL, Tableau, GCP, AWS\n
Python Packages: Pandas, NumPy, Matplotlib, scikit-learn, Tensorflow, GPT\n
Machine Learning Models: Linear/Logistic Regression, Decision Trees, Random Forest, Extra Trees, k-Means Clusters, K-Nearest Neighbors, Neural Networks ( LSTM, CNNs ), NLP model\n

"""

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

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=os.environ["OPENAI_API_KEY"])
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
        if i % 2 == 0:
            st.write(ChatUI.user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(ChatUI.bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    # load_dotenv()
    st.set_page_config(page_title="Chat with Resume",
                       page_icon="https://i.ibb.co/XXrhT5P/protraitt.jpg")
    st.write(ChatUI.css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with candidate Ping Hsien Yang 👨‍💻")
    st.markdown('<span style="font-size:12px"><i>This Chat engine by GPT-3.5</span>', unsafe_allow_html=True)
    user_question = st.text_input(""" Ask Ping Hsien Yang's resume if he can be a unicorn whispering, cookie tasting, or data analyst? 🦄🍪👨‍🔧""")

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

        st.markdown('<h1 style="font-size:2em;">Ping Hsien Yang\'s Resume</h1>', unsafe_allow_html=True)
        st.sidebar.markdown("[Download Resume PDF](https://drive.google.com/file/d/1j-BvvDxjOrhxorORx71gGJv_fW950zBG/view)")

        with st.expander("Expand Resume", expanded=True):
            st.write(benson_resume)
        # get the text chunks
        text_chunks = get_text_chunks(benson_resume)

        # create vector store
        vectorstore = get_vectorstore(text_chunks)

        # create conversation chain
        st.session_state.conversation = get_conversation_chain(
            vectorstore)
        # print(get_conversation_chain(vectorstore))

        # st.write(benson_resume)


if __name__ == '__main__':
    main()
