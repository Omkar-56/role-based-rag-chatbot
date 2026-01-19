from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
)

response = llm.invoke([
    HumanMessage(content="what is the capital of india.")
])

print(response.content)
