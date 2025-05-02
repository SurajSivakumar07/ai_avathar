import streamlit as st
import requests
import json
from uuid import uuid4

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

# Streamlit UI
st.title("🎓 AI Coach Orchestrator")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
    st.session_state.chat_log = []
    st.session_state.coach = None

# Function to make API calls
def make_api_call(endpoint, data=None, files=None, params=None):
    try:
        url = f"{BACKEND_URL}/{endpoint}"
        if files:
            response = requests.post(url, files=files, params=params)
        else:
            response = requests.post(url, json=data, params=params)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Start Session Section
if not st.session_state.session_id:
    st.header("Start a New Session")
    with st.form("start_session_form"):
        age_group = st.selectbox("Select Age Group", ["", "Grade 6-8", "Grade 9-12"], index=0)
        role = st.selectbox("Select Role", ["", "Goal Partner", "Study Guru", "Life Coach", "Cheerleader", "Career Compass", "Agony Aunt", "Guru Guide"], index=0)
        tone = st.selectbox("Select Tone", ["", "Friendly", "Wise", "Strict", "Calm"], index=0)
        language = st.selectbox("Select Language", ["", "English", "Hindi"], index=0)
        submit_session = st.form_submit_button("🚀 Start Session")

        if submit_session and age_group and role and tone and language:
            data = {
                "age_group": age_group,
                "coach": "",  # Coach is determined by backend
                "role": role,
                "tone": tone,
                "language": language
            }
            with st.spinner("Starting session..."):
                response, status = make_api_call("start_session", data)
                print(f"Start session response: {response}, Status: {status}")
            if status == 200 and "session_id" in response:
                st.session_state.session_id = response["session_id"]
                st.session_state.coach = response.get("message", "").split("with ")[-1] or "Unknown"
                st.session_state.chat_log.append({"role": "system", "text": f"Session started with {role}"})
                st.success(f"Session started with {st.session_state.coach}! Session ID: {st.session_state.session_id}")
            else:
                st.error(response.get("error", "Failed to start session. Please try again."))

# Goal Setting and Chat Section
if st.session_state.session_id:
    # Set Goal Section
    st.header("🎯 Set Your Academic or Life Goal")
    with st.form("set_goal_form"):
        goal = st.text_input("e.g., Crack NEET in 2026, Become more focused")
        submit_goal = st.form_submit_button("Set Goal")

        if submit_goal and goal:
            data = {
                "session_id": st.session_state.session_id,
                "goal": goal
            }
            with st.spinner("Setting goal..."):
                response, status = make_api_call("set_goal", data)
                print(f"Set goal response: {response}, Status: {status}")
            if status == 200:
                st.session_state.coach = response.get("coach", st.session_state.coach)
                st.session_state.chat_log.append({"role": "system", "text": f"🎯 Goal set: {goal}"})
                st.success("Goal set successfully!")
            else:
                st.error(response.get("error", "Failed to set goal. Please try again."))

    # Chat Section
    st.header(f"Chat with Your Coach ({st.session_state.coach})")

    # Display chat history
    chat_container = st.empty()
    with chat_container.container():
        for msg in st.session_state.chat_log:
            if msg["role"] == "user":
                st.markdown(f"**You**: {msg['text']}")
            elif msg["role"] == "coach":
                st.markdown(f"**Coach**: {msg['text']}")
            else:
                st.markdown(f"**System**: {msg['text']}")
            st.markdown("---")

    # Chat input form
    with st.form("chat_form_unique"):
        user_message = st.text_area("Ask your coach something...")
        submit_message = st.form_submit_button("Send")

        if submit_message and user_message.strip():
            if not st.session_state.session_id:
                st.error("No active session. Please start a new session.")
            else:
                print(f"Sending chat with session_id = {st.session_state.session_id}, message = {user_message}")
                st.session_state.chat_log.append({"role": "user", "text": user_message})
                data = {
                    "session_id": st.session_state.session_id,
                    "message": user_message
                }
                with st.spinner("Sending message to coach..."):
                    response, status = make_api_call("chat", data)
                    print(f"Chat API response: {response}, Status: {status}")
                if status == 200 and "error" not in response:
                    coach_reply = response.get("response", "No response from coach")
                    st.session_state.chat_log.append({"role": "coach", "text": coach_reply})
                    print(f"Coach reply added to chat log: {coach_reply}")
                    st.success("Message sent!")
                    st.rerun()  # Refresh UI to display new message
                else:
                    st.error(response.get("error", "Failed to process message. Please try again or start a new session."))
    # Section: Audio chat
    st.subheader("🎙️ Or upload audio")
    audio_file = st.file_uploader("Upload audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

    # Initialize flag to track audio processing
    if "audio_processed" not in st.session_state:
        st.session_state.audio_processed = False

    if audio_file and not st.session_state.audio_processed:
        if not st.session_state.session_id:
            st.error("No active session. Please start a new session.")
        else:
            with st.spinner("Transcribing and getting response..."):
                files = {"file": (audio_file.name, audio_file, "multipart/form-data")}
                params = {"session_id": st.session_state.session_id}
                response, status = make_api_call("audio_chat", data=None, files=files, params=params)

                if status == 200 and "error" not in response:
                    transcript = response.get("transcript", "")
                    reply = response.get("response", "")
                    st.session_state.chat_log.append({"role": "user", "text": transcript})
                    st.session_state.chat_log.append({"role": "coach", "text": reply})
                    st.success("Audio processed successfully!")

                    # Set flag to True to prevent rerun loop
                    st.session_state.audio_processed = True
                    st.rerun()
                else:
                    st.error(response.get("error", "Failed to process audio."))

    # Switch Coach Section
    st.subheader("🔄 Switch Coach")
    available_coaches = ["tara", "ravi"]
    other_coach = [c for c in available_coaches if c != st.session_state.coach.lower()]

    if other_coach:
        new_coach = st.selectbox("Choose a coach", other_coach)
        if st.button("Switch Coach"):
            data = {
                "session_id": st.session_state.session_id,
                "new_coach": new_coach
            }
            with st.spinner("Switching coach..."):
                response, status = make_api_call("switch_coach", data)
                print(f"Switch coach response: {response}, Status: {status}")
            if status == 200 and "coach" in response:
                st.session_state.coach = response["coach"]
                st.session_state.chat_log.append({
                    "role": "system",
                    "text": f"🔁 Coach switched to {response['coach']}"
                })
                st.success(response["message"])
                st.rerun()
            else:
                st.error(response.get("error", "Failed to switch coach. Please try again."))
