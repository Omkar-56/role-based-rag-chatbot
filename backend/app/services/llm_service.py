import os
from typing import List, Dict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


class LLMService:
    """
    Handles interaction with Groq LLM using LangChain.
    """

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    # --------------------------
    # Build Prompt + Call LLM
    # --------------------------

    def generate_answer(self, query: str, chunks: List[Dict]) -> str:
        """
        Builds a grounded prompt using retrieved chunks and sends it to the LLM.
        """

        # -------------------------
        # 1. Basic empty check
        # -------------------------
        if not chunks:
            return "I don't have enough information to answer that."

        # -------------------------
        # 2. Filter low-quality chunks
        # -------------------------
        relevant_chunks = [
            c for c in chunks if len(c["content"].strip()) > 50
        ]

        if not relevant_chunks:
            return "I don't have enough information to answer that."

        # -------------------------
        # 4. Build context
        # -------------------------
        context = "\n\n".join(
            f"[Source: {c['source']} | Role: {c['role']}]\n{c['content']}"
            for c in chunks
        )

        # -------------------------
        # 5. Prompt
        # -------------------------
        system_prompt = """
            You are a helpful enterprise assistant.
            Answer the user's question strictly using the provided context.
            If the answer is not present in the context, say:
            "I don't have enough information to answer that."
        """

        user_prompt = f"""
            Context:
            {context}
        
            Question:
            {query}
        """

        messages = [
            SystemMessage(content=system_prompt.strip()),
            HumanMessage(content=user_prompt.strip()),
        ]

        # -------------------------
        # 6. Call LLM
        # -------------------------
        response = self.llm.invoke(messages)

        return response.content.strip()
