from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from typing import List

from src.database.connect import get_db
from src.database.models import User
from src.services.auth import auth_service
from src.schemas import ContactResponse, BirthdayResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> List[ContactResponse]:
    """
    Returns a list of contacts

    Args:
        limit (int, optional): amount of contacs to return
        offset (int, optional): amount of contacs to skip
        db (Session, optional): session with db
        current_user (User, optional): user object

    Returns:
        List[ContactResponse]: list of contacts
    """
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(query: str = Query(default='', min_length=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Search for contact

    Args:
        query (str, optional): query
        db (Session, optional): session with db
        current_user (User, optional): user object

    Returns:
        list: list of contacts
    """

    contacts = await repository_contacts.search_contacts(query, db)
    return contacts


@router.get("/birthday/", response_model=List[BirthdayResponse])
async def get_contacts_birthday(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Returns a list of contacts that have birthday within the next week

    Args:
        db (Session, optional): session with db
        current_user (User, optional): user object

    Returns:
        List: list of contacts
    """
    birthdays = await repository_contacts.get_birthdays_one_week(db)
    return birthdays


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    """
    Search for contact by id

    Args:
        contact_id (int, optional): user´s id
        db (Session, optional): session with db
        current_user (User, optional): user object

    Raises:
        HTTPException: if not found

    Returns:
        ContactResponse: contact object
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 2 requests per 10 sec',
             dependencies=[Depends(RateLimiter(times=2, seconds=10))])
async def create_contact(body: ContactResponse, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    """
    Creates a new contact in db

    Args:
        body (ContactResponse): data
        db (Session, optional): session with db
        current_user (User, optional): user object

    Returns:
        ContactResponse: contact object
    """
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactResponse, contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    """
    Updates a contact in db

    Args:
        body (ContactResponse): data
        contact_id (int, optional): contact_id
        db (Session, optional): session with db
        current_user (User, optional): user object

    Raises:
        HTTPException: if not found

    Returns:
        ContactResponse: updated contact object
    """
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    removes a contact from DB

    Args:
        contact_id (int, optional): contact_id
        db (Session, optional): session with db
        current_user (User, optional): user object

    Raises:
        HTTPException: if not found

    Returns:
        _type_: removed contact object
    """
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
