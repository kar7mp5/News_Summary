# summarize_contents.py
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA




def summarize_article(link):
    """summarize the article

    Args:
        link (str): article link
    
    Returns:
        (str): summarized contents 
    """
    # Initialize loader for each link
    loader = WebBaseLoader(link)
    data = loader.load()

    # Initialize text splitter for each iteration
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    # Initialize model for each iteration
    model = Ollama(model='gemma2:2b', stop=["<|eot_id|>"]) # Added the stop token

    # Define user and system prompts
    user_prompt = "Summarize the content and explain in detail by korean(한국어)."
    system_prompt = """Think and write your step-by-step reasoning before responding.
    Make sure you don't deviate from json grammar.
    Please write all conversations in Korean(한국어).
    """

    # Initialize embeddings and vectorstore for each iteration
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)
    docs = vectorstore.similarity_search(user_prompt)

    # Define prompt template for each iteration
    template = """
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        {system_prompt}
        <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {user_prompt}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
    """
    prompt = PromptTemplate(
        input_variables=['system_prompt', 'user_prompt'],
        template=template
    )

    # Initialize QA chain for each iteration
    qachain = RetrievalQA.from_chain_type(model, retriever=vectorstore.as_retriever())

    # Get the response
    response = qachain(prompt.format(system_prompt=system_prompt, user_prompt=user_prompt))

    return response['result']
