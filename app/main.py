from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import Base, User
from .schemas import UserCreate, UserRead
from .utils import hash_password

Base.metadata.create_all(bind=engine)  # safe in dev

app = FastAPI(title="Secure FastAPI Users")


# ---- Dependency to get DB session ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---- Routes ----
@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if (
        db.query(User)
        .filter((User.username == payload.username) | (User.email == payload.email))
        .first()
    ):
        raise HTTPException(status_code=409, detail="Username or email already exists.")

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password.get_secret_value()),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
