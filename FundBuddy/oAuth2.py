from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

import tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return tokens.verify_token(token, credentials_exception)
