from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Replicate
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os  

os.environ["REPLICATE_API_TOKEN"] ="r8_MRMNavwiEfL76j8BNhML8fN6RmdPDny2NFOQV"


# Load documents
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
retriever = vectorstore.as_retriever()

# Define prompt template
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum and keep the answer as concise as possible. Still give details, don't be generic.
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# Initialize RetrievalQA chain
llm = Replicate(
    model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
    model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1}
)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

question = "What projects has Likhit done?"
result = qa_chain({"query": question})
print(result["result"])


for doc in result["source_documents"]:
    print(doc.page_content)

print("\nAnswer:")
print(result["result"])