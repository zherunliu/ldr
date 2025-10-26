from typing import Dict
from fastapi import status, HTTPException, Request
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

# 查找 .env 文件并加载键值对
load_dotenv()
clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))


# authenticate and get user details
def authenticate(request: Request) -> Dict[str, str | None]:
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173"],
                jwt_key=os.getenv("JWT_KEY"),
            ),
        )
        if not request_state.is_signed_in:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        user_id = None
        if request_state.payload:
            user_id = request_state.payload.get("sub")
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid credentials: " + str(e),
        )
