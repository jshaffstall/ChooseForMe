from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing

class RowTemplate2(RowTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def delete_click(self, **event_args):
        self.parent.raise_event('x-delete', item=self.item)

    def link_1_click(self, **event_args):
        routing.set_url_hash(f'choose?id={self.item["id"]}')
