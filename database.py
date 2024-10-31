from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

connection_url = "postgresql://admin:1234@localhost:5437/missions_db"

engin = create_engine(connection_url, convert_unicode=True)


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engin))
def init_db():
    import models
    Base.metadata.create_all(bind=engin)