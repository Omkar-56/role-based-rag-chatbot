from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.rbac import RBAC

DB_DIR = "vector_db"

# --------------------
# Initialize Services
# --------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

rbac = RBAC("config/rbac.yaml")

# --------------------
# Test Runner
# --------------------

def run_test(query, role, expected_role):
    print("\n" + "=" * 60)
    print(f"QUERY: {query}")
    print(f"USER ROLE: {role}")
    print(f"EXPECTED ROLE: {expected_role}")

    allowed = rbac.allowed_departments(role)
    print("ALLOWED DEPARTMENTS:", allowed)

    results = db.similarity_search(
        query,
        k=3,
        filter={"role": {"$in": allowed}}
    )

    for i, r in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("ROLE:", r.metadata["role"])
        print("SOURCE:", r.metadata["source"])
        print("CONTENT PREVIEW:", r.page_content[:200])


# -------------------
# Semantic Test Cases
# -------------------

run_test("maternity leave policy", "hr", "hr / general")
run_test("CI/CD pipeline architecture", "engineering", "engineering")
run_test("marketing ROI and campaign performance", "marketing", "marketing")
run_test("vendor costs and expenses", "finance", "finance")
