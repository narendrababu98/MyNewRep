from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt_password(password):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_cxt.verify(plain_password, hash_password)
