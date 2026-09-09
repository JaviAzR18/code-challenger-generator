from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

load_dotenv()

clerk_sdk = Clerk(
    bearer_auth=os.getenv("CLERK_SECRET_KEY")
)


def authenticate_and_get_user_details(request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[
                    "http://localhost:5173",
                    "http://localhost:5174"
                ],
                jwt_key=os.getenv("CLERK_JWT_KEY"),
                clock_skew_in_ms=100000
            )
        )

        if not request_state.is_signed_in:
            raise HTTPException(
                status_code=401,
                detail=f"Authentication failed: {request_state.reason}"
            )

        return {
            "user_id": request_state.payload.get("sub")
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Authentication error: {str(e)}"
        )