# Placement Portal Application

A full-stack web application for managing the college placement process. It provides separate functionality for students, companies, and placement administrators.

## Features

* Student registration, login, and job applications
* Company job posting and application management
* Interview scheduling and offer management
* Placement tracking
* JWT-based authentication
* Email notifications
* CSV application export
* Redis caching
* Celery background and scheduled tasks

## Tech Stack

* **Frontend:** Vue.js, Vite, Bootstrap, Axios
* **Backend:** Flask, Python
* **Database:** SQLite, SQLAlchemy
* **Authentication:** JWT
* **Caching & Tasks:** Redis, Celery
* **Email:** Flask-Mail

## Project Structure

```text
Placement-Portal/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── tasks.py
│   ├── celery_worker.py
│   └── ...
├── frontend/
│   ├── src/
│   └── ...
└── README.md
```

## Running Locally

### Backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Celery

Make sure Redis is running, then start:

```bash
celery -A celery_worker.celery worker --pool=solo --loglevel=info
```

For scheduled tasks:

```bash
celery -A celery_worker.celery beat --loglevel=info
```

The frontend runs on `localhost:5173` and the Flask API on `localhost:5000`.

## Screenshots

![Screenshot 175](images/Screenshot%20%28175%29.png)
![Screenshot 176](images/Screenshot%20%28176%29.png)
![Screenshot 177](images/Screenshot%20%28177%29.png)
![Screenshot 178](images/Screenshot%20%28178%29.png)
![Screenshot 179](images/Screenshot%20%28179%29.png)
![Screenshot 180](images/Screenshot%20%28180%29.png)
![Screenshot 181](images/Screenshot%20%28181%29.png)


