from fastapi import FastAPI
from controllers import *

def include_controllers(app):
	# app.include_router(user.user_controller)
    # app.include_router(robot.robot_controller)
    # app.include_router(match.match_controller)
    pass

def start_application():
	app = FastAPI()
	include_controllers(app)
	return app 

app = start_application()