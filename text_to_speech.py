# import streamlit as st
# import os
# import time

# # Function to play video
# def play_video(video_path):
#     video_file = open(video_path, 'rb')
#     video_bytes = video_file.read()
#     st.video(video_bytes)
#     video_file.close()

# # Function to check and play videos based on words
# def check_and_play_videos(sentence):
#     words = sentence.split()  # Split the sentence into words

#     for word in words:
#         video_path = f"{word}.mp4"  # Assuming videos are named after the words with .mp4 extension
#         if os.path.exists(video_path):
#             st.write(f"Playing video for: {word}")
#             play_video(video_path)
#             time.sleep(2)  # Wait 2 seconds before playing the next video
#         else:
#             st.write(f"Video not found for: {word}")

# # Streamlit app
# st.title("Sentence to Video Player")

# sentence = st.text_input("Enter a sentence:")

# if sentence:
#     check_and_play_videos(sentence)
import streamlit as st
import os
import tempfile
import soundfile as sf
from groq import Groq
from io import BytesIO

# Set up your Groq API key
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Streamlit App Header
st.title("Audio to English Translation using Groq API")

# Step 1: Record or Upload Audio
st.header("Record or Upload Audio")
audio_input_method = st.radio("Choose Input Method", ("Record Audio", "Upload Audio File"))

# Step 2: Handle Audio Input (Recording or Uploading)
audio_file = None

if audio_input_method == "Record Audio":
    # Record Audio using Streamlit
    audio_data = st.audio(st.audio("record_audio"), format="wav")
    
    if audio_data:
        audio_file = BytesIO(audio_data)
        st.success("Audio recorded successfully!")

elif audio_input_method == "Upload Audio File":
    # Upload Audio
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "webm", "mp4"])
    if uploaded_file is not None:
        audio_file = uploaded_file
        st.success("Audio file uploaded successfully!")

# Step 3: Convert Audio (if needed) to ensure compatibility
def convert_audio_to_wav(audio_file):
    # Use soundfile to convert and return as .wav format (Groq API expects .wav files)
    data, samplerate = sf.read(audio_file)
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_file.name, data, samplerate)
    return temp_file.name

# Step 4: Use Groq API to Translate Audio to English
def translate_audio_to_english(audio_path):
    # Open the audio file and use Groq API to get the translation
    with open(audio_path, "rb") as file:
        translation = client.audio.translations.create(
            file=(audio_path, file.read()),        # Required audio file
            model="whisper-large-v3",              # Required model for translation (multilingual)
            prompt="Optional context",             # Optional: Specify context or spelling
            response_format="json",                # Optional: json or text
            temperature=0.0                        # Optional: Creativity control
        )
        return translation.text

# Step 5: Trigger the Translation after Audio is Provided
if audio_file:
    # Convert to WAV format if needed
    audio_path = convert_audio_to_wav(audio_file)

    # Step 6: Get and Display Translation from Groq API
    if st.button("Translate Audio to English"):
        translated_text = translate_audio_to_english(audio_path)
        st.header("Translated English Text")
        st.write(translated_text)