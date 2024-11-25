import os
from pathlib import Path

UPLOAD_AUDIO_FOLDER = "static/uploaded_audio"
UPLOAD_IMAGE_FOLDER = "static/uploaded_images"

# Ensure upload folders exist
Path(UPLOAD_AUDIO_FOLDER).mkdir(parents=True, exist_ok=True)
Path(UPLOAD_IMAGE_FOLDER).mkdir(parents=True, exist_ok=True)



def save_uploaded_file(upload_folder, uploaded_file):
    """Save uploaded file to the `static/` folder."""
    file_path = Path(upload_folder) / uploaded_file.name
    
    # Save the file to the specified path
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Return the file path relative to `static/` for serving (without an extra `static/`)
    return file_path.relative_to('static').as_posix()

def get_audio_file_url(file_path):
    """Generate a Streamlit URL to serve the audio file."""
    return f"/{AUDIO_DIRECTORY}/{Path(file_path).name}"