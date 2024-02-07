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
        self.list_changed = False
        
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.repeating_panel_1.set_event_handler('x-delete', self.delete_choice)
        self.repeating_panel_1.set_event_handler('x-edit', self.edit_choice)

        # TODO: when clicking from a saved list after having started
        # a new list, the saved list doesn't get reloaded here
        # Why?
        
        # If the user is asking for a specific list, give it to them.
        # Otherwise, give them the list in the Cache.
        if 'id' in self.url_dict:
            Cache.list_name, Cache.temp_list = anvil.server.call('get_choices', self.url_dict['id'])
            Cache.list_id = self.url_dict['id']

        self.repeating_panel_1.items = Cache.temp_list
        self.panel_visibility()

    def panel_visibility(self):
        self.choices_panel.visible = len(Cache.temp_list) > 0
        self.choose.visible = len(Cache.temp_list) > 1
        self.list_name_panel.visible = Cache.list_id is not None
        self.needs_saved.visible = self.list_changed
        
    def delete_choice(self, choice, **event_args):
        if confirm(f"Really delete the choice: {choice['choice']}"):
            Cache.temp_list.remove(choice)
            self.repeating_panel_1.items = Cache.temp_list
            self.list_changed = True
            self.panel_visibility()

    def edit_choice(self, choice, **event_args):
        content = TextEditInAlert()
        content.text_box_1.text = choice['choice']
        alert(content, dismissible=False, title="Edit choice description")
        index = Cache.temp_list.index(choice)
        if Cache.temp_list[index]['choice'] != content.text_box_1.text:
            Cache.temp_list[index]['choice'] = content.text_box_1.text
            self.repeating_panel_1.items = Cache.temp_list
            self.list_changed = True
            self.panel_visibility()
        
    def add_choice_click(self, **event_args):
        if not self.choice_box.text:
            return

        Cache.temp_list.append ({
            'choice': self.choice_box.text
        })

        self.repeating_panel_1.items = Cache.temp_list
        self.choice_box.text = ''
        self.choice_box.focus()
        self.list_changed = True
        self.panel_visibility()

    def choose_click(self, **event_args):
        choice = random.choice(Cache.temp_list)
        alert(f"We chose for you: {choice['choice']}")

    def clear_all_click(self, **event_args):
        if self.list_changed and not confirm("Your current list has changed and not been saved.  Starting a new list at this point will lose those changes.  Are you sure you want to start a new list?"):
            return
            
        Cache.temp_list = []
        Cache.list_id = None
        Cache.list_name = None
        routing.set_url_hash('choose')

    def timer_1_tick(self, **event_args):
        self.save_list.visible = bool(Cache.user)

    def save_list_click(self, **event_args):
        # If the list already exists, need to update
        # it rather than create it.

        if Cache.list_id:
            anvil.server.call('update_list', Cache.list_id, Cache.list_name, Cache.temp_list)
            self.list_changed = False
            self.panel_visibility()  
        else:
            content = TextEditInAlert()
            alert(content, dismissible=False, title="Enter the list name")
            if not content.text_box_1.text:
                alert("You did not enter a list name, list not saved")
                return
    
            list_id = anvil.server.call('create_list', content.text_box_1.text, Cache.temp_list)
            routing.set_url_hash(f'choose?id={list_id}', replace_current_url=True)

    def save_name_click(self, **event_args):
        if self.list_name_box.enabled:
            self.save_name.icon = 'fa:pencil'
            self.list_name_box.enabled = False

            if self.list_name_box.text != Cache.list_name:
                Cache.list_name = self.list_name_box.text
                self.list_changed = False
                self.panel_visibility()  
        else:
            self.save_name.icon = 'fa:check'
            self.list_name_box.enabled = True

    def form_show(self, **event_args):
        self.panel_visibility()
        self.list_name_box.text = Cache.list_name    
