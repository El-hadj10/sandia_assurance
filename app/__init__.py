from flask import Flask

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "dev-secret-key"  # Change this in production

from app import routes
from app.models import setup_database, teardown_appcontext

app.teardown_appcontext(teardown_appcontext)
setup_database()