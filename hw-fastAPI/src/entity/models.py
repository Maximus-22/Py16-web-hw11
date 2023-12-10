from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    phone_number = Column(String(24), nullable=False, index=True)
    birth_date = Column(Date, nullable=False, index=True)
    crm_status = Column(String, default='operational')
