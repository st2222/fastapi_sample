import hashlib

from domain.models.user.password import HashedPassword, RawPassword


def hash_password(password: RawPassword):
    return HashedPassword(hashlib.sha256(password.value.encode()).hexdigest())



