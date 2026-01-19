import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
DB_DIR = "vector_db"

# ----------------------------
# Load documents from folders
# ----------------------------

def load_documents():
    documents = []

    for role in os.listdir(DATA_DIR):
        role_path = os.path.join(DATA_DIR, role)

        if not os.path.isdir(role_path):
            continue

        for file in os.listdir(role_path):
            file_path = os.path.join(role_path, file)

            # -------- MARKDOWN FILES --------
            if file.endswith(".md"):
                loader = TextLoader(file_path, encoding="utf-8")
                docs = loader.load()

                for d in docs:
                    d.metadata["role"] = role
                    d.metadata["source"] = file

                documents.extend(docs)

            # -------- CSV FILES (HR) --------
            elif file.endswith(".csv"):
                df = pd.read_csv(file_path)

                # Convert each row into text
                for idx, row in df.iterrows():
                    row_text = " | ".join(
                        [f"{col}: {row[col]}" for col in df.columns]
                    )

                    doc = Document(
                        page_content=row_text,
                        metadata={
                            "role": role,
                            "source": file,
                            "row": idx
                        }
                    )
                    documents.append(doc)

            else:
                print(f"⚠️ Skipping unsupported file: {file}")

    return documents

# ----------------------------
# Split documents into chunks
# ----------------------------

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)

# ----------------------------
# Create Vector Store
# ----------------------------

def create_vector_db(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    print("Vector database created successfully!")

# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":
    print("📄 Loading documents...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")

    print("✂️ Splitting documents...")
    chunks = split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("🧠 Creating embeddings + vector store...")
    create_vector_db(chunks)