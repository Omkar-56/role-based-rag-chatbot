from app.services.retrieval_service import RetrievalService

retriever = RetrievalService()

results = retriever.retrieve(
    query="maternity leave policy",
    user_role="hr",
)

for r in results:
    print("\n-------------------")
    print("ROLE:", r["role"])
    print("SOURCE:", r["source"])
    print("CONTENT:", r["content"][:200])
