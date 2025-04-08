from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from hashing import Hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

import schemas
import tokens

users_router = APIRouter(
    tags=["Users"]
)


@users_router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(request: schemas.User, db: Session = Depends(get_db)):
    if request.email == "" or "@" not in request.email or "." not in request.email or \
            request.email.split(".")[-1] != "com":
        raise HTTPException(detail="Please Enter Valid Email", status_code=status.HTTP_400_BAD_REQUEST)
    elif request.password == "" or len(request.password) <= 6:
        raise HTTPException(detail="Please Enter Valid Password", status_code=status.HTTP_400_BAD_REQUEST)
    elif request.email in [user.email for user in db.query(User).all()]:
        raise HTTPException(detail="Email already exists", status_code=status.HTTP_400_BAD_REQUEST)
    new_user = User(email=request.email, password=Hash.bcrypt_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@users_router.post('/login', status_code=status.HTTP_200_OK)
def user_login(request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if request.email == "" or "@" not in request.email or "." not in request.email or \
            request.email.split(".")[-1] != "com":
        raise HTTPException(detail="Please Enter Valid Email", status_code=status.HTTP_400_BAD_REQUEST)
    elif not user:
        raise HTTPException(detail="email not found", status_code=status.HTTP_401_UNAUTHORIZED)
    elif request.password == "" or len(request.password) <= 6:
        raise HTTPException(detail="Please Enter Valid Password", status_code=status.HTTP_400_BAD_REQUEST)
    elif not Hash.verify_password(request.password, user.password):
        raise HTTPException(detail="password not found", status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        access_token = tokens.generate_access_token(data={"sub": user.email}, expire_timedelta=timedelta(minutes=15))
        return {"access_token": access_token, "token_type": "Bearer"}
