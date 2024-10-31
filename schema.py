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
    resolve_mission_by_target_type = graphene.List(Mission, target_type=graphene.String())

# שאילתא 1
    @staticmethod
    def resolve_mission_by_id(self, info, id):
        return db_session.query(MissionModel).get(id)
# שאילתא 2
    @staticmethod
    def resolve_mission_by_range_date(self, info, min_date, max_date):
        return db_session.query(MissionModel).filter(
            and_(MissionModel.mission_date>=min_date, MissionModel.mission_date<=max_date)
        )
#שאילתא 3
    # @staticmethod
    # def resolve_mission_by_country(self, country_name):
    #     return db_session.query(MissionModel).filter(
    #
    #     )

# שאילתא 4
    # the function create a list and get the mission_ids then I get the missions list and get the missions from the list
    @staticmethod
    def resolve_mission_by_target_industry(self, info, target_industry):
        list_of_mission_ids = ([mis_id for mis_id in models.TargetModel.target_industry
                               if ["target_industry"] == target_industry])
        return [mis_id for mis_id in list_of_mission_ids if MissionModel.mission_id == mis_id]


# פטור משאילתא 5


# שאילתא 6
# אותה עבודה כמו בשאילתא הקודמת רק פה אני עובר על שדה בשם target_type_id
    @staticmethod
    def resolve_mission_by_target_type(self, info, target_type):
        list_of_mission_ids = ([mis_id for mis_id in models.TargetModel.target_type_id
                                if ["target_type"] == target_type])
        return [mis_id for mis_id in list_of_mission_ids if MissionModel.mission_id == mis_id]

#################################### Mutation  ################################

class AddMission(graphene.Mutation):
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

        mission = graphene.Field(lambda: Mission)

        def mutate(self, info, mission_id, mission_date,
                   airborne_aircraft, attacking_aircraft,
                   bombing_aircraft, aircraft_returned,
                   aircraft_failed, aircraft_damaged, aircraft_lost):
            mission = graphene.Field(lambda: Mission)
            new_mission = MissionModel(mission_date=mission_date, airborne_aircraft=airborne_aircraft,
                                       attacking_aircraft=attacking_aircraft, bombing_aircraft =bombing_aircraft
                                       , aircraft_returned=aircraft_returned,aircraft_failed=aircraft_failed,
                                       aircraft_damaged=aircraft_damaged, aircraft_lost=aircraft_lost
                                       )
            db_session.add(new_mission)
            db_session.commit()
            return AddMission(mission=mission)




class UpdateMissions(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        returned_aircraft = graphene.Float()
        failed_aircraft = graphene.Float()
        damaged_aircraft = graphene.Float()
        lost_aircraft = graphene.Float()
        damage_assessment = graphene.Float()

        def mutate(self, info, mission_id, returned_aircraft,
                   failed_aircraft,damaged_aircraft,
                   lost_aircraft, damage_assessment):
            mission = db_session.query(MissionModel).get(mission_id)
            if not mission:
                raise Exception("Mission not found")
            mission.returned_aircraft = returned_aircraft
            mission.failed_aircraft = failed_aircraft
            mission.damaged_aircraft = damaged_aircraft
            mission.lost_aircraft = lost_aircraft
            mission.damage_assessment = damage_assessment
            db_session.commit()
            return UpdateMissions(mission=mission)



class Mutation(graphene.ObjectType):
    add_mission = AddMission.Field()
    update_mission = UpdateMissions.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)