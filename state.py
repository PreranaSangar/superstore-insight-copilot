from typing import TypedDict


class AgentState(TypedDict):

    user_query: str
    conversation_history: str
    plan: str
    tool_name: str
    tool_result: str
    final_answer: str