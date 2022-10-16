from fastapi import FastAPI
from pony.orm import db_session
from controllers import match_controller
from database.dao import user_dao, robot_dao
from view_entities.user_view_entities import NewUserToDb
from view_entities.robot_view_entities import NewRobotTest
from fastapi.middleware.cors import CORSMiddleware
from database.models.models import db

@db_session
def initial_users():
    users = [
        ('basbenja', 'basbenja@gmail.com', "", 'compu2317', '12345', True),
        ('jolcese', 'juliolcese@gmail.com', "", 'Whil3True', '56542', True),
        ('tonimond', 'tonimondejar@gmail.com', "", '122e31', '58924', True)
    ]
    for username, email, avatar, password, verif_code, verified in users:
        user_dao.create_user(NewUserToDb(username = username, email = email, 
                                         avatar = avatar, hashed_password = password, 
                                         verification_code = verif_code, 
                                         verified = verified))
    return

@db_session
def initial_robots():
    src_code = "data:text/x-python;base64,aW1wb3J0IHV2aWNvcm4KCgppZiBfX25hb"\
               "WVfXyA9PSAiX19tYWluX18iOgogICAgdXZpY29ybi5ydW4oImFwcC5hcGk6"\
               "YXBwIiwgaG9zdD0iMC4wLjAuMCIsIHBvcnQ9ODAwMCwgcmVsb2FkPVRydWUp"
    robots = [
        ('robot1',"basbenja@gmail.com", "", src_code),
        ('robot2',"basbenja@gmail.com", "", src_code),
        ('robot1',"juliolcese@gmail.com", "", src_code),
        ('robot2',"juliolcese@gmail.com", "", src_code),
        ('robot1',"tonimondejar@gmail.com", "", src_code),
        ('robot2',"tonimondejar@gmail.com", "", src_code),
        ('robot3',"tonimondejar@gmail.com", "", src_code)        
    ]
    for name, owner, avatar, source_code in robots:
        robot_dao.create_robot(NewRobotTest(name = name, email = owner, 
                                            avatar = avatar, source_code = source_code))
    return


def include_controllers(app):
	# app.include_router(user.user_controller)
    # app.include_router(robot.robot_controller)
    app.include_router(match_controller.match_controller)
    pass

def start_application():
	app = FastAPI()
	include_controllers(app)
	return app 

app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# db.drop_all_tables(with_all_data = True)
# db.create_tables()
# initial_users()
# initial_robots()
