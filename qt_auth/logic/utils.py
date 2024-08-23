import base64
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings

from qt_user.models import User

KEY = base64.b64decode(settings.AUTH_KEY)


def clean_email(email: str) -> str:
    return email.lstrip().rstrip('\r\t\n. ')


def get_token_secure_key(user: User) -> str:
    password_bytes = user.password.encode('utf-8')
    user_salt = generate_salt(user)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=user_salt,
        iterations=100000,
        backend=default_backend()
    )

    derived_key = kdf.derive(password_bytes)

    h = hmac.HMAC(KEY, hashes.SHA256(), backend=default_backend())
    h.update(derived_key)
    token = h.finalize()

    return base64.b64encode(token).decode('utf-8')


def generate_salt(user: User) -> bytes:
    str_user_id = str(user.id)
    salt = hashlib.sha256(str_user_id.encode('utf-8')).digest()
    return salt[:16]
