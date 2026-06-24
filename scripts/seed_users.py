"""
One-time utility to seed initial users.

Usage (run from repo root):
    python -m scripts.seed_users

Edit INITIAL_USERS below before running.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.services.auth_service import hash_password

INITIAL_USERS = [
    {"username": "admin",    "password": "changeme123", "role": UserRole.supervisor},
    {"username": "operator1","password": "changeme123", "role": UserRole.operator},
]


def seed():
    db = SessionLocal()
    try:
        for u in INITIAL_USERS:
            exists = db.query(User).filter(User.username == u["username"]).first()
            if exists:
                print(f"  skip  {u['username']} (already exists)")
                continue
            db.add(User(
                username=u["username"],
                hashed_password=hash_password(u["password"]),
                role=u["role"],
            ))
            print(f"  added {u['username']} ({u['role'].value})")
        db.commit()
        print("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
