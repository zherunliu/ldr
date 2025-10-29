from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Challenge, ChallengeQuota

# for __name__ == __main__
# from models import Challenge, ChallengeQuota


# database operation on table challenge_quotas
def get_challenge_quota(db: Session, user_id: str):
    return db.query(ChallengeQuota).filter(ChallengeQuota.user_id == user_id).first()


def create_challenge_quota(db: Session, user_id: str):
    db_quota = ChallengeQuota(user_id=user_id)
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota)
    return db_quota


def reset_quota_if_need(db: Session, quota: ChallengeQuota):
    now = datetime.now()
    if now - quota.last_reset_date > timedelta(hours=24):  # type: ignore
        quota.quota_remaining = 10  # type: ignore
        quota.last_reset_date = now  # type: ignore
        db.commit()
        db.refresh(quota)
    return quota


# database operation on table challenges
def create_challenge(
    db: Session,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str,
):
    db_challenge = Challenge(
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


def get_user_challenges(db: Session, user_id: str):
    return db.query(Challenge).filter(Challenge.created_by == user_id).all()


def delete_user_challenge(db: Session, id: int):
    challenge = db.query(Challenge).get(id)
    if challenge:
        db.delete(challenge)
        db.commit()
        print(f"\033[1;31mDeleted challenge with id={id}\033[0m")
        return True
    return False


if __name__ == "__main__":
    from models import get_db

    db = next(get_db())
    delete_user_challenge(db, 3)
    challenge = db.query(Challenge).first()
    if challenge:
        print("first challenge id:", challenge.id)
