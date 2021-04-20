
import waitress
from bazblog import create_app

waitress.serve(create_app(), port=8080)
