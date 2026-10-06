import streamlit as st
import requests
from pydantic import BaseModel
from faster_whisper import WhisperModel

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Interview Preparation System",
    page_icon="🎯",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🎯 AI Interview Preparation System")
st.write("Prepare for technical and HR interviews using AI.")

# ---------------- USER INPUT ----------------
name = st.text_input("Enter your name")

role = st.text_input(
    "Enter your target job role",
    placeholder="Example: Python Developer"
)

difficulty = st.selectbox(
    "Select difficulty",
    ["Easy", "Medium", "Hard"]
)

# ---------------- INTERVIEW QUESTION ----------------
if st.button("Start Interview"):

    if not name or not role:
        st.error("Please enter your name and job role.")

    else:
        st.success("Interview started!")

        st.subheader("💬 Interview Question")

        if difficulty == "Easy":
            question = f"What is {role} and what are its basic responsibilities?"

        elif difficulty == "Medium":
            question = f"What skills are important for a {role}, and how have you developed them?"

        else:
            question = f"Describe a difficult problem you might face as a {role} and explain how you would solve it."

        st.write(question)

# ---------------- ANSWER ----------------
st.subheader("📝 Your Answer")

answer = st.text_area(
    "Type your interview answer here",
    height=150
)

if st.button("Evaluate Answer"):

    if not answer:
        st.warning("Please enter your answer first.")

    else:
        word_count = len(answer.split())

        st.success("Answer submitted!")

        st.write("### 📊 Basic Evaluation")

        if word_count < 20:
            st.warning("Your answer is too short. Try to explain it in more detail.")
        elif word_count < 50:
            st.info("Good start. Add examples to make your answer stronger.")
        else:
            st.success("Good! Your answer has enough detail.")

        st.write("**Word Count:**", word_count)

        st.write("**Suggestions:**")
        st.write("- Explain your answer clearly.")
        st.write("- Give a practical example.")
        st.write("- Avoid unnecessary information.")
        st.write("- Speak confidently.")

# ---------------- VOICE FEATURE ----------------
st.subheader("🎤 Voice Interview")

audio = st.file_uploader(
    "Upload your recorded answer",
    type=["wav", "mp3", "m4a"]
)

if audio is not None:

    st.audio(audio)

    if st.button("Convert Voice to Text"):

        with open("audio_input", "wb") as f:
            f.write(audio.getbuffer())

        try:
            with st.spinner("Converting voice to text..."):

                model = WhisperModel(
                    "base",
                    device="cpu",
                    compute_type="int8"
                )

                segments, info = model.transcribe("audio_input")

                transcript = ""

                for segment in segments:
                    transcript += segment.text + " "

            st.subheader("📝 Transcribed Answer")
            st.write(transcript)

        except Exception as e:
            st.error("Voice processing failed.")
            st.write(e)