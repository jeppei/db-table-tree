import json

from db import DB
from db_navigator import DBNavigator


def test_get_parents_1(db_navigator):
    columns, parent_rows, _ = db_navigator.get_parents("users", "id", 1)

    print(json.dumps(columns, sort_keys=True, indent=4))
    print(pretty(parent_rows[0]))


def test_get_parents_0(db_navigator):
    columns, parent_rows, _ = db_navigator.get_parents("users", "user_settings_id", 9999999)

    print(json.dumps(columns, sort_keys=True, indent=4))
    print(pretty(parent_rows[0]))


def test_get_children(db_navigator):
    columns, parent_rows = db_navigator.get_children("users", 1)

    print(json.dumps(columns, sort_keys=True, indent=4))
    print(pretty(parent_rows[0]))


def test_get_primary_key(db_navigator):
    primary_key1 = db_navigator.get_primary_key_of_table("users")
    print(primary_key1)


def test_get_row_count_of_table(db_navigator):
    count = db_navigator.get_row_count_of_table("users")
    print(count)


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + '"' + str(key) + '":')
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


if __name__ == "__main__":
    db = DB("local")
    my_db_navigator = DBNavigator(db)
    test_get_primary_key(my_db_navigator)
    test_get_parents_1(my_db_navigator)
    test_get_parents_0(my_db_navigator)
    test_get_children(my_db_navigator)
    test_get_row_count_of_table(my_db_navigator)
