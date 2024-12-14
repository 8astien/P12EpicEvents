from model.customer import Customer
from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, joinedload
from .base import BaseModel
from database import session
from utils import validate_positive_float


class Contract(BaseModel):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    total_amount = Column(Float, default=0)
    settled_amount = Column(Float, default=0)
    remaining_amount = Column(Float, default=0)
    creation_date = Column(DateTime, default=func.now())
    contract_sign = Column(Boolean, default=False)

    customer = relationship('Customer', back_populates='contracts', lazy='select')
    events = relationship('Event', back_populates='contract', lazy='select')

    @classmethod
    def create(cls, **kwargs):
        if not validate_positive_float(kwargs.get('total_amount')):
            raise ValueError("Invalid total amount: Must be positive.")
        if not validate_positive_float(kwargs.get('settled_amount')):
            raise ValueError("Invalid settled amount: Must be positive.")
        if kwargs['settled_amount'] > kwargs['total_amount']:
            raise ValueError("Settled amount cannot exceed total amount.")

        kwargs['remaining_amount'] = kwargs['total_amount'] - kwargs['settled_amount']
        return super().create(**kwargs)

    @classmethod
    def find_by_sales_contact(cls, sales_contact_id):
        """Retrieve all contracts associated with a specific sales contact."""
        return (
            session.query(cls)
            .join(cls.customer)
            .filter(Customer.sales_contact == sales_contact_id)
            .options(joinedload(cls.customer))
            .all()
        )
