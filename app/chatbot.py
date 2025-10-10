import streamlit as st

st.set_page_config(page_title="Wellness Chatbot", page_icon=":speech_balloon:", layout="centered")

st.title("Wellness Chatbot")
st.subheader("Depression Risk Screening")

questions = [
    "Have you felt down, sad, or hopeless often recently?",
    "Have you lost interest in activities you usually enjoy?",
    "Do you have trouble sleeping or sleep too much?",
    "Do you feel tired often or have low energy?",
    "Have you had thoughts of self-harm or suicide?"
]

# Initialize/restore conversation history and screening status
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [("bot", "Hi! I'm here to support your mental wellbeing. Type below or click 'Start screening'.")]
if 'screening' not in st.session_state:
    st.session_state.screening = False
if 'screening_idx' not in st.session_state:
    st.session_state.screening_idx = 0
if 'screening_answers' not in st.session_state:
    st.session_state.screening_answers = []

# Render conversation
for who, msg in st.session_state.chat_history:
    if who == "bot":
        st.markdown(f"<div style='background:#eaf1fb;border-radius:14px;padding:10px;margin:9px 0;color:#22304a'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#ffeaa7;border-radius:14px;padding:10px;margin:9px 0;text-align:right;color:#5f432f'>{msg}</div>", unsafe_allow_html=True)

# Button to start screening
if not st.session_state.screening and st.button("Start screening"):
    st.session_state.screening = True
    st.session_state.screening_idx = 0
    st.session_state.screening_answers = []
    next_q = questions[0]
    st.session_state.chat_history.append(("bot", next_q))
    st.experimental_rerun()

# Screening question: Yes/No buttons
if st.session_state.screening and st.session_state.screening_idx < len(questions):
    q_idx = st.session_state.screening_idx
    col1, col2 = st.columns(2)
    if col1.button("Yes", key=f"yes_{q_idx}"):
        st.session_state.chat_history.append(("user", "Yes"))
        st.session_state.screening_answers.append("Yes")
        st.session_state.screening_idx += 1
        if st.session_state.screening_idx < len(questions):
            next_q = questions[st.session_state.screening_idx]
            st.session_state.chat_history.append(("bot", next_q))
        st.experimental_rerun()
    if col2.button("No", key=f"no_{q_idx}"):
        st.session_state.chat_history.append(("user", "No"))
        st.session_state.screening_answers.append("No")
        st.session_state.screening_idx += 1
        if st.session_state.screening_idx < len(questions):
            next_q = questions[st.session_state.screening_idx]
            st.session_state.chat_history.append(("bot", next_q))
        st.experimental_rerun()

# If screening ended: show result
if st.session_state.screening and st.session_state.screening_idx == len(questions):
    score = sum(1 for a in st.session_state.screening_answers if a == "Yes")
    if score >= 3:
        result = "Based on your answers, you may be at risk for depression. Please reach out to a professional."
    elif score >= 1:
        result = "You show some symptoms. Consider self-care, talking to friends or professionals if you feel unwell."
    else:
        result = "No significant symptoms detected at this time. Stay well and take care!"
    st.session_state.chat_history.append(("bot", result))
    st.session_state.screening = False
    st.experimental_rerun()

# Text input for free chat (always available)
user_input = st.text_input("Type your message:", key="user_input")
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    # Bot basic response
    if user_input.lower() in ["hi", "hello"]:
        bot_response = "Hello! Type 'Start screening' to begin assessment, or just keep chatting."
    elif "screening" in user_input.lower():
        st.session_state.screening = True
        st.session_state.screening_idx = 0
        st.session_state.screening_answers = []
        next_q = questions[0]
        bot_response = next_q
    else:
        bot_response = "Thank you for sharing. If you'd like to do depression screening, type 'Start screening' or click the button."
    st.session_state.chat_history.append(("bot", bot_response))
    st.experimental
