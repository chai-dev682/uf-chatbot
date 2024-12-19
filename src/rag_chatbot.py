from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.vectordb_utils import query_pinecone
import config

def create_rag_chain():
    # Initialize the LLM
    llm = ChatOpenAI(
        model=config.ModelType.gpt4o,
        temperature=0.7,
        api_key=config.OPENAI_API_KEY
    )

    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(config.get_prompt_template(config.PromptTemplate.MAIN_PROMPT))

    # Create the RAG chain
    rag_chain = (
        {"context": lambda x: query_pinecone(x["question"]), "question": lambda x: x["question"], "conversation": lambda x: x["conversation"]}
        | prompt
        | llm
    )
    
    return rag_chain

def chat_with_rag(question: str, conversation: str):
    chain = create_rag_chain()
    response = chain.invoke({"question": question, "conversation": conversation})
    return response.content