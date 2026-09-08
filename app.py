import streamlit as st
from google import genai

client = genai.Client()

st.title("🤖 My Gemini Career Assistant")
st.write("Your personal AI career guide 🎓")

# Student profile
st.subheader("🎓 Student Profile")

branch = st.selectbox(
    "Your Branch",
    ["ECE", "CSE", "EEE", "Mechanical", "Civil", "Other"]
)

skills = st.text_input(
    "Your Skills",
    placeholder="Example: Python, Electronics, C programming"
)

interests = st.text_input(
    "Your Interests",
    placeholder="Example: AI, Robotics, Embedded Systems"
)

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_id" not in st.session_state:
    st.session_state.previous_id = None

# Clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.previous_id = None
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User question
question = st.chat_input("Ask about your career...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    prompt = f"""
You are a helpful College Career Assistant.

Student profile:
Branch: {branch}
Skills: {skills}
Interests: {interests}

Student question:
{question}

Give practical and personalized career guidance based on the student's profile.
Explain your answer clearly and suggest useful next steps.
"""

    if st.session_state.previous_id is None:
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt
        )
    else:
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            previous_interaction_id=st.session_state.previous_id,
            input=prompt
        )

    answer = interaction.output_text

    st.session_state.previous_id = interaction.id

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)