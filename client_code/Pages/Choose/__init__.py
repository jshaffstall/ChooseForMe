from ._anvil_designer import ChooseTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing
import random

from ...TextEditInAlert import TextEditInAlert

@routing.route('choose')
class Choose(ChooseTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.repeating_panel_1.set_event_handler('x-delete', self.delete_choice)
        self.repeating_panel_1.set_event_handler('x-edit', self.edit_choice)
        
        self.choices = []
        self.panel_visibility()

    def panel_visibility(self):
        self.choices_panel.visible = len(self.choices) > 0
        self.choose.visible = len(self.choices) > 1
        
    def delete_choice(self, choice, **event_args):
        if confirm(f"Really delete the choice: {choice['choice']}"):
            self.choices.remove(choice)
            self.repeating_panel_1.items = self.choices
            self.panel_visibility()

    def edit_choice(self, choice, **event_args):
        content = TextEditInAlert()
        content.text_box_1.text = choice['choice']
        alert(content, dismissible=False, title="Edit choice description")
        index = self.choices.index(choice)
        self.choices[index]['choice'] = content.text_box_1.text
        self.repeating_panel_1.items = self.choices
        
    def add_choice_click(self, **event_args):
        if not self.choice_box.text:
            return

        self.choices.append ({
            'choice': self.choice_box.text
        })

        self.repeating_panel_1.items = self.choices
        self.choice_box.text = ''
        self.choice_box.focus()
        self.panel_visibility()

    def choose_click(self, **event_args):
        choice = random.choice(self.choices)
        alert(f"We chose for you: {choice['choice']}")
