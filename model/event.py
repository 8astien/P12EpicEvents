from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, or_
from sqlalchemy.orm import relationship
from database import session
from .base import BaseModel
from utils import validate_non_empty_string, check_date_format, validate_positive_float


class Event(BaseModel):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    title = Column(String(100))
    date_hour_start = Column(DateTime)
    date_hour_end = Column(DateTime)
    address = Column(String(255))
    guests = Column(Integer, default=0)
    notes = Column(Text)
    support_contact = Column(Integer, ForeignKey('users.id'))

    contract = relationship('Contract', back_populates='events', lazy='select')
    user = relationship('User', back_populates='events', lazy='select')

    @classmethod
    def create(cls, **kwargs):
        if not validate_non_empty_string(kwargs.get('title')):
            raise ValueError("Invalid title: Cannot be empty.")
        if not check_date_format(kwargs.get('date_hour_start')):
            raise ValueError("Invalid start date format.")
        if not check_date_format(kwargs.get('date_hour_end')):
            raise ValueError("Invalid end date format.")
        if kwargs['date_hour_start'] >= kwargs['date_hour_end']:
            raise ValueError("Start date must be earlier than end date.")
        if not validate_non_empty_string(kwargs.get('address')):
            raise ValueError("Invalid address: Cannot be empty.")
        if not validate_positive_float(kwargs.get('guests')):
            raise ValueError("Invalid number of guests: Must be positive.")

        return super().create(**kwargs)

    @classmethod
    def find_events_without_support(cls):
        """Retourne tous les événements sans support associé."""
        return session.query(cls).filter(
            or_(
                cls.support_contact == None,
                cls.user == None
            )
        ).all()

    @classmethod
    def find_by_support_contact(cls, support_contact_id):
        """Retourne tous les événements assignés à un support spécifique."""
        return session.query(cls).filter(cls.support_contact == support_contact_id).all()
