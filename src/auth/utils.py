import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.auth.config import auth_settings
from src.auth.schemas import TokenData
from src.exceptions import TokenExpired, InvalidCredentials


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with proper length handling."""
    # Convert to bytes and truncate if necessary (bcrypt 72-byte limit)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash with proper length handling."""
    try:
        # Convert to bytes and truncate if necessary
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Convert hashed password to bytes
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Verify password
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


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