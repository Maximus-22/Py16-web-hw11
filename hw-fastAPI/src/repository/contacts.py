from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact
from src.schemas.contact import ContactSchema, ContactResponseSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    statement = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(statement)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    statement = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(statement)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    # Метод [model_dump()] у Pydantic моделях використовується для перетворення моделі на словник.
    # (first_name=body.first_name, last_name=body.last_name, ...)
    # Параметр <exclude_unset> = True вказує, що в результуючий словник повинні бути включені тільки поля,
    # які були встановлені (тобто не мають значення за замовчуванням).
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession):
    statement = select(Contact).filter_by(id=contact_id)
    result = await db.execute(statement)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.crm_status = body.crm_status
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    statement = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(statement)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
