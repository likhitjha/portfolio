import pickle
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.llms import Replicate  # Using Replicate instead of OpenAI
import logging

# Set up Replicate API key
os.environ["REPLICATE_API_TOKEN"] = "r8_MRMNavwiEfL76j8BNhML8fN6RmdPDny2NFOQV"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to assign metadata based on content
def assign_metadata(doc):
    content_upper = doc.page_content.upper()
    if "INTERNSHIP EXPERIENCE" in content_upper:
        doc.metadata['section'] = 'Internship Experience'
    elif "EDUCATION" in content_upper:
        doc.metadata['section'] = 'Education'
    elif "TECHNICAL SKILLS" in content_upper:
        doc.metadata['section'] = 'Technical Skills'
    elif "PROJECTS" in content_upper:
        doc.metadata['section'] = 'Projects'
    else:
        doc.metadata['section'] = 'Other'
    return doc

# Function to split documents with metadata
def split_with_metadata(documents, splitter):
    split_docs = []
    for doc in documents:
        splits = splitter.split_text(doc.page_content)
        for split in splits:
            # Retain metadata
            split_docs.append(Document(page_content=split, metadata=doc.metadata))
            logger.debug(f"Split Document Content: {split}")
            logger.debug(f"Split Document Metadata: {doc.metadata}")
    return split_docs


# Check if vector store exists
if os.path.exists("faiss_index.pkl"):
    with open("faiss_index.pkl", "rb") as file:
        vectorstore = pickle.load(file)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
else:
    # Load documents
    loader_resume = PyPDFLoader("src/Resume.pdf")
    resume_data = loader_resume.load()
    resume_data = [assign_metadata(doc) for doc in resume_data]  # Assign metadata


    # Optionally, decide which documents to index
    # For example, only index resume_data
    all_data = resume_data  # Exclude sto   ry_data for professional queries

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )
    all_splits = split_with_metadata(all_data, text_splitter)

    # Initialize embeddings
    hf = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}  # Adjust settings as in your second code
    )

    # Initialize vector store
    vectorstore = FAISS.from_documents(documents=all_splits, embedding=hf)

    # Save vector store to disk using pickle
    with open("faiss_index.pkl", "wb") as file:
        pickle.dump(vectorstore, file)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

print('Vector store is ready.')

# Initialize the LLM using Replicate
llm = Replicate(
    model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
    model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1}
)

# Define a custom prompt template
prompt_template = """
You are an intelligent assistant that answers questions based on the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

# Create the RetrievalQA chain with Replicate
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PromptTemplate.from_template(prompt_template)},
    return_source_documents=True
)

# Function to run QA with logging
def run_qa_with_logging(query):
    result = qa_chain({"query": query})
    '''
    logger.info(f"Query: {query}")
    logger.info(f"Retrieved Documents: {[doc.page_content for doc in result['source_documents']]}")
    logger.info(f"Retrieved Document Metadata: {[doc.metadata for doc in result['source_documents']]}")
    '''
    return result['result']


while True:
    query = input("Enter your query (type 'quit' to exit): ")
    if query.lower() == "quit":
        print("Exiting the loop.")
        break
    answer = run_qa_with_logging(query)
    print("Answer:", answer)