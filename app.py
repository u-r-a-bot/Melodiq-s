import streamlit as st
import os
from PIL import Image
from database import save_audio_to_db, get_all_audio_files
from utils import save_uploaded_file, UPLOAD_AUDIO_FOLDER, UPLOAD_IMAGE_FOLDER
count = 0
# Page Configuration
st.set_page_config(
    page_title="Music Streaming Platform",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)
# Playback State
if "current_audio" not in st.session_state:
    st.session_state.current_audio = None
if "current_audio_name" not in st.session_state:
    st.session_state.current_audio_name = None
if "current_audio_artist" not in st.session_state:
    st.session_state.current_audio_artist = None

# Sidebar Navigation
st.sidebar.title("Navigation")
options = ["Home", "Upload Audio"]
choice = st.sidebar.radio("Go to:", options)

# Home Page: Display uploaded audio files
if choice == "Home":
    st.header("🎶 Home - Your Music Library")
    audio_files = get_all_audio_files()

    if audio_files:
        for file in audio_files:
            col1, col2 = st.columns([1, 5])
            with col1:
                # Display album image if available
                if file["imagepath"]:
                    image_path = os.path.join(os.getcwd(), 'static',file['imagepath'])
                    image = Image.open(image_path)
                    st.image(image, width=80)
                else:
                    st.image("https://via.placeholder.com/80", width=80)
            with col2:
                # Display song title and artist
                st.markdown(f"### {file['title']} by {file['artist']}")
                # Play button for each song
                if st.button(f"Play '{file['title']}'"):
                    if count ==1:
                        st.rerun()
                    st.session_state.current_audio = file["filepath"]
                    st.session_state.current_audio_name = file["title"]
                    st.session_state.current_audio_artist = file["artist"]
                    count = 1
                    
                    
    else:
        st.warning("No audio files uploaded yet. Go to 'Upload Audio' to add some!")

# Upload Audio Page: Allow users to upload audio and image files
elif choice == "Upload Audio":
    st.header("🎵 Upload Your Audio File")
    title = st.text_input("Song Title")
    artist = st.text_input("Artist Name")
    uploaded_audio = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg"])
    uploaded_image = st.file_uploader("Upload a song image (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Upload"):
        if not title or not artist or not uploaded_audio:
            st.error("Please provide all required details (title, artist, and audio file).")
        else:
            # Save uploaded audio and image files to disk
            audio_path = save_uploaded_file(UPLOAD_AUDIO_FOLDER, uploaded_audio)
            image_path = save_uploaded_file(UPLOAD_IMAGE_FOLDER, uploaded_image) if uploaded_image else None

            # Save file details to the database
            save_audio_to_db(title, artist, audio_path, image_path)
            st.success(f"Uploaded '{title}' by {artist} successfully!")

@st.fragment
def play_music():
    st.markdown(
        f"""
        <div style='
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #121212;
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.5);
            z-index: 100;
            padding-bottom: 10px;
            box-sizing: border-box;
        '>
            <div style="display: flex; align-items: center; font-size: 14px;">
                <strong>Now Playing:</strong>
                <span style="margin-left: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {st.session_state.current_audio_name} - {st.session_state.current_audio_artist}
                </span>
            </div>
            <audio controls autoplay style="width: 70%; max-width: 400px; margin-left: 20px;">
                <source src="/app/static/{st.session_state.current_audio}?{st.session_state.current_audio_name}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Adjust for sidebar visibility by checking if the sidebar is open
    st.markdown(
        """
        <style>
            .css-1lcb9o8 {
                margin-bottom: 0;
            }
            .css-1sga9yn {
                padding-bottom: 30px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
# Spotify-Like Play Bar: Display a persistent play bar at the bottom
if st.session_state.current_audio:
    play_music()
