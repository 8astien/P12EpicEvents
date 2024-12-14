import sentry_sdk
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import exc, or_
from database import session

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def find_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id_):
        return session.query(cls).filter(cls.id == id_).first()

    @classmethod
    def create(cls, **kwargs):
        try:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            return instance
        except exc.SQLAlchemyError as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            raise ValueError(f"Error creating {cls.__name__}: {e}")

    @classmethod
    def delete(cls, instance):
        try:
            session.delete(instance)
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            raise ValueError(f"Error deleting {cls.__name__}: {e}")

    @classmethod
    def update(cls, instance, **kwargs):
        """
        Met à jour une instance en préservant les valeurs existantes
        si un champ dans kwargs est vide ou absent.
        """
        # Sauvegarder les données originales pour journalisation
        original_data = {key: getattr(instance, key) for key in kwargs.keys()}

        try:
            for key, value in kwargs.items():
                if key == 'password' and value:  # Hachage du mot de passe si nécessaire
                    value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
                # Ne mettre à jour que si une valeur valide est fournie
                if value not in [None, ""]:
                    setattr(instance, key, value)

            session.commit()

            # Capture des données mises à jour
            updated_data = {key: getattr(instance, key) for key in kwargs.keys()}
            sentry_sdk.capture_message(
                f"{cls.__name__} modifié : ID={instance.id}, Avant={original_data}, Après={updated_data}",
                level="info"
            )
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            raise ValueError(f"Error updating {cls.__name__}: {e}")
