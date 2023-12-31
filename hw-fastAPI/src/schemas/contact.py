import re
from datetime import datetime
from datetime import date

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal, Generic


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=3, max_length=32)
    email: EmailStr = Field(min_length=8, max_length=64)
    phone_number: str = Field(max_length=24)
    birth_date: str = Field(max_length=10)
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
        
        if not re.match(r'\d{4}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4}', birth_date):
            raise ValueError("Incorrect date format, Birth date should be in format [YYYY.MM.DD] or [DD.MM.YYYY].")

        if re.match(r'\d{4}\.\d{2}\.\d{2}', birth_date):
            return datetime.strptime(birth_date, '%Y.%m.%d').date()
        else:
            return datetime.strptime(birth_date, '%d.%m.%Y').date()


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponseSchema(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    crm_status: str

    class Config:
        from_orm = True
