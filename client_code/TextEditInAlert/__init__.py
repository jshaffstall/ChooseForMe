from ._anvil_designer import TextEditInAlertTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TextEditInAlert(TextEditInAlertTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.text_box_1.focus()

    def text_box_1_pressed_enter(self, **event_args):
        self.raise_event('x-close-alert')
