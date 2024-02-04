import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import uuid
from datetime import datetime

@anvil.server.callable
def get_lists():
    user = anvil.users.get_user()

    if not user:
        raise ValueError("Invalid user")

    return app_tables.lists.search(tables.order_by('modified', ascending=False), owner=user)

@anvil.server.callable
def get_choices(list_id):
    user = anvil.users.get_user()

    if not user:
        raise ValueError("Invalid user")

    list_row = app_tables.lists.get(id=list_id, owner=user)

    if not list_row:
        raise ValueError("Invalid list id")

    # TODO: return a list of dictionaries so it can be updated
    # on the client and sent back to the server later
    return app_tables.choices.search(tables.order_by('description'), list=list_row)

@anvil.server.callable
def create_list(list_name, choices):
    user = anvil.users.get_user()

    if not user:
        raise ValueError("Invalid user")

    list_id = str(uuid.uuid4())
    list_row = app_tables.lists.add_row(id=list_id, owner=user, title=list_name, modified=datetime.now())

    # TODO: choices should be a list of dictionaries
    for choice in choices:
        app_tables.choices.add_row(description=choice, list=list_row, id=str(uuid.uuid4()), modified=datetime.now())

@anvil.server.callable
def update_list(list_row, list_name, choices):
    user = anvil.users.get_user()

    if not user:
        raise ValueError("Invalid user")

    list_row = app_tables.lists.get(id=list_row['id'])

    if not list_row or list_row['owner'] != user:
        raise ValueError("Invalid list")

    # TODO: choices should be a list of dictionaries
    for choice in choices:
        app_tables.choices.add_row(description=choice, list=list_row, id=str(uuid.uuid4()), modified=datetime.now())



