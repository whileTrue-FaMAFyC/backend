from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import user_controller, robot_controller, match_controller

def include_routers(app):
	app.include_router(user_controller.user_controller)
    # app.include_router(robot_controller.robot_router)
    # app.include_router(match_controller.match_router)

def start_application():
	app = FastAPI()
	include_routers(app)
	return app 

app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*", 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
