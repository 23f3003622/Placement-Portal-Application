from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from datetime import datetime
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
    Placement,
    Interview
)



app = Flask(__name__)



# Configuration
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config["DEBUG"] = config.DEBUG

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
cache = Cache(app)

from flask_mail import Mail, Message

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "shriyakuhu534@gmail.com"
app.config["MAIL_PASSWORD"] = "fgvecosaodcdshgf"
app.config["MAIL_DEFAULT_SENDER"] = "shriyakuhu534@gmail.com"

mail = Mail(app)


# Extensions
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(message):
    print("JWT Unauthorized:", message)
    return jsonify({"message": message}), 401


@jwt.invalid_token_loader
def invalid_token_callback(message):
    print("JWT Invalid:", message)
    return jsonify({"message": message}), 422


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print("JWT Expired")
    return jsonify({"message": "Token expired"}), 401

# ==================== AUTH ROUTES ====================

@app.route(
    "/api/company/applications/<int:application_id>/send-offer",
    methods=["POST"]
)
@jwt_required()
def send_offer_letter(application_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "company":
        return jsonify({"message": "Access denied"}), 403

    application = Application.query.get(application_id)

    print("Application:", application)

    if application:
        print("Status:", application.status)
        print("Student:", application.student.full_name)
        print("Student Email:", application.student.user.email)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.status != "Selected":
        return jsonify({"message": "Student is not selected"}), 400

    student = application.student
    company = application.job.company

    msg = Message(
    subject="Offer Letter",
    sender="shriyakuhu534@gmail.com",
    recipients=[student.user.email]
)
    
    
    msg.body = f"""
        Congratulations {student.full_name}!

        You have been selected for the position of
        {application.job.title}

        Company:
        {company.company_name}

        Regards,
        HR Team
        """
    print(student.user.email)
    mail.send(msg)

    return jsonify({
        "message": "Offer letter sent successfully."
    }), 200

@app.route("/api/export-applications", methods=["POST"])
@jwt_required()
def export_applications():

    from tasks import export_applications_csv


    user_id = get_jwt_identity()

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    export_applications_csv.delay(student.id)

    return jsonify({
        "message": "Export started successfully. You will receive an email once the CSV is generated."
    }), 200



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

    cache.clear()

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
    cache.clear()

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
        
        if user.role == "company":

            company = Company.query.filter_by(user_id=user.id).first()

            if company.status == "Blacklisted":
                return jsonify({
                    "message": "Company account has been blacklisted."
                }), 403
    
    if user.role == "student":

        student = Student.query.filter_by(user_id=user.id).first()

        if student is None:
            return jsonify({
                "message": "Student profile not found."
            }), 404

        if student.status == "Blacklisted":
            return jsonify({
                "message": "Student account has been blacklisted."
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

# Dashboard Statistics

@app.route("/api/admin/dashboard", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def admin_dashboard():

    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    total_students = Student.query.count()
    total_companies = Company.query.filter_by(
    status="Active"
).count()
    total_jobs = JobPosition.query.count()
    total_applications = Application.query.count()

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_applications": total_applications
    }), 200

@app.route("/api/admin/company/<int:id>")
@jwt_required()
def company_details(id):

    company = Company.query.get_or_404(id)

    return jsonify({

        "id": company.id,
        "company_name": company.company_name,
        "industry": company.industry,
        "website": company.website,
        "location": company.location,
        "description": company.description,
        "hr_name": company.hr_name,
        "hr_email": company.hr_email

    })


# Approve Company
@app.route("/api/admin/approve-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def approve_company(company_id):

    current_user = User.query.get(int(get_jwt_identity()))

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
    cache.clear()

    return jsonify({
        "message": "Company approved successfully."
    }), 200

# Get All Companies
@app.route("/api/admin/companies", methods=["GET"])
@jwt_required()
def get_companies():

    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    companies = Company.query.filter_by(
    approval_status="Approved",
    status="Active"
).all()
    data = []

    for company in companies:
        data.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "approval_status": company.approval_status
        })

    return jsonify(data), 200

@app.route("/api/admin/pending-companies", methods=["GET"])
@jwt_required()
def pending_companies():

    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    companies = Company.query.filter_by(
    approval_status="Pending",
    status="Active"
).all()

    data = []

    for company in companies:
        data.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location
        })

    return jsonify(data), 200

# Search Companies
@app.route("/api/admin/search-companies", methods=["GET"])
@jwt_required()
@cache.cached(timeout=120,query_string=True)
def search_companies():

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    keyword = request.args.get("q", "")

    companies = Company.query.filter(
            Company.approval_status == "Approved",
            Company.status == "Active"
        ).filter(
            (Company.company_name.ilike(f"%{keyword}%")) |
            (Company.industry.ilike(f"%{keyword}%"))
        ).all()

    data = []

    for company in companies:
        data.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "approval_status": company.approval_status
        })

    return jsonify(data), 200

# Blacklist Company
@app.route("/api/admin/blacklist-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def blacklist_company(company_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.status = "Blacklisted"
    jobs = JobPosition.query.filter_by(company_id=company.id).all()

    for job in jobs:
        db.session.delete(job)

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Company blacklisted successfully"
    }), 200

# Get All Students
@app.route("/api/admin/students", methods=["GET"])
@jwt_required()
def get_students():

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    students = Student.query.filter_by(
    status="Active"
).all()

    data = []

    for student in students:
        data.append({
            "id": student.id,
            "full_name": student.full_name,
            "branch": student.branch,
            "year": student.year,
            "cgpa": student.cgpa
        })

    return jsonify(data), 200

# Search Students
@app.route("/api/admin/search-students", methods=["GET"])
@jwt_required()
@cache.cached(timeout=120, query_string=True)
def search_students():

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    keyword = request.args.get("q", "")

    students = Student.query.filter(
    Student.status == "Active"
).filter(
    (Student.full_name.ilike(f"%{keyword}%")) |
    (Student.branch.ilike(f"%{keyword}%"))
).all()

    data = []

    for student in students:
        data.append({
            "id": student.id,
            "full_name": student.full_name,
            "branch": student.branch,
            "year": student.year,
            "cgpa": student.cgpa
        })

    return jsonify(data), 200

# Blacklist Student
@app.route("/api/admin/blacklist-student/<int:student_id>", methods=["PUT"])
@jwt_required()
def blacklist_student(student_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    student.status = "Blacklisted"

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Student blacklisted successfully"
    }), 200

# Create Placement Drive

# Get All Job Postings
@app.route("/api/admin/jobs", methods=["GET"])
@cache.cached(timeout=300)
@jwt_required()
def get_jobs():

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    jobs = JobPosition.query.all()

    data = []

    for job in jobs:

        company = Company.query.get(job.company_id)

        data.append({

            "id": job.id,
            "title": job.title,
            "company": company.company_name if company else "Unknown",
            "location": job.location,
            "deadline": job.application_deadline

        })

    return jsonify(data), 200

# Delete Job Posting
@app.route("/api/admin/delete-job/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    db.session.delete(job)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Job deleted successfully"
    }), 200

# Get All Applications
@app.route("/api/admin/applications", methods=["GET"])
@jwt_required()
def get_applications():

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    applications = Application.query.all()

    data = []

    for application in applications:

        student = Student.query.get(application.student_id)
        job = JobPosition.query.get(application.job_id)

        company_name = ""

        if job:
            company = Company.query.get(job.company_id)
            if company:
                company_name = company.company_name

        data.append({

            "id": application.id,

            "student": student.full_name if student else "Unknown",

            "drive": job.title if job else "Unknown",

            "company": company_name,

            "date": application.application_date

        })

    return jsonify(data), 200

@app.route("/api/admin/student/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student_details(student_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    student = Student.query.get_or_404(student_id)

    applications = []

    for app in student.applications:

        job = app.job

        company = job.company

        applications.append({

            "application_id": app.id,

            "company": company.company_name,

            "job_title": job.title,

            "status": app.status,

            "remarks": app.remarks,

            "applied_at": app.application_date.strftime("%d-%m-%Y")

        })

    return jsonify({

        "student": {

            "id": student.id,

            "name": student.full_name,

            "branch": student.branch,

            "year": student.year,

            "cgpa": student.cgpa,

            "phone": student.phone,

            "skills": student.skills,

            "experience": student.experience,

            "resume": student.resume,

            "placement_status": student.placement_status

        },

        "applications": applications

    })

# ==================== COMPANY ROUTES ====================

# Create Job
# Create Job / Placement Drive
# Create Job / Placement Drive
@app.route("/api/company/jobs", methods=["POST"])
@jwt_required()
def create_job():

    # Get logged-in user
    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user:
        return jsonify({
            "message": "User not found"
        }), 404

    if current_user.role != "company":
        return jsonify({
            "message": "Access denied"
        }), 403

    # Get company profile
    company = Company.query.filter_by(user_id=current_user.id).first()

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    # Read request data
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data received"
        }), 400

    # Validate required fields
    required_fields = [
        "title",
        "description",
        "location",
        "salary",
        "skills_required",
        "eligibility_branch",
        "minimum_cgpa",
        "application_deadline"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

    # Convert deadline string into Python date
    try:
        deadline = datetime.strptime(
            data["application_deadline"],
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return jsonify({
            "message": "Invalid date format. Use YYYY-MM-DD."
        }), 400

    # Create Job
    job = JobPosition(
    company_id=company.id,

    title=data["title"],

    description=data.get("description"),

    salary=data.get("salary"),

    experience_required=data.get("experience_required"),

    benefits=data.get("benefits"),

    location=data.get("location"),

    skills_required=data.get("skills_required"),

    eligibility_branch=data.get("eligibility_branch"),

    minimum_cgpa=data.get("minimum_cgpa"),

    application_deadline=datetime.strptime(
        data["application_deadline"],
        "%Y-%m-%d"
    ).date() if data.get("application_deadline") else None
)

    db.session.add(job)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Drive created successfully",
        "job": {
            "id": job.id,
            "title": job.title,
            "status": job.status
        }
    }), 201

@app.route("/api/company/jobs/<int:job_id>/close", methods=["PUT"])
@jwt_required()
def close_job(job_id):

    company = get_current_company()

    if not company:
        return jsonify({"message": "Access denied"}), 403

    job = db.session.get(JobPosition, job_id)

    if not job:
        return jsonify({"message": "Job not found"}), 404

    if job.company_id != company.id:
        return jsonify({"message": "Unauthorized"}), 403

    job.status = "Closed"

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Drive Closed Successfully"
    }), 200

def get_current_company():

    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return None

    if user.role != "company":
        return None

    company = Company.query.filter_by(
        user_id=user.id
    ).first()

    if not company:
        return None

    if company.approval_status != "Approved":
        return None

    return company
'''
@app.route("/api/company/jobs", methods=["GET"])
@jwt_required()
def get_company_jobs():
    """List the authenticated company's drives, including their current state."""
    company = get_current_company()
    if not company:
        return jsonify({"message": "Access denied"}), 403

    jobs = JobPosition.query.filter_by(company_id=company.id).order_by(
        JobPosition.created_at.desc()
    ).all()

    return jsonify([
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "skills_required": job.skills_required,
            "eligibility_branch": job.eligibility_branch,
            "minimum_cgpa": job.minimum_cgpa,
            "application_deadline": job.application_deadline.isoformat()
            if job.application_deadline else None,
            "status": job.status,
            "created_at": job.created_at.isoformat() if job.created_at else None
        }
        for job in jobs
    ]), 200 '''

@app.route("/api/company/jobs", methods=["GET"])
@jwt_required()
def get_company_jobs():

    user_id = get_jwt_identity()
    print("JWT User ID:", user_id)

    user = User.query.get(int(user_id))
    print("User:", user)

    company = Company.query.filter_by(user_id=user.id).first()
    print("Company:", company)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    jobs = JobPosition.query.filter_by(company_id=company.id).all()

    print("Jobs:", jobs)

    return jsonify([
        {
            "id": job.id,
            "title": job.title,
            "status": job.status
        }
        for job in jobs
    ])


@app.route("/api/company/jobs/<int:job_id>/applications", methods=["GET"])
@jwt_required()
def get_job_applications(job_id):
    """Return applicants only when the drive belongs to the logged-in company."""
    company = get_current_company()
    if not company:
        return jsonify({"message": "Access denied"}), 403

    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first()
    if not job:
        return jsonify({"message": "Drive not found"}), 404

    return jsonify({
        "job": {"id": job.id, "title": job.title, "status": job.status},
        "applications": [
            {
                "id": application.id,
                "status": application.status,
                "remarks": application.remarks,
                "application_date": application.application_date.isoformat()
                if application.application_date else None,
                "student": {
                    "id": application.student.id,
                    "name": application.student.full_name,
                    "email": application.student.user.email,
                    "branch": application.student.branch,
                    "year": application.student.year,
                    "cgpa": application.student.cgpa,
                    "skills": application.student.skills,
                    "resume": application.student.resume
                }
            }
            for application in job.applications
        ]
    }), 200

@app.route("/api/company/applications/<int:application_id>", methods=["GET"])
@jwt_required()
def get_application_details(application_id):

    company = get_current_company()

    if not company:
        return jsonify({"message": "Access denied"}), 403

    application = db.session.get(Application, application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.job.company_id != company.id:
        return jsonify({"message": "Access denied"}), 403

    student = application.student

    interview = application.interview

    return jsonify({

        "id": application.id,

        "status": application.status,

        "remarks": application.remarks,

        "application_date":
            application.application_date.isoformat()
            if application.application_date else None,

        "student":{

            "id": student.id,

            "name": student.full_name,

            "email": student.user.email,

            "branch": student.branch,

            "year": student.year,

            "cgpa": student.cgpa,

            "phone": student.phone,

            "skills": student.skills,

            "resume": student.resume

        },

        "interview":{

            "type":
                interview.interview_mode
                if interview else "",

            "date":
                interview.interview_date.isoformat()
                if interview and interview.interview_date else "",

            "time":
                interview.interview_time.strftime("%H:%M")
                if interview and interview.interview_time else "",

            "link":
                interview.interview_link
                if interview else "",

            "location":
                interview.interview_location
                if interview else "",

            "status":
                interview.status
                if interview else ""

        }

    }),200

@app.route("/api/company/applications/<int:application_id>/status", methods=["PUT"])
@jwt_required()
def update_application_status(application_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "company":
        return jsonify({"message": "Access denied"}), 403

    company = Company.query.filter_by(user_id=current_user.id).first()

    application = db.session.get(Application, application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.job.company_id != company.id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    application.status = data.get("status", application.status)
    application.remarks = data.get("remarks", application.remarks)

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Application updated successfully"
    }), 200

@app.route("/api/company/jobs/<int:job_id>/complete", methods=["PUT"])
@jwt_required()
def complete_job(job_id):
    """Move an open drive into the company's closed drives list."""
    company = get_current_company()
    if not company:
        return jsonify({"message": "Access denied"}), 403

    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first()
    if not job:
        return jsonify({"message": "Drive not found"}), 404

    job.status = "Closed"
    db.session.commit()
    cache.clear()

    return jsonify({"message": "Drive marked complete", "id": job.id, "status": job.status}), 200

'''
# View Company Profile
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
    }), 200 '''

@app.route("/api/company/profile", methods=["GET"])
@jwt_required()
def company_profile():

    user = User.query.get(int(get_jwt_identity()))

    print("Logged in user:", user.id)
    print("Role:", user.role)

    if user.role != "company":
        return jsonify({
            "message": "Access denied",
            "role": user.role
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
@app.route("/api/student/applications", methods=["GET"])
@jwt_required()
def student_applications():

    user = User.query.get(int(get_jwt_identity()))

    if not user or user.role != "student":
        return jsonify({"message": "Access denied"}), 403

    student = Student.query.filter_by(user_id=user.id).first()

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    data = []

    for application in applications:

        job = JobPosition.query.get(application.job_id)

        company = Company.query.get(job.company_id)

        data.append({
            "id": application.id,
            "job": job.title,
            "company": company.company_name,
            "status": application.status,
            "date": application.application_date.strftime("%d-%m-%Y")
        })

    return jsonify(data), 200

@app.route("/api/student/applications/<int:application_id>", methods=["GET"])
@jwt_required()
def student_application_details(application_id):

    user = User.query.get(int(get_jwt_identity()))

    if not user or user.role != "student":
        return jsonify({"message": "Access denied"}), 403

    student = Student.query.filter_by(user_id=user.id).first()

    application = Application.query.filter_by(
        id=application_id,
        student_id=student.id
    ).first()

    if not application:
        return jsonify({"message": "Application not found"}), 404

    job = JobPosition.query.get(application.job_id)
    company = Company.query.get(job.company_id)
    interview = application.interview
    return jsonify({

        "id": application.id,

        "status": application.status,

        "remarks": application.remarks,

        "application_date": application.application_date.strftime("%d-%m-%Y"),

        "job": {
            "title": application.job.title,
            "description": application.job.description,
            "salary": application.job.salary,
            "location": application.job.location,
            "skills_required": application.job.skills_required,
            "eligibility_branch": job.eligibility_branch,
            "minimum_cgpa": job.minimum_cgpa,
            "application_deadline": job.application_deadline.strftime("%d-%m-%Y")
        },

        "company": {
            "company_name": application.job.company.company_name,
            "location": application.job.company.location,
            "industry": company.industry,
            "website": application.job.company.website,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email
        },

        "student": {
            "name": student.full_name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "resume": student.resume
        },

    "interview": {
    "type": interview.interview_mode if interview else "",
    "date": interview.interview_date.isoformat() if interview and interview.interview_date else "",
    "time": interview.interview_time.strftime("%H:%M") if interview and interview.interview_time else "",
    "link": interview.interview_link if interview else "",
    "location": interview.interview_location if interview else ""
}


    }), 200

@app.route("/api/student/history", methods=["GET"])
@jwt_required()
def student_history():

    user = User.query.get(int(get_jwt_identity()))

    if not user or user.role != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    student = Student.query.filter_by(user_id=user.id).first()

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    history = []

    for application in applications:

        job = JobPosition.query.get(application.job_id)
        company = Company.query.get(job.company_id)

        interview = application.interview

        if interview:
            interview_details = (
                f"{interview.interview_mode} | "
                f"{interview.interview_date.strftime('%d-%m-%Y')} | "
                f"{interview.interview_time.strftime('%I:%M %p')}"
            )
        else:
            interview_details = "Not Scheduled"

        history.append({

            "application_id": application.id,

            "drive": job.id,

            "job_title": job.title,

            "company": company.company_name,

            "result": application.status,

            "remarks": application.remarks,

            "interview": interview_details

        })

    return jsonify({

        "student": {

            "name": student.full_name,

            "branch": student.branch

        },

        "history": history

    }), 200

@app.route("/api/student/search-jobs", methods=["GET"])
@jwt_required()
@cache.cached(timeout=120, query_string=True)
def search_jobs():

    user = User.query.get(int(get_jwt_identity()))

    if not user or user.role != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    keyword = request.args.get("q", "")

    jobs = db.session.query(JobPosition).join(Company).filter(
    JobPosition.status == "Open"
).filter(
    (JobPosition.title.ilike(f"%{keyword}%")) |
    (JobPosition.skills_required.ilike(f"%{keyword}%")) |
    (Company.company_name.ilike(f"%{keyword}%"))
).all()

    data = []

    for job in jobs:

        company = Company.query.get(job.company_id)

        data.append({
            "id": job.id,
            "title": job.title,
            "company": company.company_name,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "skills_required": job.skills_required,
            "eligibility_branch": job.eligibility_branch,
            "minimum_cgpa": job.minimum_cgpa,
            "application_deadline": job.application_deadline.isoformat()
        })

    return jsonify(data), 200


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
        "resume": student.resume,
        "experience": student.experience

   }), 200

@app.route("/api/student/profile", methods=["PUT"])
@jwt_required()
def update_student_profile():

    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "student":
        return jsonify({"message": "Access denied"}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()

    
    student.branch = data.get("branch")
    student.year = data.get("year")
    student.cgpa = data.get("cgpa")
    student.phone = data.get("phone")
    student.skills = data.get("skills")
    student.resume = data.get("resume")

    # Only if you've added this column to your Student model
    if hasattr(student, "experience"):
        student.experience = data.get("experience")

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200

@app.route("/api/student/jobs/<int:job_id>", methods=["GET"])
@jwt_required()
def student_job_details(job_id):

    user = User.query.get(int(get_jwt_identity()))

    if not user or user.role != "student":
        return jsonify({"message": "Access denied"}), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({"message": "Drive not found"}), 404

    company = Company.query.get(job.company_id)

    return jsonify({
        "id": job.id,
        "title": job.title,
        "company": company.company_name,
        "description": job.description,
        "salary": job.salary,
        "location": job.location,
        "skills_required": job.skills_required,
        "eligibility_branch": job.eligibility_branch,
        "minimum_cgpa": job.minimum_cgpa,
        "application_deadline": job.application_deadline.isoformat()
    }), 200

@app.route("/api/student/jobs", methods=["GET"])
@jwt_required()
def student_jobs():

    user = User.query.get(int(get_jwt_identity()))

    if not user or user.role != "student":
        return jsonify({"message":"Access denied"}),403

    jobs = JobPosition.query.filter_by(status="Open").all()

    data = []

    for job in jobs:

        company = Company.query.get(job.company_id)

        data.append({
            "id": job.id,
            "title": job.title,
            "company": company.company_name if company else "Unknown",
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "skills_required": job.skills_required,
            "eligibility_branch": job.eligibility_branch,
            "minimum_cgpa": job.minimum_cgpa,
            "application_deadline": job.application_deadline.isoformat()
        })

    return jsonify(data),200

@app.route("/api/student/interviews", methods=["GET"])
@jwt_required()
def get_student_interviews():

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "student":
        return jsonify({"message": "Access denied"}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()

    interviews = (
        Interview.query
        .join(Application)
        .join(JobPosition)
        .filter(Application.student_id == student.id)
        .order_by(Interview.interview_date)
        .all()
    )

    return jsonify([
        {
            "id": interview.application.id,
            "company": interview.application.job.company.company_name,
            "job": interview.application.job.title,
            "date": interview.interview_date.isoformat() if interview.interview_date else "",
            "time": interview.interview_time.strftime("%H:%M") if interview.interview_time else "",
            "type": interview.interview_mode,
            "link": interview.interview_link,
            "location": interview.interview_location,
            "status": interview.status
        }
        for interview in interviews
    ])

@app.route("/api/company/interviews", methods=["GET"])
@jwt_required()
def company_interviews():

    company = get_current_company()

    if not company:
        return jsonify({"message": "Access denied"}), 403

    interviews = (
        Interview.query
        .join(Application)
        .join(JobPosition)
        .filter(JobPosition.company_id == company.id)
        .order_by(Interview.interview_date, Interview.interview_time)
        .all()
    )

    result = []

    for interview in interviews:

        application = interview.application
        student = application.student
        job = application.job

        result.append({

            "id": application.id,

            "student": student.full_name,

            "job": job.title,

            "date": interview.interview_date.isoformat()
                    if interview.interview_date else "",

            "time": interview.interview_time.strftime("%H:%M")
                    if interview.interview_time else "",

            "type": interview.interview_mode,

            "link": interview.interview_link,

            "location": interview.interview_location,

            "status": interview.status

        })

    return jsonify(result), 200

@app.route("/api/company/dashboard-stats", methods=["GET"])
@jwt_required()
def company_dashboard_stats():

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "company":
        return jsonify({"message":"Access denied"}),403

    company = Company.query.filter_by(user_id=current_user.id).first()

    if not company:
        return jsonify({"message":"Company not found"}),404

    jobs = JobPosition.query.filter_by(company_id=company.id).all()

    total_drives = len(jobs)

    active_drives = JobPosition.query.filter_by(
        company_id=company.id,
        status="Open"
    ).count()

    closed_drives = JobPosition.query.filter_by(
        company_id=company.id,
        status="Closed"
    ).count()

    applications = Application.query.join(JobPosition).filter(
        JobPosition.company_id==company.id
    ).count()

    shortlisted = Application.query.join(JobPosition).filter(
        JobPosition.company_id==company.id,
        Application.status=="Shortlisted"
    ).count()

    rejected = Application.query.join(JobPosition).filter(
        JobPosition.company_id==company.id,
        Application.status=="Rejected"
    ).count()

    waitlisted = Application.query.join(JobPosition).filter(
        JobPosition.company_id==company.id,
        Application.status=="Waitlisted"
    ).count()

    selected=(Application.query.join(JobPosition).filter(JobPosition.company_id==company.id,
Application.status=="Selected").count()

)

    return jsonify({

        "total_drives":total_drives,

        "active_drives":active_drives,

        "closed_drives":closed_drives,

        "applications":applications,

        "selected":selected,

        "shortlisted":shortlisted,

        "rejected":rejected,

        "waitlisted":waitlisted

    })

from datetime import datetime

@app.route("/api/company/applications/<int:application_id>/schedule-interview", methods=["POST"])
@jwt_required()
def schedule_interview(application_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user or current_user.role != "company":
        return jsonify({"message": "Access denied"}), 403

    company = Company.query.filter_by(user_id=current_user.id).first()

    application = db.session.get(Application, application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.job.company_id != company.id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    interview = Interview.query.filter_by(
        application_id=application.id
    ).first()

    if not interview:
        interview = Interview(
            application_id=application.id
        )
        db.session.add(interview)

    interview.interview_mode = data["type"]

    interview.interview_date = datetime.strptime(
        data.get("date"),
        "%Y-%m-%d"
    ).date()

    interview.interview_time = datetime.strptime(
        data.get("time"),
        "%H:%M"
    ).time()

    if data.get("type") == "Online":
        interview.interview_link = data["location"]
        interview.interview_location = None
    else:
        interview.interview_location = data["location"]
        interview.interview_link = None

        db.session.commit()

    # Send interview email

    student = application.student

    msg = Message(
        subject="Interview Invitation",
        sender=app.config["MAIL_USERNAME"],
        recipients=[student.user.email]
    )

    msg.body = f"""
Dear {student.full_name},

Congratulations!

You have been shortlisted for the position of {application.job.title}
at {company.company_name}.

Interview Details

Date: {interview.interview_date.strftime("%d-%m-%Y")}
Time: {interview.interview_time.strftime("%I:%M %p")}
Mode: {interview.interview_mode}
"""

    if interview.interview_mode == "Online":
        msg.body += f"""

Meeting Link:
{interview.interview_link}
"""
    else:
        msg.body += f"""

Venue:
{interview.interview_location}
"""

    msg.body += """

Please be available at least 10 minutes before your scheduled interview.

Best Wishes,
HR Team
"""

    mail.send(msg)

    return jsonify({
        "message": "Interview Scheduled Successfully"
    }), 200


@app.route("/api/student/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_job(job_id):

    user = User.query.get(int(get_jwt_identity()))

    if not user or user.role!="student":
        return jsonify({"message":"Access denied"}),403

    student = Student.query.filter_by(user_id=user.id).first()

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({"message":"Drive not found"}),404

    already = Application.query.filter_by(
        student_id=student.id,
        job_id=job.id
    ).first()

    if already:
        return jsonify({"message":"Already applied"}),400

    application = Application(
        student_id=student.id,
        job_id=job.id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()
    cache.clear()

    return jsonify({"message":"Applied Successfully"}),201
# ==================== MAIN ====================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)
