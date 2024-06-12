from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    Search for a contact by email

    Args:
        email (str): email to match
        db (Session): session with db

    Returns:
        User | None: user object or none if it isn´t
    """
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user ini db

    Args:
        body (UserModel): UserModel object
        db (Session): session with db

    Returns:
        User: user object
    """
    g        = Gravatar(body.email)
    new_user = User(**body.dict(), avatar=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token: str | None, db: Session) -> None:
    """
    Updates token

    Args:
        user (User): user object
        refresh_token (str | None): token
        db (Session): session with db
    """
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Email confirmation in db

    Args:
        email (str): email to match
        db (Session): session with db
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates user´s avatar

    Args:
        email (str): email to match
        url (str): avatar´s url
        db (Session): session with db

    Returns:
        User: user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
