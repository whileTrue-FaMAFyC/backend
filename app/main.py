from fastapi import FastAPI
from routers import match, robot, user

def include_routers(app):
	app.include_router(user.user_router)
    # app.include_router(robot.robot_router)
    # app.include_router(match.match_router)

def start_application():
	app = FastAPI()
	include_routers(app)
	return app 

app = start_application()