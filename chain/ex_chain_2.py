import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

model = ChatGroq(
    model="llama3-70b-8192", temperature=0.5
)

system = """
You are a helpful assistant that always provides a single sentence as answer.
"""
# Create an output parser
output_parser = StrOutputParser()


human = "{question}"
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", human)])

chain = prompt | model | output_parser

print(chain.invoke({"question": "How can I utilise an LLM?"}))
