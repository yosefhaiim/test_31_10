from audioop import maxpp

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType  # יבוא את SQLAlchemyObjectType המאפשר ליצור סוגים המבוססים על מודלים של SQLAlchemy.
from sqlalchemy import and_

import models
from database import db_session
from models import MissionModel

class Mission(graphene.ObjectType):
    class Meta:
        model = MissionModel
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    mission_by_id = graphene.Field(Mission, id=graphene.Int(required=True))
    mission_by_range_date = graphene.List(Mission, min_date=graphene.Date(), max_date=graphene.Date(), required=True) # בינתיים עד שנדע מה קורה עם התארכים, מה אני מקבל?
    # mission_by_country = graphene.List(Mission, country=graphene.String(), required=True)
    mission_by_target_industry = graphene.List(Mission, target_industry=graphene.String())



    @staticmethod
    def resolve_mission_by_id(self, info, id):
        return db_session.query(MissionModel).get(id)

    @staticmethod
    def resolve_mission_by_range_date(self, info, min_date, max_date):
        return db_session.query(MissionModel).filter(
            and_(MissionModel.mission_date>=min_date, MissionModel.mission_date<=max_date)
        )

    # @staticmethod
    # def resolve_mission_by_country(self, country_name):
    #     return db_session.query(MissionModel).filter(
    #
    #     )


    # the function create a list and get the mission_ids then I get the missions list and get the missions from the list
    @staticmethod
    def resolve_mission_by_target_industry(self, info, target_industry):
        list_of_mission_ids = ([mis_id for mis_id in models.TargetModel.target_industry
                               if ["target_industry"] == target_industry])
        return [mis_id for mis_id in list_of_mission_ids if MissionModel.mission_id == mis_id]



#################################### Mutation  ################################

class AddMissions(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True, primary_key=True)
        mission_date = graphene.Date(required=True)
        airborne_aircraft = graphene.Float()
        attacking_aircraft = graphene.Float()
        bombing_aircraft = graphene.Float()
        aircraft_returned = graphene.Float()
        aircraft_failed = graphene.Float()
        aircraft_damaged = graphene.Float()
        aircraft_lost = graphene.Float()



schema = graphene.Schema(query=Query)