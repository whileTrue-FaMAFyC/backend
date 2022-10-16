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


# Just to test integration with front-end
# from pony.orm import db_session
# from database.models.models import User
# from passlib.hash import bcrypt

# # Add some users to the database
# users = [
#     ('bas_benja', 'basbenja3@gmail.com', 'Compuamigos2', 555888, True),
#     ('juliolcese', 'juliolcese@mi.unc.edu.ar', '1whileTrue1', 889654, False),
#     ('tonimondejar', 'mondejarantonio@hotmail.com', 'FAMAFyC2022', 123456, True),
#     ('valennegrelli', 'valen57negrelli@yahoo.com.ar', 'piXies18', 852436, False),
#     ('sebagiraudo', 'sebagir4udo@unc.edu.ar', 'B_1kerfuliate', 785364, True),
#     ('lucasca22ina', 'cassinalucas@gmail.com', 'chicosSSS1456', 152347, True),
#     ('israangulo4', 'isra1234@hotmail.com', 'Argentiña222', 853314, True)
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