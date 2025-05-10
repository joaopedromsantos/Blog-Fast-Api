from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.repositories.jwt_repo import JWTRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def get_current_user_dependency(token: str = Depends(oauth2_scheme)):
    try:
        payload = JWTRepo.decode_token(token)
        user = payload.get('sub')
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
