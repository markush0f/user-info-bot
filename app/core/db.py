import os
from sqlmodel import Session, create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}"
    f"@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DATABASE')}"
)

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
