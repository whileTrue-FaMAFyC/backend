from database.dao.user_dao import get_user_by_username, unverified_users_cleanup

not_deleted = ["bas_benja", "juliolcese", "sebagiraudo", "lucasca22ina", "israangulo4"]

deleted = ["tonimondejar", "valennegrelli"]

def test_unverified_users_cleanup():
    unverified_users_cleanup()

    for user in not_deleted:
        assert(get_user_by_username(user)) != None
     
    for user in deleted:
        assert(get_user_by_username(user)) == None
