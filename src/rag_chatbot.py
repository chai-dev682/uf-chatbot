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
    prompt = ChatPromptTemplate.from_template("""
    You are an intelligent AI assistant, designed to provide comprehensive and informative responses for https://www.ultimatefitnessholiday.com websites clients.
                                                
    Ultimate Fitness Holiday offers a range of fitness retreats and holidays designed for individuals seeking to enhance their health and fitness in beautiful tropical locations. Here are the key features of the program:

    ## Overview
    - **Locations**: Ultimate Fitness Holiday operates in popular destinations such as **Spain**, **Thailand**, and **Bali**, catering to various fitness levels and preferences.
    - **Target Audience**: The retreats are open to everyone, whether you're looking to kickstart your fitness journey or improve your existing routine. 

    ## Programs Offered
    - **Fitness Bootcamps**: These are structured programs that combine workouts with relaxation, set in picturesque environments. The Mallorca bootcamp is highlighted as the only European option, providing a blend of fitness and holiday experiences.
    - **Long-Term Transformations**: Options for extended stays in Thailand focus on significant lifestyle changes and personal growth.

    ## Community and Support
    - Participants benefit from the guidance of expert personal trainers and the motivation of a supportive community. This environment encourages accountability and fosters connections with like-minded individuals.

    ## Experience
    - The retreats emphasize not just physical fitness but also mental well-being, aiming to transform participants' outlooks on health and fitness. Activities are balanced with free time for relaxation and exploration of the stunning locales.

    Overall, Ultimate Fitness Holiday combines fitness training with vacationing, allowing participants to achieve their health goals while enjoying luxurious accommodations and beautiful surroundings.

    Based on the given context below, produce an answer that elaborates on the situation, provides in-depth knowledge.
    If context includes url, you can return that url as a reference
    If the question is a context-free question, you do not need to describe anything related to the context.
    Context: {context}

    Question: {question}""")

    # Create the RAG chain
    rag_chain = (
        {"context": lambda x: query_pinecone(x["question"]), "question": lambda x: x["question"]}
        | prompt
        | llm
    )
    
    return rag_chain

def chat_with_rag(question: str):
    chain = create_rag_chain()
    response = chain.invoke({"question": question})
    return response.content