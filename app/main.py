from fastapi import FastAPI
from controllers.robot_controller import robot_controller
from fastapi.middleware.cors import CORSMiddleware

def include_controllers(app):
	# app.include_router(user.user_controller)
    app.include_router(robot_controller)
    # app.include_router(match.match_controller)
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
