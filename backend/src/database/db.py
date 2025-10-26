from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models


# database operation
def get_challenge_quota(db: Session, user_id: str):
    return (
        db.query(models.ChallengeQuota)
        .filter(models.ChallengeQuota.user_id == user_id)
        .first()
    )


def create_challenge_quota(db: Session, user_id: str):
    db_quota = models.ChallengeQuota(user_id=user_id)
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota)
    return db_quota


def reset_quota(db: Session, quota: models.ChallengeQuota):
    now = datetime.now()
    if now - quota.last_reset_date > timedelta(hours=24): # type: ignore
        quota.quota_remaining = 10 # type: ignore
        quota.last_reset_date = now # type: ignore
        db.commit()
        db.refresh(quota)
    return quota


def create_challenge(
    db: Session,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str,
):
    db_challenge = models.Challenge(
        difficulty=difficulty,
        created_by=created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation,
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def get_user_challenge(db: Session, user_id: str):
    return (
        db.query(models.Challenge).filter(models.Challenge.create_by == user_id).all()
    )
