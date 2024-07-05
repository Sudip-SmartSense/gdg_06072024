import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# Load environment variables from .env file
load_dotenv()


model = ChatGroq(
    model="llama3-70b-8192", temperature=0.5
)

system = """
You are a helpful assistant that always provides a single sentence as answer.
"""


human = "{question}"
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", human)])

chain = prompt | model

print(chain.invoke({"question": "How can I utilise an LLM?"}))
