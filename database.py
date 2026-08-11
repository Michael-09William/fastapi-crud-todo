import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)


def init_db():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        if db.query(Task).count() == 0:
            sample_tasks = [
                Task(title="Buy groceries", done=False),
                Task(title="Complete Stage 1 assignment", done=True),
                Task(title="Read FastAPI documentation", done=False),
            ]
            db.add_all(sample_tasks)
            db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()