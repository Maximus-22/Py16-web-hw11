from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal, Generic


# def validate_phone_number(cls, phone):
#     if not phone.isdigit():
#         raise ValueError('Phone number must contain only digits.')
#     return phone

# def validate_birth_date(cls, birth_date):
#     if len(str(birth_date)) != 10:
#         raise ValueError('Birth date must contain exactly 10 characters.')
#     return birth_date

class BirthDate(BaseModel):
    date: date

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, birth_date):
        if isinstance(birth_date, date):
            return cls(date=birth_date)
        try:
            return cls(date=date.fromisoformat(birth_date))
        except ValueError:
            pass
        try:
            return cls(date=datetime.strptime(birth_date, "%d-%m-%Y").date())
        except ValueError:
            raise ValueError("Invalid date format.")


class ContactSchema(BaseModel):
    # _validate_phone_number = validator('phone_number', allow_reuse=True)(validate_phone_number)
    # _validate_birth_date = validator('birth_date', allow_reuse=True)(validate_birth_date)

    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=3, max_length=32)
    email: EmailStr = Field(min_length=8, max_length=64)
    phone_number: int
    birth_date: BirthDate = Field(Generic)
    crm_status: Literal['operational', 'analitic', 'corporative'] = 'operational'

    @validator('phone_number')
    def validate_phone_number(cls, phone):
        if not phone.isdigit():
            raise ValueError('Phone number must contain only digits.')
        return phone
 
    @validator('birth_date')
    def validate_birth_date(cls, birth_date):
        if len(str(birth_date)) != 10:
            raise ValueError('Birth date must contain exactly 10 characters.')
        return birth_date


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponseSchema(ContactSchema):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    birth_date: date
    crm_status: Literal['operational', 'analitic', 'corporative']

    class Config:
        from_orm = True
