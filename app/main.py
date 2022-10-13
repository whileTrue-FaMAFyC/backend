from fastapi import FastAPI
from controllers import match_controller

def include_routers(app):
	# app.include_router(user_controller.user_router)
    # app.include_router(robot_controller.robot_router)
    app.include_router(match_controller.controller)
    pass

def start_application():
	app = FastAPI()
	include_routers(app)
	return app 

app = start_application()