from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ==========================
# USER MODEL
# ==========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # admin / company / student
    role = db.Column(db.String(20), nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship(
        "Student",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    company = db.relationship(
        "Company",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<User {self.username}>"


# ==========================
# COMPANY MODEL
# ==========================
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    company_name = db.Column(db.String(150), nullable=False)

    industry = db.Column(db.String(100))

    website = db.Column(db.String(200))

    location = db.Column(db.String(150))

    description = db.Column(db.Text)

    hr_name = db.Column(db.String(100))

    hr_email = db.Column(db.String(120))

    approval_status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    jobs = db.relationship(
        "JobPosition",
        backref="company",
        cascade="all, delete-orphan"
    )

    placements = db.relationship(
        "Placement",
        backref="company",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Company {self.company_name}>"


# ==========================
# STUDENT MODEL
# ==========================
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    full_name = db.Column(db.String(120), nullable=False)

    branch = db.Column(db.String(100))

    year = db.Column(db.Integer)

    cgpa = db.Column(db.Float)

    phone = db.Column(db.String(20))

    skills = db.Column(db.Text)

    resume = db.Column(db.String(255))

    placement_status = db.Column(
        db.String(30),
        default="Not Placed"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    applications = db.relationship(
        "Application",
        backref="student",
        cascade="all, delete-orphan"
    )

    placements = db.relationship(
        "Placement",
        backref="student",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.full_name}>"


# ==========================
# JOB POSITION MODEL
# ==========================
class JobPosition(db.Model):
    __tablename__ = "job_positions"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    salary = db.Column(db.Float)

    location = db.Column(db.String(150))

    skills_required = db.Column(db.Text)

    eligibility_branch = db.Column(db.String(100))

    minimum_cgpa = db.Column(db.Float)

    application_deadline = db.Column(db.Date)

    status = db.Column(
        db.String(20),
        default="Open"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    applications = db.relationship(
        "Application",
        backref="job",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Job {self.title}>"


# ==========================
# APPLICATION MODEL
# ==========================
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("job_positions.id"),
        nullable=False
    )

    application_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(30),
        default="Applied"
    )

    remarks = db.Column(db.Text)

    placement = db.relationship(
        "Placement",
        backref="application",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Application {self.id}>"


# ==========================
# PLACEMENT MODEL
# ==========================
class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    salary = db.Column(db.Float)

    joining_date = db.Column(db.Date)

    position = db.Column(db.String(150))

    offer_letter = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Placement {self.id}>"