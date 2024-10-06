# import streamlit as st
# from streamlit.components.v1 import html

# def audio_recorder():
#     html_code = """
#     <script>
#     let recording = false;
#     let mediaRecorder;
#     let audioChunks = [];
    
#     function startRecording() {
#         if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
#             navigator.mediaDevices.getUserMedia({ audio: true })
#                 .then(stream => {
#                     mediaRecorder = new MediaRecorder(stream);
#                     mediaRecorder.ondataavailable = event => {
#                         audioChunks.push(event.data);
#                     };
#                     mediaRecorder.onstop = () => {
#                         const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
#                         const audioUrl = URL.createObjectURL(audioBlob);
#                         const audio = new Audio(audioUrl);
#                         audio.controls = true;
#                         document.getElementById('audio_player').src = audioUrl;
#                         const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
#                         document.getElementById('audio_file').files = new DataTransfer().files;
#                     };
#                     mediaRecorder.start();
#                     recording = true;
#                 });
#         }
#     }
    
#     function stopRecording() {
#         if (mediaRecorder && recording) {
#             mediaRecorder.stop();
#             recording = false;
#         }
#     }
#     </script>
#     <button onclick="startRecording()">Start Recording</button>
#     <button onclick="stopRecording()">Stop Recording</button>
#     <br><br>
#     <audio id="audio_player" controls></audio>
#     <input type="file" id="audio_file" style="display:none;">
#     """
    
#     st.components.v1.html(html_code, height=200)

#     # Capture the uploaded audio file
#     if st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a"]):
#         uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])
#         if uploaded_file:
#             st.audio(uploaded_file, format='audio/wav')

# # Main function to handle the sentence-to-sign process
# def main():
#     st.title("Indian Sign Language Converter")

#     st.header("Record or Upload Audio to Convert to Sign Language")
#     audio_recorder()
    
#     # Add more functionality here based on audio input
#     # ...

# if __name__ == "__main__":
#     main()




import os
import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import base64
from groq import Groq

# Initialize the Groq client with API key (replace "YOUR_API_KEY" with actual API key)
API = "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"
client = Groq(api_key=API)

# Function for audio-to-text conversion using Groq
def audio_to_text(audio_file):
    try:
        # Use the Groq client to translate the audio file
        translation = client.audio.translations.create(
            file=("audio.wav", audio_file.read()),  # Pass the audio file
            model="whisper-large-v3",               # Model for translation
            prompt="Optional context",              # Optional context or prompt
            response_format="json",                 # Get the response in JSON format
            temperature=0.0                         # Deterministic output
        )
        return translation.text  # Return the translated text
    except Exception as e:
        st.error(f"Error during audio translation: {str(e)}")
        return None
# # Dummy function for audio-to-text conversion
# def audio_to_text(audio_file):
#     # Replace with your actual implementation
#     return "translated text from audio"

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

# Audio recorder using HTML and JS
def audio_recorder():
    html_code = """
    <script>
    let recording = false;
    let mediaRecorder;
    let audioChunks = [];
    
    function startRecording() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.ondataavailable = event => {
                        audioChunks.push(event.data);
                    };
                    mediaRecorder.onstop = () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        const audioUrl = URL.createObjectURL(audioBlob);
                        const audio = new Audio(audioUrl);
                        audio.controls = true;
                        document.getElementById('audio_player').src = audioUrl;

                        const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const audioBase64 = e.target.result.split(',')[1];
                            document.getElementById('audio_base64').value = audioBase64;
                        };
                        reader.readAsDataURL(audioFile);
                    };
                    mediaRecorder.start();
                    recording = true;
                });
        }
    }
    
    function stopRecording() {
        if (mediaRecorder && recording) {
            mediaRecorder.stop();
            recording = false;
        }
    }
    </script>
    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>
    <br><br>
    <audio id="audio_player" controls></audio>
    <input type="hidden" id="audio_base64" name="audio_base64">
    """
    
    st.components.v1.html(html_code, height=300)

    audio_base64 = st.text_input("Recorded Audio (Base64):")
    return audio_base64

# Main function to handle the entire flow
def main():
    st.title("Indian Sign Language Converter")

    # Audio Upload Feature
    st.header("Record or Upload Audio to Convert to Sign Language")
    
    # Record Audio
    st.subheader("Record Audio:")
    recorded_audio_base64 = audio_recorder()
    
    # Audio Upload Option
    st.subheader("Upload Audio:")
    uploaded_audio = st.file_uploader("Choose an audio file", type=["m4a", "mp3", "wav"])

    if recorded_audio_base64:
        # If the user recorded an audio
        audio_bytes = BytesIO(base64.b64decode(recorded_audio_base64))
        sentence = audio_to_text(audio_bytes)
        st.write(f"Converted Text from Recorded Audio: {sentence}")
        sentence_to_sign(sentence)
    elif uploaded_audio:
        # If the user uploaded an audio file
        with st.spinner("Converting audio to text..."):
            audio_bytes = uploaded_audio.read()
            sentence = audio_to_text(BytesIO(audio_bytes))
            st.write(f"Converted Text: {sentence}")
            sentence_to_sign(sentence)

    # Text-to-Sign Feature
    st.header("Or Enter Text to Convert to Sign Language")
    sentence_input = st.text_input("Enter a sentence:")
    if st.button("Convert Text to Sign Language"):
        if sentence_input:
            sentence_to_sign(sentence_input)
        else:
            st.write("Please enter a sentence.")

if __name__ == "__main__":
    main()
