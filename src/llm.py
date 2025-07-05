from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def initiate_llm():
    llm = ChatOpenAI(model="o3-mini")
    return llm
