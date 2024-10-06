import os
import streamlit as st
import time

def play_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    video_file.close()


# Function to check and play videos based on words
def check_and_play_videos(sentence):
    words = sentence.split()  # Split the sentence into words

    for word in words:
        video_path = f"Video/{word}.mp4"  # Assuming videos are named after the words with .mp4 extension
        if os.path.exists(video_path):
            st.write(f"Playing video for: {word}")
            play_video(video_path)
            time.sleep(2)  # Wait 2 seconds before playing the next video
        else:
            pass
            # st.write(f"Video not found for: {word}")
st.markdown("""
    <style>

        body {

        .title {
            font-size: 36px; /* Adjust title size */
            font-family: 'Arial Black', Gadget, sans-serif;
            font-weight: bold;
            background: linear-gradient(45deg, #FF5733, #FF6F61);
            -webkit-background-clip: text;
            -webkit-text-fill-color: red;
            background-clip: text;
            text-fill-color: red;
            text-align: left;
            margin-top: 20px;
            margin-bottom: 10px; /* Reduce bottom margin */
        }
    </style>

""", unsafe_allow_html=True)

st.markdown("""<h1 class='title'>Text to Sign language Conversion </h1>""", unsafe_allow_html=True)


sentence = st.text_input("Enter a sentence to convert to sign language:", placeholder="Hello")
sentence=sentence.lower()
if sentence:
        check_and_play_videos(sentence)

        