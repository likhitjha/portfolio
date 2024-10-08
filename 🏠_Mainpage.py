import streamlit as st
import streamlit.components.v1 as components
from constant import *
import os
import pickle

# Import necessary modules for the chatbot
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Replicate
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up OpenAI API key
os.environ["REPLICATE_API_TOKEN"] = st.secrets["general"]["REPLICATE_API_TOKEN"]
 

# Initialize Streamlit page
st.set_page_config(page_title="Main Page", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")

# Cache the Resume loading function
@st.cache_data
def load_resume():
    with open("src/Resume.pdf", "rb") as file:
        return file.read()

# Cache the vector store creation/loading
@st.cache_data
def get_vectorstore():
    if os.path.exists("faiss_index.pkl"):
        with open("faiss_index.pkl", "rb") as file:
            vectorstore = pickle.load(file)
    else:
        # Load documents and embeddings
        loader_resume = PyPDFLoader("src/Resume.pdf")
        resume_data = loader_resume.load()

        loader_story = PyPDFLoader("src/Story.pdf")
        story_data = loader_story.load()

        resume_data.extend(story_data)

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        all_splits = text_splitter.split_documents(resume_data)

        # Initialize embeddings
        hf = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )

        # Initialize vector store
        vectorstore = FAISS.from_documents(documents=all_splits, embedding=hf)

        # Save vector store to disk using pickle
        with open("faiss_index.pkl", "wb") as file:
            pickle.dump(vectorstore, file)
    
    return vectorstore

# Cache the question-answering chain creation
@st.cache_resource
def get_qa_chain():
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer. 
    You are Likhit's Personal Assistant Leebot, don't use the context provided bellow if you think its useless for answering the question asked.

    Context:
    {context}

    Question: {question}

    Helpful Answer:"""

    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Initialize RetrievalQA chain
    llm = Replicate(
        model="meta/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0",
        model_kwargs={"temperature": 0.1, "max_length": 500, "top_p": 1}
    )

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    return qa_chain

margin_r, body, margin_l = st.columns([0.4, 3, 0.4])

with body:
    menu()
    
    # Sidebar
    with st.sidebar:
        st.success("Select a page above.")
        
    # Main Page
    st.header("About Me", divider='rainbow')

    col1, col2, col3 = st.columns([1.3, 0.2, 1])

    with col1:
        st.write(info['brief'])
        st.markdown(f"###### 😄 Name: {info['name']}")
        st.markdown(f"###### 👉 Study: {info['study']}")
        st.markdown(f"###### 📍 Location: {info['location']}")
        st.markdown(f"###### 📚 Interest: {info['interest']}")
        st.markdown("###### 🟡 Favorite Color: Yellow")
        st.markdown(f"###### 👀 Linkedin: {linkedin_link}")
        
        resume_file = load_resume()

        st.download_button(
            label="Download my :blue[resume]",
            data=resume_file,
            file_name="resume",
            mime="application/pdf"
        )

    with col3:
        st.image("src/portrait.jpeg")

    # Skills Section
    st.subheader("My :blue[skills] ⚒️", divider='rainbow')

    def skill_tab():
        rows, cols = len(info['skills']) // skill_col_size, skill_col_size
        skills = iter(info['skills'])
        if len(info['skills']) % skill_col_size != 0:
            rows += 1
        for x in range(rows):
            columns = st.columns(skill_col_size)
            for index_ in range(skill_col_size):
                try:
                    columns[index_].button(next(skills))
                except:
                    break

    with st.spinner(text="Loading section..."):
        skill_tab()

    qa_chain = get_qa_chain()

st.title("💬 Leebot")
st.write("This is a simple chatbot that uses LangChain with LLaMA-2 to generate responses.")

# Initialize session state for messages if not already done
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle user and assistant interactions
def handle_interaction(prompt):
    # Append the user's question to the chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display a spinner while waiting for the LLM response
    with st.spinner("Leebot is thinking..."):
        # Generate a response using the RetrievalQA chain
        result = qa_chain({"query": prompt})
        response = result["result"]

    # Append the assistant's response to the chat
    st.session_state.messages.append({"role": "assistant", "content": response})

# Suggested Questions
st.markdown("### Here are some questions you can ask:")
col1, col2, col3 = st.columns(3)

# Define suggested questions
question_1 = "Can you tell me about Likhit's experience at WNS?"
question_2 = "What is Likhit's expertise in time series forecasting?"
question_3 = "What is Likhit like ? "

# Handle button clicks for suggested questions
if col1.button(question_1):
    handle_interaction(question_1)

if col2.button(question_2):
    handle_interaction(question_2)

if col3.button(question_3):
    handle_interaction(question_3)

# Handle user input via chat input box
if prompt := st.chat_input("I am Likhit's personal assistant, chat with me"):
    handle_interaction(prompt)

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
