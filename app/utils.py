from passlib.context import CryptContext

pwd_contest = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_contest.hash(password)
