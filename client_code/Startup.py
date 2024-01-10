from anvil_extras import routing
import anvil.users
from .MainRouter import MainRouter
from . import Cache

Cache.user = anvil.users.get_user()

if Cache.user and not routing.get_url_hash():
    routing.set_url_hash('rooms')

routing.launch()