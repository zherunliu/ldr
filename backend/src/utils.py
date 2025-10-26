from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

# 查找 .env 文件并加载键值对
load_dotenv()
clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))


# authenticate and get user details
def authenticate(request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173"],
                jwt_key=os.getenv("JWT_KEY"),
            ),
        )
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = None
        if request_state.payload:
            user_id = request_state.payload.get("sub")
        return {"user_id", user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Invalid credentials: " + str(e))
