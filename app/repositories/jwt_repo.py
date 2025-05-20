from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.models.users import Users
from config import SECRET_KEY, ALGORITHM


class JWTRepo:
    @staticmethod
    def generate_token(user: Users):
        to_encode = {
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'sub': str(user.id),
            'role': user.role
        }
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as e:
            raise JWTError(f'Invalid token: {str(e)}')
