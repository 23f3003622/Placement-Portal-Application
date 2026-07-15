import os
from datetime import timedelta

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask Configuration
SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-change-in-production"

# SQLite Database
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    BASE_DIR, "instance", "database.db"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT Configuration
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key-change-in-production"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# Debug Mode
DEBUG = True