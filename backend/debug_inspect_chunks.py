from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import random

DB_DIR = "vector_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

# Fetch random samples
results = db.similarity_search("policy", k=5, )

for r in results:
    print("\n----------------")
    print("SOURCE:", r.metadata)
    print("CONTENT:\n", r.page_content[:500])
