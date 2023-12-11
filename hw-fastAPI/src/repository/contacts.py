from datetime import datetime
from sqlalchemy import select, Date
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
    # print(type(body.birth_date))
    # print(body.birth_date)

    # body.birth_date = datetime.strptime(body.birth_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    # body.birth_date = datetime.strptime(body.birth_date, '%Y-%m-%d') -> не працюэ
    # body.birth_date = Date(body.birth_date)

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


async def search_by_firstname(contact_first_name: str, db: AsyncSession):
    statement = select(Contact).where(Contact.first_name.ilike(f'%{contact_first_name}%'))
    result = await db.execute(statement)
    if result:
        return result.scalars().all()
    raise ValueError("204 No Content. The Search did not get results.")


async def search_by_lastname(contact_last_name: str, db: AsyncSession):
    statement = select(Contact).where(Contact.last_name.ilike(f'%{contact_last_name}%'))
    result = await db.execute(statement)
    if result:
        return result.scalars().all()
    raise ValueError("204 No Content. The Search did not get results.")


async def search_by_email(contact_email, db: AsyncSession):
    statement = select(Contact).where(Contact.email.ilike(f'%{contact_email}%'))
    result = await db.execute(statement)
    if result:
        return result.scalars().all()
    raise ValueError("204 No Content. The Search did not get results.")


async def search(query: str, db: AsyncSession):
    statement = select(Contact).where(or_(
        Contact.first_name.ilike(f'%{query}%'),
        Contact.last_name.ilike(f'%{query}%'),
        Contact.email.ilike(f'%{query}%')
    ))
    result = await db.execute(statement)
    return result.scalars().all()