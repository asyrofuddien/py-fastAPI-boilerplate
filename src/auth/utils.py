from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.auth.config import auth_settings
from src.auth.schemas import TokenData
from src.exceptions import TokenExpired, InvalidCredentials


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=auth_settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        auth_settings.JWT_SECRET, 
        algorithm=auth_settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(
            token, 
            auth_settings.JWT_SECRET, 
            algorithms=[auth_settings.JWT_ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        
        if user_id is None or username is None:
            raise InvalidCredentials()
            
        return TokenData(user_id=user_id, username=username)
        
    except JWTError:
        raise InvalidCredentials()