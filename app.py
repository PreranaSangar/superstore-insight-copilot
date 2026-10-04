import streamlit as st
from agent import app as agent_app


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Superstore Insight Copilot",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# Header
# =========================================================

st.title("📊 Superstore Insight Copilot")

st.write(
    "Ask questions about the Superstore dataset "
    "and get AI-powered data insights."
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# Initialize Chat History
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# Display Previous Messages
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# User Input
# =========================================================

user_question = st.chat_input(
    "Ask a question about your Superstore data..."
)


# =========================================================
# Process User Question
# =========================================================

if user_question and user_question.strip():

    user_question = user_question.strip()


    # =====================================================
    # Create Conversation History
    # =====================================================

    conversation_history = ""

    for message in st.session_state.messages:

        conversation_history += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )


    # =====================================================
    # Store User Message
    # =====================================================

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })


    # =====================================================
    # Display User Message
    # =====================================================

    with st.chat_message("user"):

        st.markdown(user_question)


    # =====================================================
    # Run Agent
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner("🤖 Analyzing your question..."):

            try:

                # -----------------------------------------
                # Invoke LangGraph Agent
                # -----------------------------------------

                result = agent_app.invoke({

                    "user_query": user_question,

                    "conversation_history":
                        conversation_history,

                    "plan": "",

                    "tool_name": "",

                    "tool_result": "",

                    "final_answer": ""
                })


                # -----------------------------------------
                # Get Results Safely
                # -----------------------------------------

                final_answer = result.get(
                    "final_answer",
                    "I could not generate an answer."
                )

                plan = result.get(
                    "plan",
                    "No plan available."
                )

                tool_name = result.get(
                    "tool_name",
                    "No tool used."
                )

                tool_result = result.get(
                    "tool_result",
                    "No tool result available."
                )


                # =========================================
                # Display Final Answer
                # =========================================

                st.subheader("💡 Answer")

                st.markdown(final_answer)


                # =========================================
                # DISPLAY GENERATED CHART
                # =========================================

                if (
                    isinstance(tool_result, str)
                    and tool_result.strip().lower().endswith(".png")
                ):

                    st.subheader("📊 Chart")

                    st.image(
                        tool_result,
                        use_container_width=True
                    )


                # =========================================
                # Display Analysis Details
                # =========================================

                with st.expander("🔍 View analysis details"):

                    st.markdown("### 🧠 Plan")

                    st.write(plan)


                    st.markdown("### 🛠️ Tool Used")

                    st.write(tool_name)


                    st.markdown("### 📊 Tool Result")

                    st.write(tool_result)


                # =========================================
                # Store Assistant Response
                # =========================================

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": final_answer

                })


            # =============================================
            # Error Handling
            # =============================================

            except Exception as e:

                st.error(
                    "❌ The agent could not process your question."
                )

                with st.expander("View error details"):

                    st.exception(e)