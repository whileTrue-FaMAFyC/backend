from fastapi import status
from fastapi.testclient import TestClient
import random
import string

from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI
from utils.user_utils import INVALID_TOKEN_EXCEPTION


# Usernames, robot names and match names used for the test
tokens = [MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI]
users = ['bas_benja', 'juliolcese', 'tonimondejar']
robots = [['0ptimusPrime', 'Bumblebee'], ['automatax',
                                          'astroGirl'], ['_tron', 'MegaByte', 'CYborg34']]
matches = []


client = TestClient(app)


def get_random_password():
    random_source = string.ascii_letters + string.digits + string.punctuation
    password = ""
    length = random.randint(0, 16)
    for i in range(length):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password


def get_random_match_name():
    password = ""
    random_source = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(3, 16)

    for i in range(length):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password


def client_put(creator_token: str, match_name: str, creator_robot: str,
               min_players: int, max_players: int, num_games: int,
               num_rounds: int, password: str):
    response = client.post(
        "/matches/new-match",
        headers={"authorization": creator_token},
        json={
            "name": match_name,
            "creator_robot": creator_robot,
            "min_players": min_players,
            "max_players": max_players,
            "num_games": num_games,
            "num_rounds": num_rounds,
            "password": password
        }
    )
    return response


def test_successful_creation_password():
    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    matches.append((creator_user, match_name))

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = get_random_password()

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_201_CREATED)


def test_successful_creation_no_password():
    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    matches.append((creator_user, match_name))

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = ""

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_201_CREATED)


def test_invalid_robot():
    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while ((creator_user, match_name) in matches):
        match_name = get_random_match_name()

    creator_robot = 'unexistent robot'

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_409_CONFLICT)
    assert response.json()["detail"] == f"Robot {creator_robot} isn't "\
                                        f"in {creator_user}'s library. "


def test_match_name_used():
    match_name = "match1"

    creator_user = "bas_benja"
    user_index = users.index(creator_user)

    creator_token = MOCK_TOKEN_BENJA

    user_index = 0
    while (users[user_index] != creator_user):
        user_index = user_index + 1

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_409_CONFLICT)
    assert response.json()["detail"] == f"{creator_user} already has a match "\
                                        f"named {match_name}. "


def test_invalid_min_players():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while ((creator_user, match_name) in matches):
        match_name = get_random_match_name()

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([random.randint(-100, 1),
                                random.randint(5, 100)])

    max_players = random.randint(2, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    # Here max_players will be between 2 and 4, but that could be a smaller
    # value than min_players, so the detail would include that.
    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert ("Minimum amount of players has to be between 2 and 4."
            in response.json()["detail"])


def test_invalid_max_players():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while ((creator_user, match_name) in matches):
        match_name = get_random_match_name()

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.choice([random.randint(-100, 1),
                                 random.randint(5, 100)])
    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert ("Maximum amount of players has to be between 2 and 4. "
            in response.json()["detail"])


def test_min_greater_than_max():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while ((creator_user, match_name) in matches):
        match_name = get_random_match_name()

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.randint(3, 4)

    max_players = random.randint(2, min_players - 1)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert response.json()["detail"] == "Minimum amount of players can't be " \
                                        "greater than maximum amount of " \
                                        "players. "


def test_invalid_games():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while ((creator_user, match_name) in matches):
        match_name = get_random_match_name()

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.choice([random.randint(-100, 0),
                               random.randint(201, 300)])

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert response.json()["detail"] == "Number of games has to be between "\
                                        "1 and 200. "


def test_invalid_rounds():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while ((creator_user, match_name) in matches):
        match_name = get_random_match_name()

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.choice([random.randint(-100, 0),
                                random.randint(10001, 10100)])

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert response.json()["detail"] == "Number of rounds has to be between "\
                                        "1 and 10000. "


def test_long_password():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while ((creator_user, match_name) in matches):
        match_name = get_random_match_name()

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = "thisHasMoreThan16Characters"

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert response.json()["detail"] == "The password can't have more than "\
                                        "16 characters. "


def test_long_match_name():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]

    match_name = "thisHasMoreThan16Characters"

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert response.json()["detail"] == "The match name has to have between "\
                                        "3 and 16 characters. "


def test_short_match_name():

    user_index = random.randint(0, 2)
    creator_token = tokens[user_index]

    match_name = "ab"

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == (status.HTTP_400_BAD_REQUEST)
    assert response.json()["detail"] == "The match name has to have between "\
                                        "3 and 16 characters. "


def test_invalid_token():
    user_index = random.randint(0, 2)
    creator_token = ""

    match_name = get_random_match_name()

    robot_index = random.randint(0, max(1, user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2, 3, 4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = get_random_password()

    response = client_put(creator_token, match_name, creator_robot, min_players,
                          max_players, num_games, num_rounds, password)

    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail
