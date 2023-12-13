from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as rep_contacts
from src.schemas.contact import ContactSchema, ContactUpdateSchema, ContactResponseSchema

router = APIRouter(prefix='/birthday', tags=['birthday'])


# Знайдена міцна залежність між шляхом {shift_days} та назвою змінної у функції -> search_contact_by_birthdate(shift_days, ... 
@router.get("/{shift_days}", response_model=list[ContactResponseSchema])
async def search_contact_by_birthdate(shift_days: int = Path(..., description="Кількість найближчих днів у запитi"),
                                      db: AsyncSession = Depends(get_db)):
    contacts = await rep_contacts.search_contact_by_birthdate(shift_days, db)
    return contacts