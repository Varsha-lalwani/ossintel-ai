import jwt
import os

from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SERVICE_ALLOWLIST = ["SSCA"]
SECRET_KEY = os.getenv("GENAI_SERVICE_SECRET")
security = HTTPBearer()


def authorize_request(authorization:
                      HTTPAuthorizationCredentials = Security(security),
                      ):
    if authorization.scheme != "Bearer":
        print("Invalid authorization scheme")

    # try:
    #     token = authorization.credentials
    #     claims = jwt.decode(token, options={"verify_signature": False})

    #     if ('sub' not in claims or
    #             claims['sub'] not in SERVICE_ALLOWLIST):
    #         raise HTTPException(status_code=401, detail="Invalid client")
    #     jwt.decode(token, SECRET_KEY, algorithms="HS256")
    #     return claims['sub']
    # except jwt.exceptions.PyJWTError as e:
    #     raise HTTPException(status_code=401, detail=str(e))
