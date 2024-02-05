from ._anvil_designer import ChooseTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing
import random
from ... import Cache

from ...TextEditInAlert import TextEditInAlert

@routing.route('choose')
@routing.route('choose', url_keys=['id'])
class Choose(ChooseTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.repeating_panel_1.set_event_handler('x-delete', self.delete_choice)
        self.repeating_panel_1.set_event_handler('x-edit', self.edit_choice)

        # TODO: see if we're being passed a list id and if so
        # load the saved list from the server

        self.list_name = None
        
        self.repeating_panel_1.items = Cache.temp_list
        self.panel_visibility()

    def panel_visibility(self):
        self.choices_panel.visible = len(Cache.temp_list) > 0
        self.choose.visible = len(Cache.temp_list) > 1
        self.list_name_panel.visible = 'id' in self.url_dict
        
    def delete_choice(self, choice, **event_args):
        if confirm(f"Really delete the choice: {choice['choice']}"):
            Cache.temp_list.remove(choice)
            self.repeating_panel_1.items = Cache.temp_list
            self.panel_visibility()

    def edit_choice(self, choice, **event_args):
        content = TextEditInAlert()
        content.text_box_1.text = choice['choice']
        alert(content, dismissible=False, title="Edit choice description")
        index = Cache.temp_list.index(choice)
        Cache.temp_list[index]['choice'] = content.text_box_1.text
        self.repeating_panel_1.items = Cache.temp_list
        
    def add_choice_click(self, **event_args):
        if not self.choice_box.text:
            return

        Cache.temp_list.append ({
            'choice': self.choice_box.text
        })

        self.repeating_panel_1.items = Cache.temp_list
        self.choice_box.text = ''
        self.choice_box.focus()
        self.panel_visibility()

    def choose_click(self, **event_args):
        choice = random.choice(Cache.temp_list)
        alert(f"We chose for you: {choice['choice']}")

    def clear_all_click(self, **event_args):
        if Cache.temp_list and confirm("Are you sure you want to clear all the choices?"):
            Cache.temp_list = []
            self.repeating_panel_1.items = Cache.temp_list
            self.choice_box.text = ''
            self.choice_box.focus()
            self.panel_visibility()                

    def timer_1_tick(self, **event_args):
        self.save_list.visible = bool(Cache.user)

    def save_list_click(self, **event_args):
        # TODO: save the list to the currently logged in user's
        # set of lists by asking the user to name the list
        # using an alert
        # 
        # after saving the list to the server reload the choose
        # page using the id of the list (replace the URL in history
        # so using the back button doesn't go to the non-saved choose page)
        pass

    def save_name_click(self, **event_args):
        # On first click enable the text box and change the icon on the button
        # to a check mark.  On second click update self.list_name with the text
        # box value, disable the text box, and change the icon back to the pencil
        pass
