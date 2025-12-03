"""
The script loads the CSV and import the data into the location table.

Config
------
CSV_FILE_NAME : The CSV file to be import. Ensure the IDs are in row 1 (index from 0)
CFG_NAME : The config name can be Develpment, Staging, Testing

Output
------
The total location numbers after import.

"""
CSV_FILE_NAME = "1000_factories.csv"
CFG_NAME = "config.config.DevelopmentConfig"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import csv
from models.model import db
from models.model_operations import location_operations
from models.model_operations import answer_operations
from config.config import Config
from flask import Flask
from controllers import root

# init db
app = Flask(__name__)
app.register_blueprint(root.bp)
app.config.from_object(CFG_NAME)
db.init_app(app)
app.app_context().push()

count = location_operations.get_location_count()
print("Location count is ", count)

aCount = answer_operations.get_gold_answer_count();
print("Answer count is ", aCount);

db.session.remove()
db.session.close()
