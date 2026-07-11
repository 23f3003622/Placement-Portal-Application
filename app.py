from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

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

app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config["DEBUG"] = config.DEBUG

# Extensions
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# ==================== AUTH ROUTES ====================

# Register Student

@app.route("/api/auth/student/register", methods=["POST"])
def register_student():

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Check required fields
    required_fields = [
        "username",
        "email",
        "password",
        "full_name",
        "branch",
        "year",
        "cgpa"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    # Check if username exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already exists"}), 400

    # Check if email exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    # Create User
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    # Create Student Profile
    student = Student(
        user_id=user.id,
        full_name=data["full_name"],
        branch=data["branch"],
        year=data["year"],
        cgpa=data["cgpa"],
        phone=data.get("phone"),
        skills=data.get("skills"),
        resume=data.get("resume")
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student registered successfully"
    }), 201

# Register Company

@app.route("/api/auth/company/register", methods=["POST"])
def register_company():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    required_fields = [
        "username",
        "email",
        "password",
        "company_name",
        "industry",
        "location",
        "hr_name",
        "hr_email"
        ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already exists"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    # Create login account
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role="company"
    )

    db.session.add(user)
    db.session.commit()

    # Create company profile
    company = Company(
        user_id=user.id,
        company_name=data["company_name"],
        industry=data["industry"],
        location=data["location"],
        website=data.get("website"),
        description=data.get("description"),
        hr_name=data["hr_name"],
        hr_email=data["hr_email"],
        approval_status="Pending"
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({
        "message": "Company registered successfully. Waiting for admin approval."
    }), 201

# Login
@app.route("/api/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "Invalid username or password"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401
    
    # Check company approval
    if user.role == "company":

        company = Company.query.filter_by(user_id=user.id).first()

        if company is None:
            return jsonify({
                "message": "Company profile not found."
            }), 404

        if company.approval_status != "Approved":
            return jsonify({
                "message": "Company account is waiting for admin approval."
            }), 403

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
        }), 200

# ==================== ADMIN ROUTES ====================

@app.route("/api/admin/profile", methods=["GET"])
@jwt_required()
def admin_profile():

    current_user_id = get_jwt_identity()

    user = User.query.get(int(get_jwt_identity()))

    if user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    return jsonify({

        "username": user.username,
        "email": user.email,
        "role": user.role

    }), 200

# Approve Company
@app.route("/api/admin/approve-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def approve_company(company_id):

    current_user = User.query.get(get_jwt_identity())

    if current_user.role != "admin":
        return jsonify({
            "message": "Only admin can approve companies."
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found."
        }), 404

    company.approval_status = "Approved"

    db.session.commit()

    return jsonify({
        "message": "Company approved successfully."
    }), 200

# Create Placement Drive

# ==================== COMPANY ROUTES ====================

# Create Job

# View Applications
@app.route("/api/company/profile", methods=["GET"])
@jwt_required()
def company_profile():

    current_user_id = get_jwt_identity()

    user = User.query.get(int(get_jwt_identity()))

    if user.role != "company":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.filter_by(user_id=user.id).first()

    if company is None:
        return jsonify({
            "message": "Company profile not found."
        }), 404

    return jsonify({
        "company_name": company.company_name,
        "industry": company.industry,
        "location": company.location,
        "website": company.website,
        "description": company.description,
        "hr_name": company.hr_name,
        "hr_email": company.hr_email,
        "approval_status": company.approval_status
    }), 200

# ==================== STUDENT ROUTES ====================

# Apply Job

# View Profile
@app.route("/api/student/profile", methods=["GET"])
@jwt_required()
def student_profile():

    current_user_id = get_jwt_identity()

    user = User.query.get(int(get_jwt_identity()))

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.role != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    return jsonify({

        "username": user.username,
        "email": user.email,

        "full_name": student.full_name,
        "branch": student.branch,
        "year": student.year,
        "cgpa": student.cgpa,
        "phone": student.phone,
        "skills": student.skills,
        "resume": student.resume

    }), 200

# ==================== MAIN ====================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)