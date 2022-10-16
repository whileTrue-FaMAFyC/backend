from controllers import match_controller
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def include_controllers(app):
	# app.include_router(user_controller.user_router)
    # app.include_router(robot_controller.robot_router)
    app.include_router(match_controller.controller)
    pass

def start_application():
	app = FastAPI()
	include_controllers(app)
	return app 

app = start_application()

origins = [
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
) 