import datetime
import bcrypt
import jwt
from cryptography.fernet import Fernet
from database import session
from model.user import User


# Encode the payload into a JWT using the secret key
def create_jwt(user):

    # Étape 1 : Génération de la clé secrète
    try:
        secret_key_bytes = Fernet.generate_key()
    except Exception as e:
        print(f"Erreur lors de la génération de la clé secrète : {e}")
        raise

    # Étape 2 : Création du payload JWT
    try:
        payload = {
            "id": user.id,
            "name_lastname": user.name_lastname,
            "department": user.department,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2)
        }
    except Exception as e:
        print(f"Erreur lors de la création du payload : {e}")
        raise

    # Étape 3 : Encodage du token JWT
    try:
        encoded_jwt = jwt.encode(payload, secret_key_bytes, algorithm="HS256")
    except Exception as e:
        print(f"Erreur lors de l'encodage du token : {e}")
        raise

    # Étape 4 : Affectation des valeurs à l'utilisateur
    try:
        user.secret_key = secret_key_bytes.decode('utf-8')
        user.token = encoded_jwt
    except Exception as e:
        print(f"Erreur lors de l'affectation des valeurs : {e}")
        raise

    # Étape 5 : Commit des changements dans la base de données
    try:
        session.commit()
    except Exception as e:
        print(f"Erreur lors du commit : {e}")
        session.rollback()  # Rollback en cas d'échec
        raise

    return encoded_jwt


# Query the database for a user with the given name and password
def check_user(name_lastname, raw_password):
    user = session.query(User).filter(User.name_lastname == name_lastname).first()

    if user and bcrypt.checkpw(raw_password.encode(), user.password.encode()):
        return user
    return None


# Query the database for a user with the given JWT
def check_token(token):
    user = session.query(User).filter(User.token == token).first()

    return user


# Decode the JWT using the user's secret key
def decode_token(token, user):
    secret_key_bytes = user.secret_key.encode('utf-8')
    try:
        decoded_jwt = jwt.decode(token, secret_key_bytes, algorithms=["HS256"])
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
