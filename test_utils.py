import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from pathlib import Path
from utils import save_uploaded_file, get_audio_file_url, UPLOAD_AUDIO_FOLDER

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_audio = BytesIO(b"Test audio content")
        self.test_audio.name = "test_song.mp3"
        self.upload_folder = UPLOAD_AUDIO_FOLDER

    @patch("builtins.open", new_callable=MagicMock)
    def test_save_uploaded_file(self, mock_open):
        """Test saving uploaded file."""
        self.test_audio.name = "test_song.mp3"
        
        mock_open.return_value.__enter__.return_value = MagicMock()
        result = save_uploaded_file(self.upload_folder, self.test_audio)

        mock_open.assert_called_once_with(Path(self.upload_folder) / "test_song.mp3", "wb")

        expected_file_path = "uploaded_audio/test_song.mp3" 
        self.assertEqual(result, expected_file_path)

    @patch("utils.AUDIO_DIRECTORY", "uploaded_audio")  # Mock AUDIO_DIRECTORY
    def test_get_audio_file_url(self):
        """Test generating the correct audio file URL."""
        file_path = "static/uploaded_audio/test_song.mp3"
        result = get_audio_file_url(file_path)

        expected_url = "/uploaded_audio/test_song.mp3"
        self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()
