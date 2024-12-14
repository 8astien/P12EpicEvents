from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import session
from .base import BaseModel
from utils import validate_email_format, validate_non_empty_string
import bcrypt
import sentry_sdk


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_lastname = Column(String(100), nullable=False)
    department = Column(Enum('COM', 'GES', 'SUP'), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    token = Column(String(300))
    secret_key = Column(String(300))

    customers = relationship('Customer', back_populates='user', lazy='select')
    events = relationship('Event', back_populates='user', lazy='select')

    @classmethod
    def create(cls, **kwargs):
        """Création d'un utilisateur avec hachage sécurisé du mot de passe."""
        if not validate_non_empty_string(kwargs.get('name_lastname')):
            raise ValueError("Invalid name: Name cannot be empty.")
        if not validate_email_format(kwargs.get('email')):
            raise ValueError("Invalid email format.")
        if not isinstance(kwargs.get('password'), str) or not kwargs['password'].strip():
            raise ValueError("Invalid password: Password cannot be empty or spaces only.")

        # Hachage du mot de passe
        kwargs['password'] = bcrypt.hashpw(kwargs['password'].encode(), bcrypt.gensalt()).decode()

        try:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            sentry_sdk.capture_message(
                f"Collaborateur créé : ID={instance.id}, Nom={instance.name_lastname}, Rôle={instance.department}",
                level="info"
            )
            return instance
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            raise ValueError(f"Error creating {cls.__name__}: {e}")

    def set_password(self, raw_password):
        """Met à jour le mot de passe avec un nouveau hash."""
        if not isinstance(raw_password, str) or not raw_password.strip():
            raise ValueError("Password cannot be empty or spaces only.")
        self.password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, raw_password):
        """Vérifie si un mot de passe brut correspond au hash stocké."""
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())
