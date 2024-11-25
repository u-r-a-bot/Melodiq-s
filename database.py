from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import sessionmaker

DATABASE_FILE = "music_streaming.db"
engine = create_engine(f"sqlite:///{DATABASE_FILE}")
metadata = MetaData()

# Table for audio metadata
audio_table = Table(
    "audio_files",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String),
    Column("artist", String),
    Column("filepath", String),
    Column("imagepath", String),
)

# Create table if not exists
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_audio_to_db(title, artist, filepath, imagepath):
    """Save audio file metadata to the database."""
    try:
        with engine.connect() as conn:
            conn.execute(audio_table.insert().values(
                title=title,
                artist=artist,
                filepath=filepath,
                imagepath=imagepath
            ))
            conn.commit()
        print(f"Successfully inserted: {title}, {artist}, {filepath}, {imagepath}")  # Debug log
    except Exception as e:
        print(f"Error inserting into database: {e}")  # Debug log
        raise RuntimeError(f"Database error: {e}")


def get_all_audio_files():
    """Retrieve all audio files from the database."""
    with engine.connect() as conn:
        result = conn.execute(audio_table.select()).fetchall()
        print(f"Fetched from DB: {result}")
    return [{"id": row[0], "title": row[1], "artist": row[2], "filepath": row[3], "imagepath": row[4]} for row in result]
