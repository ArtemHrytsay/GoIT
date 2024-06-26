from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from typing import List

from database.connect import get_db
from src.database.models import User
from src.services.auth import auth_service
from src.schemas import ContactResponse, BirthdayResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> List[ContactResponse]:
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(query: str = Query(default='', min_length=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.search_contacts(query, db)
    return contacts


@router.get("/birthday/", response_model=List[BirthdayResponse])
async def get_contacts_birthday(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    birthdays = await repository_contacts.get_birthdays_one_week(db)
    return birthdays


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 2 requests per 10 sec',
             dependencies=[Depends(RateLimiter(times=2, seconds=10))])
async def create_contact(body: ContactResponse, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactResponse, contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
