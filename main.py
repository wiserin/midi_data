from app.parser import ParseLinks
from app.database.models import start_db

if __name__ == "__main__":
    start_db
    parser = ParseLinks()
    parser.parse(200)