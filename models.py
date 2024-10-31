from sqlalchemy import Column, Integer,Float, String, Date, Table, ForeignKey  # ייבוא מחלקים שונים של SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base  # ייבוא פונקציה ליצירת מודלים
from sqlalchemy.orm import relationship  # ייבוא פונקציה ליצירת קשרים בין מודלים


Base = declarative_base()

mission_country_targetType_target = Table(
    'mission_country_target',
    Base.metadata,
    Column('mission_id', Integer,ForeignKey('Missions.mission_id')),
    Column('country_id', Integer,ForeignKey('Countries.country_id')),
    Column('target_type_id', Integer,ForeignKey('TargetTypes.target_type_id')),
    Column('target_id', Integer,ForeignKey('Targets.target_id')),
)


# mission_country_relation = Table(
#     'mission_country',
#     Base.metadata,
#     Column('mission_id', Integer, primary_key=True),
#     Column('country_id', Integer, ForeignKey('countries.id')),
# )




class MissionModel(Base):
    __tablename__ = 'Missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Float)
    attacking_aircraft = Column(Float)
    bombing_aircraft = Column(Float)
    aircraft_returned = Column(Float)
    aircraft_failed = Column(Float)
    aircraft_damaged = Column(Float)
    aircraft_lost = Column(Float)

    countries = relationship('Countries',
                             secondary=mission_country_targetType_target,
                             backref='Missions',
                             )

    targetTypes = relationship('TargetTypes',
                               secondary=mission_country_targetType_target,
                               backref='Missions',
                               )


class TargetModel(Base):
    __tablename__ = 'Targets'
    target_id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey('Missions.mission_id'))
    target_industry = Column(String)
    city_id = Column(Integer)
    target_type_id = Column(Integer)
    target_priority = Column(Integer)

    missions = relationship('MissionModel',
                            secondary=mission_country_targetType_target,
                            backref='Targets',
                            )






    # countries = relationship(
    #     "CountryModel",
    #     secondary=mission_country_relation,
    #     back_populates="missions",
    # )

class CountryModel(Base):
    __tablename__ = 'Countries'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String)

    missions = relationship('MissionModel',
                            secondary=mission_country_targetType_target,
                            backref='Countries',
                            )


class TargetTypeModel(Base):
    __tablename__ = 'TargetTypes'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String)

    missions = relationship('MissionModel',
                            secondary=mission_country_targetType_target,
                            backref='TargetTypes',
                            )



