from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import user_controller, robot_controller, match_controller

def include_controllers(app):
    app.include_router(user_controller.user_controller)
    # app.include_router(robot_controller.robot_controller)
    app.include_router(match_controller.match_controller)

def start_application():
	app = FastAPI()
	include_controllers(app)
	return app 

app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*", 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
