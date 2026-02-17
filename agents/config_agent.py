import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA

class ConfigAgent:
    def __init__(self, doc_path="./data/docs/", db_path="./database/vector_store/"):
        # 1. Load fMRIPrep & BIDS Documentation
        loader = DirectoryLoader(doc_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()

        # 2. Use Local Embeddings (No API Key Needed)
        # This will download a small model (~400MB) the first time you run it
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        self.vector_db = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings, 
            persist_directory=db_path
        )
        
        # 3. Use Groq for the "Thinking"
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile", 
            temperature=0
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever()
        )

    def generate_command(self, bids_dir, participant_id, has_fmap):
        query = f"""
        Context: BIDS_DIR={bids_dir}, Sub={participant_id}, Fieldmaps_Found={has_fmap}
        TASK: Generate a ONE-LINE fMRIPrep Docker command.
        RULES:
        1. Use "$PWD/data/bids_input" for the input volume.
        2. Use "$PWD/outputs" for the output volume.
        3. Return ONLY the bash code block.
        """
        response = self.qa_chain.invoke(query)
        return response["result"]