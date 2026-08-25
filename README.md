# Placement Portal Application

A full-stack **Placement Portal Application (PPA)** designed to streamline the campus placement process by connecting students, companies, and placement administrators through a centralized web platform.

The application provides features for **job posting, student applications, interview scheduling, placement management, offer management, email notifications, application exports, caching, and background task processing**.

---

## 🚀 Features

### 👨‍🎓 Student

* Student registration and authentication
* View available job opportunities
* Apply for jobs
* Track application status
* View scheduled interviews
* Receive email notifications
* View placement information

### 🏢 Company

* Company authentication
* Create and manage job positions
* View applications for posted jobs
* Schedule interviews
* Send placement/offer notifications
* View company dashboard and statistics

### 🧑‍💼 Placement Administration

* Manage students and companies
* Monitor job positions and applications
* Track placement information
* Generate application reports
* Manage the overall placement workflow

### ⚙️ Background Processing

The application uses **Celery and Redis** for asynchronous/background tasks such as:

* Sending deadline reminder emails
* Generating application export files
* Generating periodic placement reports

### ⚡ Caching

**Redis** is used for caching frequently accessed data to improve application performance and reduce unnecessary database queries.

---

## 🛠️ Tech Stack

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| Python             | Backend programming             |
| Flask              | REST API backend                |
| Vue.js             | Frontend                        |
| Vite               | Frontend development/build tool |
| SQLite             | Database                        |
| SQLAlchemy         | ORM                             |
| Redis              | Caching & Celery message broker |
| Celery             | Background task processing      |
| Flask-JWT-Extended | JWT authentication              |
| Flask-Mail         | Email notifications             |
| Bootstrap          | UI styling                      |
| Axios              | Frontend API communication      |

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      Vue.js UI      │
                    │     + Bootstrap     │
                    └──────────┬──────────┘
                               │
                               │ HTTP / REST API
                               ▼
                    ┌─────────────────────┐
                    │     Flask Backend   │
                    │                     │
                    │  REST API + JWT     │
                    └───────┬─────┬───────┘
                            │     │
                 ┌──────────┘     └──────────┐
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ SQLite Database │        │      Redis      │
        │  + SQLAlchemy   │        │     Cache       │
        └─────────────────┘        └────────┬────────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │     Celery      │
                                   │ Worker / Tasks  │
                                   └────────┬────────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │ Email / Reports │
                                   └─────────────────┘
```

---

## 📂 Project Structure

```text
Placement-Portal/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   ├── tasks.py
│   ├── celery_worker.py
│   ├── celery_config.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── ...
```

> The exact folder structure may vary depending on the version of the project.

---

# 🔐 Authentication

The application uses **JSON Web Tokens (JWT)** for authentication.

After successful login:

```text
User Login
    ↓
Flask verifies credentials
    ↓
JWT access token generated
    ↓
Token sent to frontend
    ↓
Frontend includes token in API requests
    ↓
Backend validates token
    ↓
Protected resource accessed
```

Different user roles can access functionality according to their permissions.

---

# 🗄️ Database Design

The main entities in the application include:

### User

Stores common authentication information.

### Student

Stores student-specific information.

### Company

Stores company information.

### JobPosition

Represents a job posted by a company.

### Application

Connects students with job positions and stores application information.

### Interview

Stores interview scheduling information.

### Placement

Stores successful placement information.

A simplified relationship can be represented as:

```text
Company
   │
   │ posts
   ▼
JobPosition
   │
   │ receives
   ▼
Application
   ▲
   │ submitted by
   │
Student
   │
   │
   ▼
Interview
   │
   ▼
Placement
```

---

# ⚡ Redis & Celery

Redis serves two important purposes in the application.

### Redis Cache

Frequently accessed information can be cached in Redis to reduce database queries.

For example:

```text
Frontend
   ↓
Flask API
   ↓
Check Redis Cache
   │
   ├── Cache Hit → Return cached data
   │
   └── Cache Miss
          ↓
      Query SQLite
          ↓
      Store result in Redis
          ↓
      Return data
```

### Celery

Celery handles tasks that should run independently of the user's request.

Examples include:

* Deadline reminder emails
* Application CSV exports
* Periodic placement reports

```text
Flask Application
       │
       │ creates task
       ▼
     Redis
       │
       │ task queue
       ▼
 Celery Worker
       │
       ├── Send Email
       ├── Generate CSV
       └── Generate Report
```

---

# 📧 Email Notifications

The application uses **Flask-Mail** to send emails through an SMTP server.

Email functionality can be used for:

* Job deadline reminders
* Placement/offer notifications
* Other application-related notifications

SMTP configuration is stored through environment/configuration variables rather than being hard-coded.

---

# 📊 Application Export

The application supports exporting application information into a CSV file.

The process uses a background Celery task:

```text
User requests export
        ↓
Flask API
        ↓
Celery task queued
        ↓
Redis
        ↓
Celery Worker
        ↓
CSV generated
```

This prevents a potentially time-consuming export operation from blocking the main web application.

---

# ⏰ Scheduled Tasks

Celery can also execute scheduled tasks using **Celery Beat**.

Examples include:

### Deadline Reminders

Students can receive reminders about upcoming application deadlines.

### Monthly Placement Report

A periodic report can be generated containing placement-related information.

The scheduling configuration uses the project's configured timezone.

---

# 💻 Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

---

## 2. Set up the backend

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure environment variables

Create a `.env` file or configure the required environment variables.

Example:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

REDIS_URL=redis://localhost:6379/0

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
```

**Do not commit real passwords, API keys, JWT secrets, or email credentials to GitHub.**

Add sensitive files such as `.env` to `.gitignore`.

---

# 🔴 Redis Setup

Make sure Redis is running locally.

The application uses:

```text
redis://localhost:6379/0
```

Redis is required for:

* Application caching
* Celery message brokering
* Celery result backend

---

# ▶️ Running the Backend

From the backend directory:

```bash
python app.py
```

The Flask server runs on:

```text
http://127.0.0.1:5000
```

---

# ⚙️ Running Celery

Start a Celery worker.

On Windows, the project can use the solo pool:

```bash
celery -A celery_worker.celery worker --pool=solo --loglevel=info
```

For scheduled tasks, start Celery Beat as well:

```bash
celery -A celery_worker.celery beat --loglevel=info
```

---

# 🌐 Running the Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will typically be available at:

```text
http://localhost:5173
```

---

# 🔄 Application Workflow

A typical student application workflow is:

```text
Student logs in
      ↓
Views available jobs
      ↓
Selects a job
      ↓
Submits application
      ↓
Application stored in database
      ↓
Cache updated/cleared
      ↓
Company views applications
      ↓
Company schedules interview
      ↓
Student receives notification
      ↓
Company sends offer
      ↓
Placement information recorded
```

---

# 🔒 Security Considerations

The project uses several mechanisms to improve application security:

* JWT-based authentication
* Protected API routes
* Role-based access control
* Password hashing
* Environment variables for sensitive configuration
* CORS configuration
* Server-side validation
* Database ORM through SQLAlchemy

Sensitive credentials should **never** be committed to the repository.

---

# 🧪 Development & Testing

Before running the complete application, verify that:

1. Redis is running.
2. Flask backend is running.
3. Celery worker is running.
4. Celery Beat is running if scheduled tasks are required.
5. Vue/Vite frontend is running.
6. Frontend API URL points to the correct Flask backend.
7. JWT tokens are correctly included in protected API requests.

---

# 🐛 Common Issues

### CORS Error

If the browser reports:

```text
No 'Access-Control-Allow-Origin' header
```

check the Flask CORS configuration and make sure the frontend origin is allowed.

### JWT Error

An error such as:

```text
JWT Invalid: Not enough segments
```

usually indicates that the request contains an invalid, missing, or incorrectly formatted JWT.

### Celery Cannot Load Application

Verify that:

* Redis is running.
* The Celery application path is correct.
* The worker is started from the correct directory.
* Python dependencies are installed.

---

# 🎯 Future Improvements

Possible improvements include:

* PostgreSQL/MySQL support for production
* Docker-based deployment
* Cloud deployment
* Improved role-based permissions
* Advanced search and filtering
* Resume upload and parsing
* Interview calendar integration
* Real-time notifications
* Automated placement analytics
* Unit and integration test coverage
* Production-grade logging and monitoring

---

# 📌 Project Goals

The primary goals of this project are to:

* Digitize the campus placement process
* Reduce manual administrative work
* Provide a centralized platform for students and companies
* Improve application and interview tracking
* Automate notifications and report generation
* Demonstrate a scalable full-stack web application architecture

---

# 👩‍💻 Author

**Shriya Tiwari**

Built as a full-stack web application project.

---

## ⭐ Acknowledgements

This project was developed as an academic software project to demonstrate concepts including:

* Full-stack web development
* REST API design
* Database management
* Authentication and authorization
* Caching
* Asynchronous task processing
* Email automation
* Frontend-backend integration
