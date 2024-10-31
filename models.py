from sqlalchemy import Column, Integer,Float, String, Date, Table, ForeignKey  # ייבוא מחלקים שונים של SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base  # ייבוא פונקציה ליצירת מודלים
from sqlalchemy.orm import relationship  # ייבוא פונקציה ליצירת קשרים בין מודלים


Base = declarative_base()


class MissionModel(Base):
    __tablename__ = 'Mission'
    id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Float)
    attacking_aircraft = Column(Float)
    bombing_aircraft = Column(Float)
    aircraft_returned = Column(Float)
    aircraft_failed = Column(Float)
    aircraft_damaged = Column(Float)
    aircraft_lost = Column(Float)

