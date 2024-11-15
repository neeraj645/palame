# app/helper/token_utils.py

import jwt
from datetime import datetime, timedelta
from flask import current_app as app

def generate_jwt_token(payload, expires_in=3600):
    """Generate a JWT token with the given payload and expiration time in seconds."""
    payload['exp'] = datetime.utcnow() + timedelta(seconds=expires_in)
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')



def decode_jwt_token(token):
    """Decode a JWT token to get the payload."""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired."
    except jwt.InvalidTokenError:
        return None, "Invalid token."
    except Exception as e:
        return None, str(e)