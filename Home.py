import streamlit as st

# Define CSS styles for gradient text, content background effects
st.markdown("""
    <style>
        .gradient-text {
            font-size: 48px; /* Enlarged font size */
            font-weight: bold;
            background: linear-gradient(45deg, #FF5733, #FF6F61);
            -webkit-background-clip: text;
            -webkit-text-fill-color: red;
            background-clip: text;
            text-fill-color: red;
            margin: 0;
            padding: 0;
            text-align: center;
            display: block;
            width: 100%;
        }
        .content {
            font-size: 20px; /* Increased font size */
            text-align: justify;
            margin: 30px auto; /* Centered and space between title and content */
            max-width: 1200px; /* Increased width for better readability */
            padding: 20px; /* Added padding for better spacing */
        }
        body {
            background: linear-gradient(135deg, #FFDDC1, #FFABAB);
            margin: 0;
            padding: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Title with gradient text
st.markdown("""<h1 class='gradient-text'>Sign Sarthi - Empowering Deaf and Mute People in India</h1>""", unsafe_allow_html=True)

# Add an image
st.image("D:\sih\img\WhatsApp Image 2024-09-06 at 11.24.58_55e09cad.jpg", use_column_width=True)

# Content with styled background
st.markdown("""
    <div class="content">
        <p>
            A revolutionary web application designed to empower deaf and mute people in India. Our platform integrates Indian Sign Language learning with interactive exercises, including alphabets, letters, and sentences. Seamlessly convert Indian text and speech to sign language, track progress through data analytics, and bridge communication gaps. Whether you're a student, teacher, parent, or part of HR, our app offers valuable tools and resources to enhance learning and inclusivity. Join us in creating a supportive and accessible educational environment for all!
        </p>
    </div>
""", unsafe_allow_html=True)
