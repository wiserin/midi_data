from app.parser import ParseLinks, ParseMidi
from app.database.models import start_db

if __name__ == "__main__":
    start_db
    parser = ParseLinks()
    parser.parse(6667)