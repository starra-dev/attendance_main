from datetime import UTC , datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

#JWT_TOKEN=jwt-token-loggoogle-access

from config import settings


