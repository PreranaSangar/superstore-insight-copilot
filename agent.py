import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from state import AgentState
from tools import (
    data_query_tool,
    calculation_tool,
    chart_tool
)

# =========================================================
# Load Environment Variables
# =========================================================

load_dotenv()


# =========================================================
# Initialize Cloud LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=200
)


# =========================================================
# Planner Node
# =========================================================

def planner_node(state: AgentState):

    user_query = state["user_query"]

    print("\n[PLANNER] Sending question to cloud LLM...")

    conversation_history = state.get(
        "conversation_history",
        ""
    )

    prompt = f"""
You are planning a data analysis task.

Previous conversation:
{conversation_history}

Current question:
{user_query}

Create a short, accurate plan in 1 sentence.

Important:
- Describe only the operations that are actually needed.
- Do not invent extra calculations.
- For sales growth from the first month to the last month, compare the first month's sales with the last month's sales and calculate the percentage growth.
- Do not say that growth is calculated separately for each year unless the user explicitly asks for yearly growth.
- Keep the plan concise.
"""

    response = llm.invoke(prompt)

    print("[PLANNER] Cloud LLM response received.")

    return {
        "plan": response.content
    }


# =========================================================
# Router Node
# =========================================================

def router_node(state: AgentState):

    user_query = state["user_query"].lower().strip()

    print("\n[ROUTER] Selecting tool...")

    # -----------------------------------------------------
    # Chart-related questions
    # -----------------------------------------------------

    chart_keywords = [
        "chart",
        "graph",
        "plot",
        "visualize",
        "visualization",
        "draw",
        "trend"
    ]

    if any(keyword in user_query for keyword in chart_keywords):

        tool_name = "chart"

    # -----------------------------------------------------
    # Product ranking / calculation questions
    # -----------------------------------------------------

    elif (
        "product" in user_query
        and (
            "highest" in user_query
            or "top" in user_query
            or "best" in user_query
            or "most" in user_query
        )
    ):

        tool_name = "calculation"

    # -----------------------------------------------------
    # Other calculation questions
    # -----------------------------------------------------

    elif any(keyword in user_query for keyword in [
        "average",
        "mean",
        "typical",
        "per order",
        "average order",
        "usual",
        "on average",
        "percentage",
        "growth",
        "difference",
        "increase",
        "decrease"
    ]):

        tool_name = "calculation"

    # -----------------------------------------------------
    # Data retrieval / grouping questions
    # -----------------------------------------------------

    else:

        tool_name = "data_query"

    print(
        f"[ROUTER] Tool selected: {tool_name}"
    )

    return {
        "tool_name": tool_name
    }


# =========================================================
# Data Tool Node
# =========================================================

def data_tool_node(state: AgentState):

    user_query = state["user_query"].lower()

    print("\n[DATA TOOL] Selecting data query...")

    # -----------------------------------------------------
    # Sales by region
    # -----------------------------------------------------

    if "region" in user_query:

        query_type = "sales_by_region"

    # -----------------------------------------------------
    # Sales by category
    # -----------------------------------------------------

    elif "category" in user_query:

        query_type = "sales_by_category"

    # -----------------------------------------------------
    # Monthly sales
    # -----------------------------------------------------

    elif (
        "monthly" in user_query
        or "month" in user_query
    ):

        query_type = "monthly_sales"

    # -----------------------------------------------------
    # Total sales
    # -----------------------------------------------------

    elif "total sales" in user_query:

        query_type = "total_sales"

    # -----------------------------------------------------
    # Default
    # -----------------------------------------------------

    else:

        query_type = "total_sales"

    print(
        f"[DATA TOOL] Query type: {query_type}"
    )

    result = data_query_tool(query_type)

    return {
        "tool_result": str(result)
    }


# =========================================================
# Calculation Tool Node
# =========================================================

def calculation_tool_node(state: AgentState):

    user_query = state["user_query"].lower()

    print(
        "\n[CALCULATION TOOL] Selecting calculation..."
    )

    # -----------------------------------------------------
    # Top / highest selling products
    # -----------------------------------------------------

    if (
        "product" in user_query
        and (
            "highest" in user_query
            or "top" in user_query
            or "best" in user_query
            or "most" in user_query
        )
    ):

        calculation_type = "top_products"

    # -----------------------------------------------------
    # Sales growth
    # -----------------------------------------------------

    elif "growth" in user_query:

        calculation_type = "sales_growth"

    # -----------------------------------------------------
    # Average sales
    # -----------------------------------------------------

    elif (
        "average" in user_query
        or "mean" in user_query
    ):

        calculation_type = "average_sales"

    # -----------------------------------------------------
    # Default
    # -----------------------------------------------------

    else:

        calculation_type = "average_sales"

    print(
        f"[CALCULATION TOOL] Calculation type: "
        f"{calculation_type}"
    )

    result = calculation_tool(
        calculation_type
    )

    return {
        "tool_result": str(result)
    }


# =========================================================
# Chart Tool Node
# =========================================================

def chart_tool_node(state: AgentState):

    user_query = state["user_query"].lower()

    print("\n[CHART TOOL] Selecting chart...")

    # -----------------------------------------------------
    # Get conversation history
    # -----------------------------------------------------

    conversation_history = state.get(
        "conversation_history",
        ""
    ).lower()

    # -----------------------------------------------------
    # IMPORTANT:
    # For chart selection, current question gets priority.
    # This prevents previous category/region questions from
    # affecting the current chart.
    # -----------------------------------------------------

    # -----------------------------------------------------
    # Top 3 Products Chart
    # -----------------------------------------------------

    if (
        "product" in user_query
        and (
            "top" in user_query
            or "highest" in user_query
            or "best" in user_query
            or "most" in user_query
        )
    ):

        chart_type = "top_3_products"

    # -----------------------------------------------------
    # Category Chart
    # -----------------------------------------------------

    elif "category" in user_query:

        chart_type = "category_sales"

    # -----------------------------------------------------
    # Region Chart
    # -----------------------------------------------------

    elif "region" in user_query:

        chart_type = "region_sales"

    # -----------------------------------------------------
    # Monthly Chart
    # -----------------------------------------------------

    elif (
        "monthly" in user_query
        or "month" in user_query
    ):

        chart_type = "monthly_sales"

    # -----------------------------------------------------
    # Trend Chart
    # -----------------------------------------------------

    elif "trend" in user_query:

        chart_type = "monthly_sales"

    # -----------------------------------------------------
    # If current question uses "it", "these", etc.,
    # use conversation history to understand the chart.
    # -----------------------------------------------------

    else:

        context = (
            conversation_history
            + "\n"
            + user_query
        )

        if (
            "product" in context
            and (
                "top" in context
                or "highest" in context
                or "best" in context
                or "most" in context
            )
        ):

            chart_type = "top_3_products"

        elif "category" in context:

            chart_type = "category_sales"

        elif "region" in context:

            chart_type = "region_sales"

        elif (
            "monthly" in context
            or "month" in context
            or "trend" in context
        ):

            chart_type = "monthly_sales"

        else:

            chart_type = "monthly_sales"

    print(
        f"[CHART TOOL] Chart type: {chart_type}"
    )

    result = chart_tool(chart_type)

    return {
        "tool_result": str(result)
    }


# =========================================================
# Final Answer Node
# =========================================================

def final_answer_node(state: AgentState):

    user_query = state["user_query"]

    plan = state["plan"]

    tool_result = state["tool_result"]

    conversation_history = state.get(
        "conversation_history",
        ""
    )

    prompt = f"""
You are a precise data analysis assistant.

Previous conversation:
{conversation_history}

Current user question:
{user_query}

Plan:
{plan}

Tool result:
{tool_result}

Answer the user's question directly using the tool result.

IMPORTANT RULES:

1. Use ONLY information contained in the tool result.

2. Do NOT invent numbers, dates, months, trends, comparisons,
   or calculations.

3. Do NOT introduce a time period such as "last month",
   "first month", "this month", or "last year" unless the user
   explicitly asks for it AND the tool result contains that
   information.

4. If the user asks "Which category performed best?",
   compare the category sales values in the tool result and
   identify the category with the highest sales value.

5. If the tool result contains multiple categories with sales
   values, the category with the highest sales value represents
   the best-performing category unless the user specifies
   another performance metric.

6. If the user asks a ranking or comparison question, give the
   ranking directly from the values in the tool result.

7. Do not say that additional data, another graph, or another
   calculation is required when the tool result already contains
   enough information.

8. Do not reinterpret total sales as monthly sales.

9. Do not add calculations that were not requested.

10. If the tool result is a chart filename, clearly state that
    the requested chart has been generated and identify what
    the chart represents.

11. Keep the answer clear, concise, and professional.

For the current question, provide the direct answer first.
"""

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }


# =========================================================
# Create LangGraph
# =========================================================

graph = StateGraph(AgentState)


# =========================================================
# Add Nodes
# =========================================================

graph.add_node(
    "planner",
    planner_node
)

graph.add_node(
    "router",
    router_node
)

graph.add_node(
    "data_tool",
    data_tool_node
)

graph.add_node(
    "calculation_tool",
    calculation_tool_node
)

graph.add_node(
    "chart_tool",
    chart_tool_node
)

graph.add_node(
    "final_answer",
    final_answer_node
)


# =========================================================
# Graph Flow
# =========================================================

graph.add_edge(
    START,
    "planner"
)

graph.add_edge(
    "planner",
    "router"
)


# =========================================================
# Conditional Routing
# =========================================================

def route_to_tool(state: AgentState):

    tool_name = state["tool_name"]

    if tool_name == "data_query":

        return "data_tool"

    elif tool_name == "calculation":

        return "calculation_tool"

    elif tool_name == "chart":

        return "chart_tool"

    return "data_tool"


graph.add_conditional_edges(
    "router",
    route_to_tool,
    {
        "data_tool": "data_tool",
        "calculation_tool": "calculation_tool",
        "chart_tool": "chart_tool"
    }
)


# =========================================================
# Tools → Final Answer
# =========================================================

graph.add_edge(
    "data_tool",
    "final_answer"
)

graph.add_edge(
    "calculation_tool",
    "final_answer"
)

graph.add_edge(
    "chart_tool",
    "final_answer"
)


# =========================================================
# Final Answer → END
# =========================================================

graph.add_edge(
    "final_answer",
    END
)


# =========================================================
# Compile Graph
# =========================================================

app = graph.compile()


# =========================================================
# Test Agent from Terminal
# =========================================================

if __name__ == "__main__":

    user_question = input(
        "Enter your question: "
    )

    result = app.invoke({

        "user_query": user_question,

        "conversation_history": "",

        "plan": "",

        "tool_name": "",

        "tool_result": "",

        "final_answer": ""

    })

    print("\n--- PLAN ---")

    print(
        result["plan"]
    )

    print("\n--- TOOL USED ---")

    print(
        result["tool_name"]
    )

    print("\n--- TOOL RESULT ---")

    print(
        result["tool_result"]
    )

    print("\n--- FINAL ANSWER ---")

    print(
        result["final_answer"]
    )