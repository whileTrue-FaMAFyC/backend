from fastapi import FastAPI
from controllers import match_controller, robot_controller, user_controller

def include_routers(app):
	# app.include_router(user.user_router)
    # app.include_router(robot.robot_router)
    app.include_router(match_controller.controller)
    pass

def start_application():
	app = FastAPI()
	include_routers(app)
	return app 

app = start_application()