from fastapi import FastAPI
from controllers.robot_controller import robot_controller
from fastapi.middleware.cors import CORSMiddleware
# Just for integration testing:
# from pony.orm import db_session
# from database.models.models import User, Robot, db
# from passlib.hash import bcrypt
# from database.dao.user_dao import get_user_by_email

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

# db.drop_all_tables(with_all_data=True)
# db.create_tables()

# # Add some users to the database
# users = [
#     ('bas_benja', 'basbenja3@gmail.com', 'Compuamigos2', 555888, True),
#     ('juliolcese', 'juliolcese@mi.unc.edu.ar', '1whileTrue1', 889654, False),
#     ('tonimondejar', 'mondejarantonio@hotmail.com', 'FAMAFyC2022', 123456, True),
#     ('valennegrelli', 'valen57negrelli@yahoo.com.ar', 'piXies18', 852436, False),
#     ('sebagiraudo', 'sebagir4udo@unc.edu.ar', '15B_ikerfuliate', 785364, True),
#     ('lucasca22ina', 'cassinalucas@gmail.com', 'Loschicos1456', 152347, True),
#     ('israangulo4', 'isra1234@hotmail.com', 'Argentina222', 853314, False)
# ]
# with db_session:
#     for username, email, password, verification_code, verified in users:
#         User(
#             username=username,
#             email=email,
#             hashed_password=bcrypt.hash(password),
#             verification_code=verification_code,
#             verified=verified
#         )

# MOCK_SOURCE_CODE = """aW1wb3J0IHV2aWNvcm4KCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgog
#                       ICAgdXZpY29ybi5ydW4oImFwcC5hcGk6YXBwIiwgaG9zdD0iMC4wLjAuMCIs
#                       IHBvcnQ9ODAwMCwgcmVsb2FkPVRydWUp"""
# MOCK_AVATAR = """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQ
#                  DwAEhQGAhKmMIQAAAABJRU5ErkJggg=="""
# # Add some robots to the database
# robots = [
#     ('robot_cool', MOCK_SOURCE_CODE, 'isra1234@hotmail.com', MOCK_AVATAR),
#     ('world_destroyer_29', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
#     ('R2D2', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
#     ('WALL-E', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
#     ('jarvis22', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
#     ('_theTERMINATOR', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
#     ('0ptimusPrime', MOCK_SOURCE_CODE, 'basbenja3@gmail.com', MOCK_AVATAR),
#     ('CYborg34', MOCK_SOURCE_CODE, 'mondejarantonio@hotmail.com', MOCK_AVATAR),
#     ('automatax', MOCK_SOURCE_CODE, 'juliolcese@mi.unc.edu.ar', MOCK_AVATAR)
# ]
# with db_session:
#     for robot_name, source_code, owner_email, avatar in robots:
#         Robot(
#             name=robot_name,
#             source_code=source_code,
#             owner=get_user_by_email(owner_email),
#             avatar=avatar
#         )
