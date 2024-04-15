from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./bulletin_board/resources/bulletin_board.db"
ENGINE = create_engine(
    DB_URL,
    echo=True,
    pool_size=50,
    connect_args={"check_same_thread": False},
)
SESS_LOC = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


def get_db():
    db = SESS_LOC()
    try:
        yield db
    finally:
        db.close()
