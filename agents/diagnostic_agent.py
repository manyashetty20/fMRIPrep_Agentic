import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

class DiagnosticAgent:
    """
    Pillar 3: The Diagnostic Agent
    Analyzes fMRIPrep logs to find root causes of crashes.
    """
    def __init__(self):
        # We use Groq (Llama 3) because it's extremely fast for reading long logs
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0
        )

    def diagnose_crash(self, error_log):
        template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Neuroimaging Data Engineer. Analyze the fMRIPrep error log and identify exactly why it failed and how to fix it."),
            ("user", "Here is the error log snippet:\n{log_text}")
        ])
        
        chain = template | self.llm
        return chain.invoke({"log_text": error_log}).content