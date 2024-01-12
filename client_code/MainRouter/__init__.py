from ._anvil_designer import MainRouterTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil_extras import routing
from .. import Cache

from ..Pages.Home import Home
from ..Pages.Lists import Lists
from ..Pages.ListDetail import ListDetail
from ..Pages.Choose import Choose

@routing.default_template
class MainRouter(MainRouterTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.lists.tag.url_hash = 'lists'
        self.choose.tag.url_hash = 'choose'
        self.home.tag.url_hash = ''
    
        #self.link_visibility()

    def link_visibility(self):
        self.login.visible = not Cache.user
        self.logout.visible = bool(Cache.user)
        self.lists.visible = bool(Cache.user)

    def nav_click(self, sender, **event_args):
       routing.set_url_hash(sender.tag.url_hash)