from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from database.connect import get_db
from src.repository import users as repository_users
from src.conf.config import settings


class Auth:
    pwd_context   = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY    = settings.secret_key
    ALGORITHM     = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


    def verify_password(self, plain_password, hashed_password):
        """
        Verify passwork function

        Args:
            plain_password (_type_): password check
            hashed_password (bool): comparising with hashed password

        Returns:
            _type_: boolean
        """
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password: str):
        """
        Gets password hash

        Args:
            password (str): password

        Returns:
            _type_: password hash
        """
        return self.pwd_context.hash(password)


    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Creates new access token

        Args:
            data (dict): data to encode
            expires_delta (Optional[float], optional): time of token expiration

        Returns:
            _type_: encoded token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now() + timedelta(hours=48)
        to_encode.update({"iat": datetime.now(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token


    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Creates refreshed token

        Args:
            data (dict): data to encode
            expires_delta (Optional[float], optional): time of token expiration

        Returns:
            _type_: encoded token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now() + timedelta(days=7)
        to_encode.update({"iat": datetime.now(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token


    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Checks if user´s token is valid

        Args:
            token (str, optional): token
            db (Session, optional): session with db

        Raises:
            credentials_exception: if unauthorized

        Returns:
            _type_: user object
        """
        credentials_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Could not validate credentials",
            headers     = {"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "access_token":
                email = payload.get("sub")
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user


    async def decode_refresh_token(self, refresh_token: str):
        """
        Decodes refreshed token

        Args:
            refresh_token (str): refreshed token

        Raises:
            HTTPException: if unauthorized, invalid scope
            HTTPException: if unauthorized, validation error

        Returns:
            _type_: user´s email
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Validation error')


    def create_email_token(self, data: dict):
        """
        Creates encoded token

        Args:
            data (dict): data to encode

        Returns:
            _type_: encoded token
        """
        to_encode = data.copy()
        expire    = datetime.now() + timedelta(hours=1)
        to_encode.update({"iat": datetime.now(), "exp": expire, "scope": "email_token"})
        token     = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token


    def get_email_from_token(self, token: str):
        """
        Returns the email encoded in token

        Args:
            token (str): token

        Raises:
            HTTPException: Invalid scope
            HTTPException: Invalid token

        Returns:
            _type_: email
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'email_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The token is invalid")


auth_service = Auth()
