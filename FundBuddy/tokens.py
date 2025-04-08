from datetime import datetime, timedelta
import jwt
import schemas

ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def generate_access_token(data, expire_timedelta: timedelta | None = None):
    to_encode = data.copy()
    if expire_timedelta:
        expire = datetime.now() + expire_timedelta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return token_data
    except:
        raise credentials_exception
