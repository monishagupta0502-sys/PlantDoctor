import time
import streamlit as st
from utils.chatbot import get_ai_response

st.set_page_config(
    page_title="PlantDoctor AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# PAGE TITLE
# ============================================================

username = st.session_state.get("username", "Guest")

st.title("🤖 PlantDoctor AI Assistant")

st.markdown(
    f"""
### Welcome back, **{username}**!

I'm your personal AI assistant for plant diseases, treatments,
prevention and crop care.
"""
)

# ============================================================
# CURRENT DIAGNOSIS
# ============================================================

last_plant = st.session_state.get("last_plant")
last_disease_name = st.session_state.get("last_disease_name")
last_disease = st.session_state.get("last_disease")
last_confidence = st.session_state.get("last_confidence")

if last_plant and last_disease_name:

    st.success("🌿 Latest AI Diagnosis")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🌱 Plant", last_plant)

    with c2:
        st.metric("🦠 Disease", last_disease_name)

    with c3:
        if last_confidence is not None:
            st.metric(
                "🎯 Confidence",
                f"{last_confidence*100:.2f}%"
            )

    st.info(
        f"""
Hi **{username}** 👋

Your latest diagnosis is **{last_disease_name}**.

You can ask:

• How do I treat this?

• What are the symptoms?

• Is this disease serious?

• How can I prevent it?

• Will today's weather make it worse?
"""
    )

else:

    st.warning(
        "📷 Upload a leaf image first to unlock personalized AI assistance."
    )

# ============================================================
# QUICK QUESTIONS
# ============================================================

st.subheader("⚡ Quick Questions")

b1, b2, b3 = st.columns(3)

prompt = None

with b1:
    if st.button("💊 Treatment"):
        prompt = "How do I treat this?"

with b2:
    if st.button("🛡 Prevention"):
        prompt = "How can I prevent this?"

with b3:
    if st.button("🔍 Symptoms"):
        prompt = "What are the symptoms?"

# Chat input overrides button if user types something
user_input = st.chat_input("Ask PlantDoctor AI...")

if user_input:
    prompt = user_input

# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# AI RESPONSE
# ============================================================

if prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = get_ai_response(
        prompt,
        last_disease
    )

    with st.chat_message("assistant"):

        placeholder = st.empty()

        text = ""

        for word in response.split():

            text += word + " "

            placeholder.markdown(text + "▌")

            time.sleep(0.02)

        placeholder.markdown(text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )