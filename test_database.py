import unittest
from unittest.mock import patch, MagicMock
from database import get_all_audio_files  # Import the method you want to test

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up a mock database connection and sample data for testing."""
        # Sample data to be used for mocking database result
        self.mock_data = [
            (1, "Test Song 1", "Artist 1", "static/test_song1.mp3", "static/image1.jpg"),
            (2, "Test Song 2", "Artist 2", "static/test_song2.mp3", None),
        ]

    @patch("database.engine.connect")
    def test_get_all_audio_files_empty(self, mock_connect):
        """Test retrieving all audio files from the database when no data exists."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        
        mock_connect.return_value.__enter__.return_value = mock_cursor

        result = get_all_audio_files()

        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
