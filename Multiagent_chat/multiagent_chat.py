from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate
import wikipedia
from ddgs import DDGS   # ✅ updated package

# Initialize LLM
llm = Ollama(model="llama3.2")


# -------------------------------
# 🧠 Planner Agent (DETAILED + RESOURCES)
# -------------------------------
def planner_agent(user_query):
    prompt = PromptTemplate(
        input_variables=["query"],
        template="""
You are a PLANNER agent.

Create a DETAILED step-by-step plan.

RULES:
- Each step must be clear and actionable
- Mention which RESOURCE to use (Wikipedia / Web / LLM knowledge)
- Do NOT explain concepts
- Stay strictly relevant
- Maximum 5 steps

Query: {query}

Output Format:

Step 1: ... (Resource: ...)
Step 2: ... (Resource: ...)
Step 3: ... (Resource: ...)
Step 4: ... (Resource: ...)
Step 5: ... (Resource: ...)
"""
    )

    chain = prompt | llm
    return chain.invoke({"query": user_query}).strip()


# -------------------------------
# 📘 Wikipedia Tool
# -------------------------------
def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "No Wikipedia data found."


# -------------------------------
# 🌐 Web Search Tool
# -------------------------------
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except:
        return "No web results found."


# -------------------------------
# 🤖 Executor Agent (IMPROVED)
# -------------------------------
def executor_agent(steps, user_query):
    wiki_data = search_wikipedia(user_query)
    web_data = search_web(user_query)

    prompt = PromptTemplate(
        input_variables=["steps", "wiki", "web", "query"],
        template="""
You are an EXECUTOR agent.

Use:
- Planner steps
- Wikipedia data
- Web data
- Your own knowledge

STRICT RULES:
- Do NOT repeat steps
- Give final answer only
- Keep it short, clear, and factual
- If data is missing, use your knowledge

QUESTION:
{query}

Wikipedia:
{wiki}

Web:
{web}

OUTPUT FORMAT:

Answer:
- Definition: ...
- Key Points:
  - ...
  - ...

Sources:
- Wikipedia
- Web
"""
    )

    chain = prompt | llm
    return chain.invoke({
        "steps": steps,
        "wiki": wiki_data,
        "web": web_data,
        "query": user_query
    }).strip()


# -------------------------------
# 💬 Main System
# -------------------------------
def multiagent_chat():
    print("\n==============================")
    print("🤖 Multi-Agent Chat System")
    print("==============================\n")

    while True:
        user_input = input("👤 You: ")

        if user_input.lower() == "exit":
            print("\n👋 Exiting Chat...\n")
            break

        # Planner
        steps = planner_agent(user_input)

        print("\n🧠 DETAILED PLAN:")
        print("------------------------------")
        print(steps)

        # Executor
        final_output = executor_agent(steps, user_input)

        print("\n🤖 FINAL ANSWER:")
        print("------------------------------")
        print(final_output)

        print("\n==============================\n")


if __name__ == "__main__":
    multiagent_chat()