from fastapi import status, APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import *
from ..utils import authenticate
from ..database.models import get_db
import json
from datetime import datetime

router = APIRouter()


class ChallengeRequest(BaseModel):
    difficulty: str

    model_config = {"json_schema_extra": {"example": {"difficulty": "easy"}}}


@router.post("/generate-challenge")
async def generate_challenge(request: ChallengeRequest, db: Session = Depends(get_db)):
    try:
        user_details = authenticate(request)
        user_id = user_details.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized: missing user_id",
            )
        quota = get_challenge_quota(db, user_id)
        if not quota:
            create_challenge_quota(db, user_id)
        quota = reset_quota(db, quota)
        if quota.quota_remaining <= 0:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Quota exhausted"
            )
        challenge_data = None
        # TODO: generate challenge

        quota.quota_remaining -= 1  # type: ignore
        db.commit()
        return challenge_data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate(request)
    user_id = user_details.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: missing user_id",
        )

    challenges = get_user_challenges(db, user_id)
    return {"challenges": challenges}


@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate(request)
    user_id = user_details.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: missing user_id",
        )

    quota = get_challenge_quota(db, user_id)
    if not quota:
        create_challenge_quota(db, user_id)
    quota = reset_quota(db, quota)
    return quota
