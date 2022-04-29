from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
#argon2: paquete para encriptar textos (cifrar y descifrar)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    #.verify() toma el texto del plain_password y lo compara con el hashed_password desencriptado


def get_password_hash(password): #Genera el codigo hash del texto que le estoy pasando
    return pwd_context.hash(password)