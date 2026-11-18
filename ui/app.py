
import requests
import streamlit as st

from ui.feedback import save_feedback
from ui.planner import render_planner


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NPTELPicker AI Assistant",
    page_icon="🎓",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "feedback_saved" not in st.session_state:
    st.session_state.feedback_saved = {}


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎓 NPTELPicker")

st.sidebar.write(
    "Your AI-powered NPTEL course assistant."
)

if st.sidebar.button("➕ New Chat"):
    st.session_state.messages = []
    st.session_state.thread_id = None
    st.session_state.feedback_saved = {}
    st.rerun()

st.sidebar.divider()

st.sidebar.subheader("Backend Status")

try:
    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    if response.status_code == 200:
        st.sidebar.success("Backend Connected")
    else:
        st.sidebar.warning("Backend Unavailable")

except requests.RequestException:
    st.sidebar.error("Backend Disconnected")

st.sidebar.divider()

st.sidebar.caption(
    "Powered by Gemini, RAG, ChromaDB and LangGraph."
)


# ==========================================
# APPLICATION TABS
# ==========================================

chat_tab, planner_tab = st.tabs(
    ["💬 AI Chat Assistant", "📅 Semester Planner"]
)


# ==========================================
# AI CHAT ASSISTANT
# ==========================================

with chat_tab:

    st.title("🎓 NPTELPicker AI Assistant")

    st.write(
        "Ask questions about NPTEL courses, "
        "get recommendations and plan your semester."
    )

    # Reserve the chat-history position above the input.
    # Messages are rendered inside this container.
    chat_container = st.container()

    # Chat input stays after the history container.
    question = st.chat_input(
        "Ask something about NPTEL courses..."
    )

    # ======================================
    # PROCESS NEW QUESTION
    # ======================================

    if question:

        # Save the user's question first.
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        # Show processing status in the chat area.
        with chat_container:

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:

                        payload = {
                            "question": question
                        }

                        if st.session_state.thread_id:

                            payload["thread_id"] = (
                                st.session_state.thread_id
                            )

                        response = requests.post(
                            f"{API_URL}/agent",
                            json=payload,
                            timeout=120
                        )

                        response.raise_for_status()

                        result = response.json()

                        status = result.get("status")

                        answer = result.get(
                            "answer",
                            "No answer received."
                        )

                        sources = result.get("sources", [])

                        if result.get("thread_id"):

                            st.session_state.thread_id = (
                                result["thread_id"]
                            )

                        if status == "approval_required":

                            answer = (
                                "Your course plan requires approval "
                                "before execution. Please use the "
                                "approval workflow in the API."
                            )

                            sources = []

                            st.warning(
                                "Approval is required. "
                                "The course plan has not been executed."
                            )

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })

                    except requests.exceptions.Timeout:

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": (
                                "The backend request timed out. "
                                "Please try again."
                            ),
                            "sources": []
                        })

                    except requests.exceptions.ConnectionError:

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": (
                                "Unable to connect to the NPTELPicker "
                                "backend. Please make sure FastAPI is running."
                            ),
                            "sources": []
                        })

                    except requests.exceptions.RequestException:

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": (
                                "An error occurred while communicating "
                                "with the backend."
                            ),
                            "sources": []
                        })

                    except ValueError:

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": (
                                "The backend returned an invalid response."
                            ),
                            "sources": []
                        })

    # ======================================
    # DISPLAY COMPLETE CHAT HISTORY
    # ======================================

    with chat_container:

        for index, message in enumerate(
            st.session_state.messages
        ):

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

                # DISPLAY SOURCES

                if message.get("sources"):

                    with st.expander("📚 View Sources"):

                        for source in message["sources"]:

                            st.markdown(
                                f"**{source.get('citation', '')} "
                                f"{source.get('title', 'Unknown Course')}**"
                            )

                            st.caption(
                                f"Source: {source.get('source', 'Not available')}"
                            )

                # FEEDBACK FOR ASSISTANT MESSAGES

                if message["role"] == "assistant":

                    feedback_key = f"feedback_{index}"

                    selected_feedback = st.feedback(
                        "thumbs",
                        key=feedback_key
                    )

                    if selected_feedback is not None:

                        if index not in st.session_state.feedback_saved:

                            user_question = ""

                            for previous_message in reversed(
                                st.session_state.messages[:index]
                            ):

                                if previous_message["role"] == "user":

                                    user_question = (
                                        previous_message["content"]
                                    )

                                    break

                            feedback_type = (
                                "positive"
                                if selected_feedback == 1
                                else "negative"
                            )

                            try:

                                save_feedback(
                                    question=user_question,
                                    answer=message["content"],
                                    feedback_type=feedback_type
                                )

                                st.session_state.feedback_saved[index] = (
                                    feedback_type
                                )

                                st.success(
                                    "Thank you! Your feedback has been saved."
                                )

                            except (OSError, ValueError) as error:

                                st.error(
                                    f"Unable to save feedback: {error}"
                                )

                        else:

                            st.caption(
                                "Thank you! Your feedback has been recorded."
                            )


# ==========================================
# SEMESTER PLANNER
# ==========================================

with planner_tab:

    render_planner()
