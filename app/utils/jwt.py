import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
from app.constants.environ import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, RESET_TOKEN_EXPIRE_MINUTES

load_dotenv()

# -------------------------
# ENV VARIABLES (CLEAN WAY)
# -------------------------




# -------------------------
# ACCESS TOKEN (LOGIN)
# -------------------------
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


