from fastapi import FastAPI
from controllers.user_controller import user_controller
from fastapi.middleware.cors import CORSMiddleware

def include_routers(app):
	app.include_router(user_controller)
    # app.include_router(robot.robot_router)
    # app.include_router(match.match_router)

def start_application():
	app = FastAPI()
	include_routers(app)
	return app 

app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], 
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)