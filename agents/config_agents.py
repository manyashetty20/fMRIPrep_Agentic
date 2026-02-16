import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_groq import ChatGroq # Use Groq instead of OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

class ConfigAgent:
    def __init__(self, doc_path="./data/docs/", db_path="./database/vector_store/"):
        # Load fMRIPrep & BIDS Documentation
        loader = DirectoryLoader(doc_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()

        # We still use OpenAI for embeddings; ensure your OPENAI_API_KEY is set
        self.embeddings = OpenAIEmbeddings()
        self.vector_db = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings, 
            persist_directory=db_path
        )
        
        # Initialize Groq LLM (e.g., Llama 3.3 70B)
        # Ensure you have set: export GROQ_API_KEY='your-key'
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile", 
            temperature=0
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever()
        )

    def generate_command(self, bids_dir, participant_id):
        query = f"""
        Analyze the setup for participant {participant_id} in {bids_dir}.
        If no fieldmaps are found in the /fmap folder, suggest the --use-syn-sdc flag.
        Generate a complete fMRIPrep Docker command.
        """
        response = self.qa_chain.invoke(query)
        return response["result"]