"""
The script exports the answer table to a CSV file. 

Config
------
CFG_NAME : The config name can be Develpment, Production

Output
------
The total location table in CSV file. (location_YYYY_MM_DD_HH_mm_ss.csv)

"""
#CFG_NAME = "config.config.DevelopmentConfig"
CFG_NAME = "config.config.ProductionConfig"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import csv
from models.model import db
from models.model import Location
from models.model_operations import location_operations
from models.model_operations import user_operations
from config.config import Config
from flask import Flask
from controllers import root
import datetime

# init db
app = Flask(__name__)
app.register_blueprint(root.bp)
app.config.from_object(CFG_NAME)
db.init_app(app)
app.app_context().push()

cvs_file_name = "location_" + datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"
print("Exporting answers to " + cvs_file_name + "...")

# Get all answers
location_query = Location.query.order_by(Location.factory_id)
locations = location_query.all()

with open(cvs_file_name, "w", newline="") as csvDataFile:
    # Write header
    csvWriter = csv.writer(csvDataFile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(["factory_id", "id", "done_at", "answer_count"])
    for location in locations:
        # Write each record in answer table
        csvWriter.writerow([location.factory_id, location.id, location.done_at, len(location.answers)])

print("{} records reported.".format(len(locations)))
db.session.remove()
db.session.close()
