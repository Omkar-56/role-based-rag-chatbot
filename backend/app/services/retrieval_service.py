from typing import List, Dict

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.rbac import RBAC


class RetrievalService:
    """
    Handles secure document retrieval using:
    - Vector similarity search
    - YAML-based RBAC filtering
    """

    def __init__(
        self,
        db_dir: str = "vector_db",
        rbac_path: str = "config/rbac.yaml",
        top_k: int = 3,
    ):
        self.top_k = top_k

        # Embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Vector database
        self.db = Chroma(
            persist_directory=db_dir,
            embedding_function=self.embeddings,
        )

        # RBAC engine
        self.rbac = RBAC(rbac_path)

    # -------------------------
    # Core Retrieval Function
    # -------------------------

    def retrieve(self, query: str, user_role: str) -> List[Dict]:
        """
        Retrieves relevant documents based on query and user role.

        Returns:
        [
            {
                "content": "...",
                "source": "employee_handbook.md",
                "role": "general"
            }
        ]
        """

        allowed_departments = self.rbac.allowed_departments(user_role)

        if not allowed_departments:
            raise ValueError(f"No access permissions for role: {user_role}")

        results = self.db.similarity_search(
            query=query,
            k=self.top_k,
            filter={"role": {"$in": allowed_departments}},
        )

        formatted_results = []
        for doc in results:
            formatted_results.append(
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source"),
                    "role": doc.metadata.get("role"),
                }
            )

        return formatted_results
