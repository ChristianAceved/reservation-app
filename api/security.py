from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# Usaremos bcrypt para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    # Tomara una de las contraseñas y la hasheara usando bcrypt, devolviendo el hash resultante
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    # Verificara si la contraseña sin formato ( contraseña plana ) coincide con el hash almacenado, devolviendo True si coinciden o False si no
    return pwd_context.verify(plain_password, hashed_password)

# Funciones para manejo de tokens JWT (Json Web Tokens)
SECRET_KEY = "your_secret_key" # En un entorno de producción, esta clave debe ser segura y no debe estar hardcodeada y debe ser almacenada en un lugar seguro como variables de entorno como ENV o un servicio de gestión de secretos
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    # Creara un token JWT con la información proporcionada en el diccionario data, y una fecha de expiración opcional
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt