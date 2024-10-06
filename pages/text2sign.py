import os
import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

import base64
from groq import Groq




# # Initialize the Groq client with API key (replace "YOUR_API_KEY" with actual API key)
# API = "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"
# client = Groq(api_key=API)

# # Function for audio-to-text conversion using Groq
# def audio_to_text(audio_file):
#     try:
#         # Use the Groq client to translate the audio file
#         translation = client.audio.translations.create(
#             file=("audio.wav", audio_file.read()),  # Pass the audio file
#             model="whisper-large-v3",               # Model for translation
#             prompt="Optional context",              # Optional context or prompt
#             response_format="json",                 # Get the response in JSON format
#             temperature=0.0                         # Deterministic output
#         )
#         return translation.text  # Return the translated text
#     except Exception as e:
#         st.error(f"Error during audio translation: {str(e)}")
#         return None
# Dummy function for audio-to-text conversion
def audio_to_text(audio_file):
    # Replace with your actual implementation
    return "he is happy"

# Function to concatenate and play videos
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

# Function to handle sentence-to-sign process
def sentence_to_sign(sentence):
    if sentence:
        video_paths = check_and_collect_videos(sentence)
        if video_paths:
            concatenate_and_play_videos(video_paths)
        else:
            st.write("No videos found to play.")
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
            margin-bottom: 5px; /* Reduce bottom margin */
        }
        .content {
            text-align: justify;
            font-weight: bold;
            background: linear-gradient(45deg, #FF5733, #FF6F61);
            font-size: 20px; /* Enlarged font size */
            max-width: 800px; /* Ensure content width */
            background: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
            border-radius: 10px;
            padding: 5px; /* Added padding for content */
            margin-bottom: 5px; /* Reduce margin to decrease space between elements */
        }
    </style>

""", unsafe_allow_html=True)


# Streamlit UI
st.markdown("<h1 class='title'>Indian Sign language Recognition</h1>"

# Audio Upload Feature

"<h1 class='content'>Upload Audio to Convert to Sign Language</h1>"
 , unsafe_allow_html=True)
 
uploaded_audio = st.file_uploader("Choose an audio file", type=["m4a", "mp3", "wav"])

if uploaded_audio:
    with st.spinner("Converting audio to text..."):
        # Read the audio file
        audio_bytes = uploaded_audio.read()
        # Convert audio bytes to text
        sentence = audio_to_text(BytesIO(audio_bytes))
        st.write(f"Converted Text: {sentence}")
        # Convert the text to sign language
        sentence_to_sign(sentence)

# Text-to-Sign Feature
st.markdown(
"""<h1 class='content'>Enter Text to Convert to Sign Language</h1>"""
 , unsafe_allow_html=True)

sentence_input = st.text_input("Enter a sentence:", placeholder="Hello, how are you?")
if st.button("Convert"):
    if sentence_input:
        sentence_to_sign(sentence_input)
    else:
        st.write("Please enter a sentence.")





# import os
# import numpy as np
# import streamlit as st
# from moviepy.editor import VideoFileClip, concatenate_videoclips
# from io import BytesIO
# from pydub import AudioSegment
# from pydub.playback import play
# from gtts import gTTS
# import speech_recognition as sr  # For audio-to-text conversion

# # Define CSS styles for gradient text, content background effects, and button
# st.markdown("""
#     <style>
#         body {
#             background: linear-gradient(135deg, #FFDDC1, #FFABAB);
#             margin: 0;
#             padding: 0;
#             font-family: Arial, sans-serif;
#         }
#         .title {
#             font-size: 36px;
#             font-family: 'Arial Black', Gadget, sans-serif;
#             font-weight: bold;
#             background: linear-gradient(45deg, #FF5733, #FF6F61);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: red;
#             background-clip: text;
#             text-fill-color: red;
#             text-align: left;
#             margin-top: 20px;
#             margin-bottom: 10px;
#         }
#         .content {
#             text-align: justify;
#             font-weight: bold;
#             background: linear-gradient(45deg, #FF5733, #FF6F61);
#             font-size: 20px;
#             max-width: 800px;
#             background: rgba(255, 255, 255, 0.8);
#             border-radius: 10px;
#             padding: 10px;
#             margin-bottom: 10px;
#         }
#         .stTextInput {
#             margin-top: 5px;
#         }
#     </style>
# """, unsafe_allow_html=True)
# def audio_to_text(audio_file):
#     recognizer = sr.Recognizer()
    
#     # Convert the uploaded audio file to WAV format using pydub
#     try:
#         # Load the audio file with pydub
#         audio = AudioSegment.from_file(audio_file)
#         # Convert to WAV format
#         wav_io = io.BytesIO()
#         audio.export(wav_io, format="wav")
#         wav_io.seek(0)  # Rewind the BytesIO object to the beginning
        
#         # Use SpeechRecognition to convert the WAV file to text
#         with sr.AudioFile(wav_io) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data)
#             return text
#     except sr.UnknownValueError:
#         st.error("Could not understand audio.")
#         return None
#     except sr.RequestError:
#         st.error("Could not request results from Google Speech Recognition service.")
#         return None
#     except Exception as e:
#         st.error(f"Error processing audio file: {str(e)}")
#         return None
# # Function to convert audio to text using SpeechRecognition
# # def audio_to_text(audio_file):
# #     recognizer = sr.Recognizer()
# #     audio_data = sr.AudioFile(audio_file)
# #     with audio_data as source:
# #         audio = recognizer.record(source)
# #     try:
# #         text = recognizer.recognize_google(audio)
# #         return text
# #     except sr.UnknownValueError:
# #         st.error("Could not understand audio.")
# #         return None
# #     except sr.RequestError:
# #         st.error("Could not request results from Google Speech Recognition service.")
# #         return None

# # Function to concatenate and play videos
# def concatenate_and_play_videos(video_paths):
#     clips = []
#     for video_path in video_paths:
#         clip = VideoFileClip(video_path)
#         clip = clip.subclip(0, clip.duration)  # Ensure the clip is using the full duration
#         clips.append(clip)

#     # Ensure all clips have the same fps
#     fps = clips[0].fps
#     for clip in clips:
#         if clip.fps != fps:
#             clip = clip.set_fps(fps)
    
#     final_clip = concatenate_videoclips(clips, method="compose")
    
#     final_clip_path = "output.mp4"
#     final_clip.write_videofile(final_clip_path, codec="libx264", audio_codec="aac")

#     # Display the final concatenated video
#     with open(final_clip_path, 'rb') as video_file:
#         video_bytes = video_file.read()
#         st.video(video_bytes)

# # Function to check and collect video paths based on words
# def check_and_collect_videos(sentence):
#     words = sentence.split()  # Split the sentence into words
#     video_paths = []

#     for word in words:
#         video_path = f"Video/{word}.mp4"  # Assuming videos are named after the words with .mp4 extension
#         if os.path.exists(video_path):
#             video_paths.append(video_path)
#         else:
#             st.write(f"Video not found for: {word}")

#     return video_paths

# def sentence_to_sign(sentence):
#     if sentence:
#         video_paths = check_and_collect_videos(sentence)
#         if video_paths:
#             concatenate_and_play_videos(video_paths)
#         else:
#             st.write("No videos found to play.")

# # Streamlit UI
# st.markdown("<h1 class='title'>Convert Sentence to Sign Language</h1>", unsafe_allow_html=True)

# # Audio Upload Feature
# st.header("Upload Audio to Convert to Sign Language")
# uploaded_audio = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

# if uploaded_audio:
#     with st.spinner("Converting audio to text..."):
#         # Convert audio bytes to text
#         sentence = audio_to_text(uploaded_audio)
#         if sentence:
#             st.write(f"Converted Text: {sentence}")
#             # Convert the text to sign language
#             sentence_to_sign(sentence)

# # Text-to-Sign Feature
# st.header("Or Enter Text Directly")
# sentence_input = st.text_input("Enter a Sentence", placeholder="Hello, how are you?")

# if st.button("Convert"):
#     if sentence_input:
#         sentence_to_sign(sentence_input)
#     else:
#         st.write("Please enter a sentence.")
