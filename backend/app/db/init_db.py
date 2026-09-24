from app.db.base import Base
from app.db.session import engine
from app.models import user, document, chunk, conversation, message, evaluation

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
