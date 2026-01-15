from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_DIR = "vector_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)


def run_test(query, expected_role):
    print("\n" + "=" * 60)
    print(f"QUERY: {query}")
    print(f"EXPECTED ROLE: {expected_role}")

    results = db.similarity_search(query, k=3)

    for i, r in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("ROLE:", r.metadata["role"])
        print("SOURCE:", r.metadata["source"])
        print("CONTENT PREVIEW:", r.page_content[:200])


# -------------------
# Semantic Test Cases
# -------------------

run_test("maternity leave policy", "hr / general")
run_test("CI/CD pipeline architecture", "engineering")
run_test("marketing ROI and campaign performance", "marketing")
run_test("vendor costs and expenses", "finance")
