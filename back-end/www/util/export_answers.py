"""
The script exports the answer table to a CSV file. 

Config
------
CFG_NAME : The config name can be Develpment, Staging, Testing

Output
------
The total answer numbers after export, and the CSV file. (aswer_YYYY_MM_DD_HH_mm_ss.csv)

"""
#CFG_NAME = "config.config.DevelopmentConfig"
CFG_NAME = "config.config.ProductionConfig"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import csv
from models.model import db
from models.model import Answer
from models.model_operations import location_operations
from models.model_operations import answer_operations
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

cvs_file_name = "answer_" + datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"
print("Exporting answers to " + cvs_file_name + "...")

# Get all answers
answer_query = Answer.query.order_by(Answer.user_id)
answers = answer_query.all()

with open(cvs_file_name, "w", newline="") as csvDataFile:
    # Write header
    csvWriter = csv.writer(csvDataFile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(["Userid", "client_id", "location_id", "factory_id", "answer_id", "land_usage", "expansion", "gold_standard_status", 
                        "year_old", "year_new", "bbox_left_top_lat", "bbox_left_top_lng", "bbox_bottom_right_lat", "bbox_bottom_right_lng", 
                        "zoom_level", "timestamp"])
    for answer in answers:
        # Write each record in answer table
        factory_id = location_operations.get_location_by_id(answer.location_id).factory_id
        client_id = user_operations.get_user_by_id(answer.user_id).client_id

        csvWriter.writerow([answer.user_id, client_id, answer.location_id, factory_id, answer.id, answer.land_usage,answer.expansion, 
        answer.gold_standard_status, answer.year_old, answer.year_new, answer.bbox_left_top_lat, answer.bbox_left_top_lng, answer.bbox_bottom_right_lat, 
        answer.bbox_bottom_right_lng, answer.zoom_level, answer.timestamp])

print("{} records reported.".format(len(answers)))
db.session.remove()
db.session.close()
