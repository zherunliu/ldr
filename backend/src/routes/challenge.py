from fastapi import status, APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import *
from ..utils import authenticate
from ..database.models import get_db
import json
from ..ai_generator import generate_challenge_with_ai

router = APIRouter()


class ChallengeRequest(BaseModel):
    difficulty: str

    model_config = {"json_schema_extra": {"example": {"difficulty": "easy"}}}


@router.post("/generate-challenge")
async def generate_challenge(
    request: ChallengeRequest, request_obj: Request, db: Session = Depends(get_db)
):
    try:
        user_details = authenticate(request_obj)
        user_id = user_details.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized: missing user_id",
            )
        quota = get_challenge_quota(db, user_id)
        if not quota:
            create_challenge_quota(db, user_id)
        quota = reset_quota_if_need(db, quota)
        if quota.quota_remaining <= 0:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Quota exhausted"
            )
        challenge_data = generate_challenge_with_ai(request.difficulty)
        new_challenge = create_challenge(
            db=db,
            difficulty=request.difficulty,
            created_by=user_id,
            options=json.dumps(challenge_data["options"]),
            correct_answer_id=challenge_data["correct_answer_id"],
            explanation=challenge_data["explanation"],
            title=challenge_data["title"],
        )

        quota.quota_remaining -= 1  # type: ignore
        db.commit()
        return {
            "id": new_challenge.id,
            "difficulty": request.difficulty,
            "title": new_challenge.title,
            "options": new_challenge.options,
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation,
            "timestamp": new_challenge.date_created.isoformat(),
        }

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
    quota = reset_quota_if_need(db, quota)
    return quota
