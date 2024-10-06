import cv2
import os
import numpy as np
import mediapipe as mp
from keras.models import load_model

from gtts import gTTS
import streamlit as st
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Define CSS styles for gradient text, content background effects, and button
st.markdown("""
    <style>

        body {
            background: linear-gradient(135deg, #FFDDC1, #FFABAB);
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
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
        .content {
            text-align: justify;
            font-weight: bold;
            background: linear-gradient(45deg, #FF5733, #FF6F61);
            font-size: 20px; /* Enlarged font size */
            max-width: 800px; /* Ensure content width */
            background: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
            border-radius: 10px;
            padding: 10px; /* Added padding for content */
            margin-bottom: 10px; /* Reduce margin to decrease space between elements */
        }
        .stTextInput {
            margin-top: 5px; /* Reduce gap between label and input */
        }
    </style>
""", unsafe_allow_html=True)

def concatenate_and_play_videos(video_paths):
    clips = []
    for video_path in video_paths:
        clip = VideoFileClip(video_path)
        clip = clip.subclip(0, clip.duration)  # Ensure the clip is using the full duration
        clips.append(clip)

    # Ensure all clips have the same fps
    fps = clips[0].fps
    for clip in clips:
        if clip.fps != fps:
            clip = clip.set_fps(fps)
    
    final_clip = concatenate_videoclips(clips, method="compose")
    
    final_clip_path = "output.mp4"
    final_clip.write_videofile(final_clip_path, codec="libx264", audio_codec="aac")

    # Display the final concatenated video
    with open(final_clip_path, 'rb') as video_file:
        video_bytes = video_file.read()
        st.video(video_bytes)

# Function to check and collect video paths based on words
def check_and_collect_videos(sentence):
    words = sentence.split()  # Split the sentence into words
    video_paths = []

    for word in words:
        video_path = f"Video/{word}.mp4"  # Assuming videos are named after the words with .mp4 extension
        if os.path.exists(video_path):
            video_paths.append(video_path)
        else:
            st.write(f"Video not found for: {word}")

    return video_paths

def sentence_to_sign():
    st.markdown("""<h1 class='title'>Convert Sentence to Sign Language</h1>""", unsafe_allow_html=True)
    # Text input with a placeholder
    sentence = st.text_input("Enter a Sentence ", placeholder="Hello, how are you?")
    
    if sentence:
        video_paths = check_and_collect_videos(sentence)
        if video_paths:
            concatenate_and_play_videos(video_paths)
        else:
            pass
            # st.write("No videos found to play.")
    

sentence_to_sign()
