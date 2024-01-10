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

@routing.default_template
class MainRouter(MainRouterTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
