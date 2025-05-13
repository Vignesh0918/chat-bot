import streamlit as st
import openai
from gtts import gTTS
from io import BytesIO
from dotenv import load_dotenv
import os

# Set your OpenAI API key securely (use env or Streamlit secrets in production)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("💬 Chatbot with Voice Reply")
st.markdown("Type your message and get a voice + text response!")

# User input
user_input = st.text_input("You:")

if st.button("Send") and user_input.strip() != "":
    try:
        # Send user input to OpenAI (GPT-3.5)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a friendly assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response['choices'][0]['message']['content']
        st.text_area("Chatbot says:", value=reply, height=150)

        # Convert reply to speech using gTTS
        tts = gTTS(reply)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Audio output
        st.audio(mp3_fp, format="audio/mp3")

    except Exception as e:
        st.error(f"Error: {e}")
