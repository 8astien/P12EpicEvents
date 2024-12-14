import datetime
import bcrypt
import jwt
from cryptography.fernet import Fernet
from database import session
from model.user import User


# Encode the payload into a JWT using the secret key
def create_jwt(user):
    secret_key_bytes = Fernet.generate_key()

    payload = {
        "id": user.id,
        "name_lastname": user.name_lastname,
        "department": user.department,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2)
    }

    encoded_jwt = jwt.encode(payload, secret_key_bytes, algorithm="HS256")

    user.secret_key = secret_key_bytes.decode('utf-8')
    user.token = encoded_jwt
    session.commit()

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
