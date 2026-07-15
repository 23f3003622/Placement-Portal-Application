from werkzeug.security import generate_password_hash

from app import app
from models import db, User


def create_admin():

    with app.app_context():

        # Check if admin already exists
        admin = User.query.filter_by(role="admin").first()

        if admin:
            print("Admin user already exists.")
            return

        # Create default admin
        admin = User(
            username="admin",
            email="admin@placement.com",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")


if __name__ == "__main__":
    create_admin()