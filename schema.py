import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType  # יבוא את SQLAlchemyObjectType המאפשר ליצור סוגים המבוססים על מודלים של SQLAlchemy.

from database import db_session
from models import MissionModel

class Mission(SQLAlchemyObjectType):
    class Meta:
        model = MissionModel
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    mission_by_id = graphene.Field(Mission, id=graphene.Int(required=True))
    mission_by_range_date = graphene.List(Mission, min_date=graphene.Date(), max_date=graphene.Date(), required=True) # בינתיים עד שנדע מה קורה עם התארכים, מה אני מקבל?
    mission_by_country = graphene.List(Mission, country=graphene.String(), required=True)

    @staticmethod
    def resolve_mission_by_id(self, info, id):
        return db_session.query(MissionModel).get(id)

    @staticmethod
    def resolve_mission_by_range_date(self, info, min_date, max_date):
        return db_session.query(MissionModel).filter(
            min_date <= MissionModel.mission_date <= max_date
        )

    # @staticmethod
    # def resolve_mission_by_country(self, country):
    #     return db_session.query(MissionModel).filter(
    #
    #     )




schema = graphene.Schema(query=Query)