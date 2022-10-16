from fastapi import FastAPI
from controllers.robot_controller import robot_controller
from fastapi.middleware.cors import CORSMiddleware
from pony.orm import db_session
from database.models.models import User, Robot, db
from passlib.hash import bcrypt

db.drop_all_tables(with_all_data=True)
db.create_tables()

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

origins = [
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)