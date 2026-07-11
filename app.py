from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

import config
from models import (
    db,
    User,
    Company,
    Student,
    JobPosition,
    Application,
    Placement
)

# ==================== INITIALIZE APP ====================

app = Flask(__name__)

# ==================== CONFIG ====================

app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config["DEBUG"] = config.DEBUG

# ==================== EXTENSIONS ====================

db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# ==================== AUTH ROUTES ====================

# login
# register

# ==================== ADMIN ROUTES ====================

# approve companies
# create placement drives

# ==================== COMPANY ROUTES ====================

# create jobs
# view applications

# ==================== STUDENT ROUTES ====================

# apply job
# view profile

# ==================== MAIN ====================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)