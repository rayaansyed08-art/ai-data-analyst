import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI

load_dotenv()

# Simple memory (no LangChain dependency)
memory = []

llm = ChatOpenAI(
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

def run_agent(df, query, context):
    prompt = f"""
    You are a professional data analyst.

    Dataset columns: {df.columns.tolist()}
    Context: {context}

    User question: {query}

    Instructions:
    - Give clear and short answers
    - Explain insights if possible
    - If chart is needed, say 'PLOT'
    """

    try:
        response = llm.invoke(prompt)

        # Store memory
        memory.append(("User", query))
        memory.append(("AI", response.content))

        return response.content

    except Exception as e:
        return f"Error: {str(e)}"


def create_plot(df):
    numeric_cols = df.select_dtypes(include='number').columns

    plt.figure()

    for col in numeric_cols:
        plt.plot(df[col], label=col)

    plt.title("Data Trends")
    plt.legend()
    plt.savefig("plot.png")