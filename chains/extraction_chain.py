from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

def extraction_chain(prompt):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )
    return prompt | llm | StrOutputParser()