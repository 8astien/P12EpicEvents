from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime, func
from sqlalchemy.orm import relationship
from .base import BaseModel
from utils import validate_email_format, validate_phone_number, validate_non_empty_string
from database import session


class Customer(BaseModel):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_lastname = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(BigInteger)
    business_name = Column(String(100))
    date_first_contact = Column(DateTime, default=func.now())
    last_date_update = Column(DateTime, default=func.now(), onupdate=func.now())
    sales_contact = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='customers', lazy='select')
    contracts = relationship('Contract', back_populates='customer', lazy='select')

    @classmethod
    def create(cls, **kwargs):
        if not validate_non_empty_string(kwargs.get('name_lastname')):
            raise ValueError("Nom invalide : ne peut pas être vide.")
        if not validate_email_format(kwargs.get('email')):
            raise ValueError("Format d'email invalide.")
        if not validate_phone_number(kwargs.get('phone')):
            raise ValueError("Numéro de téléphone invalide.")
        if not validate_non_empty_string(kwargs.get('business_name')):
            raise ValueError("Nom d'entreprise invalide : ne peut pas être vide.")

        return super().create(**kwargs)

    @classmethod
    def find_by_sales_contact(cls, sales_contact_id):
        """
        Trouve tous les clients associés à un vendeur spécifique.
        """
        return session.query(cls).filter(cls.sales_contact == sales_contact_id).all()
