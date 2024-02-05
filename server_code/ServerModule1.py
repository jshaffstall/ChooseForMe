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

    list_choices = app_tables.choices.search(tables.order_by('description'), list=list_row)

    choices = []
    for choice in list_choices:
        choices.append({
            'choice': choice['description'],
            'id': choice['id']
        })
    
    return list_row['title'], choices

@anvil.server.callable
def create_list(list_name, choices):
    user = anvil.users.get_user()

    if not user:
        raise ValueError("Invalid user")

    list_id = str(uuid.uuid4())
    list_row = app_tables.lists.add_row(id=list_id, owner=user, title=list_name, modified=datetime.now())

    for choice in choices:
        app_tables.choices.add_row(description=choice['choice'], list=list_row, id=str(uuid.uuid4()), modified=datetime.now())

    return list_id

@anvil.server.callable
def update_list(list_id, list_name, choices):
    user = anvil.users.get_user()

    if not user:
        raise ValueError("Invalid user")

    list_row = app_tables.lists.get(id=list_id)

    if not list_row or list_row['owner'] != user:
        raise ValueError("Invalid list")

    # the choice might have an id and need updated or it
    # might be a new choice and need added.  If it has an id
    # it might not have been changed at all.
    for choice in choices:
        if 'id' in choice:
            choice_row = app_tables.choices.get(id=choice['id'], list=list_row)

            if not choice_row:
                raise ValueError("Invalid choice id")

            if choice_row['description'] != choice['choice']:
                choice_row['description'] = choice['choice']
                choice_row['modified'] = datetime.now()
        else:
            app_tables.choices.add_row(description=choice['choice'], list=list_row, id=str(uuid.uuid4()), modified=datetime.now())



