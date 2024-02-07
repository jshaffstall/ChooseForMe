from ._anvil_designer import ListsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing
from ... import Cache

@routing.route('lists')
class Lists(ListsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.repeating_panel_1.add_event_handler('x-delete', self.delete_list)

        self.my_lists = anvil.server.call('get_lists')
        self.update()
        
    def update(self):
        self.no_lists_message.visible = len(self.my_lists) == 0
        self.data_grid_1.visible = len(self.my_lists) > 0
        self.repeating_panel_1.items = self.my_lists
        
    def delete_list(self, item, **event_args):
        if confirm(f"Do you really want to delete the list named {item['title']}?"):
            if Cache.list_id == item['id']:
                Cache.list_id = None
                Cache.temp_list = []
                Cache.list_name = None

            self.my_lists = anvil.server.call('delete_list', item)
            self.update()

