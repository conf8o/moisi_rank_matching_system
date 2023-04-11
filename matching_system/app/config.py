import os

DATABASE_URL = os.environ.get("MOISI_MATCHING_SYSTEM_DATABASE_URL", "sqlite:///db.sqlite3")
