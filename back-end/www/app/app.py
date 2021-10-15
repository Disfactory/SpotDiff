from flask import Flask
from flask_cors import CORS
from models.model import db
from models.schema import ma


# Initialize the Web Server Gateway Interface
app = Flask(__name__)

# Load the settings in config.py
app.config.from_object("config.config.config")

# Setup CORS for development (so that localhost works)
if app.config["ENV"] == "development":
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize app with database
db.init_app(app)

# Initialize app with schema
ma.init_app(app)
