"""
The script exports the answer table to a CSV file. 

Config
------
CFG_NAME : The config name can be Develpment, Staging, Testing

Output
------
The total answer numbers after export, and the CSV file. (aswer_YYYY_MM_DD_HH_mm_ss.csv)

"""
CFG_NAME = "config.config.DevelopmentConfig"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import csv
from models.model import db
from models.model import Answer
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

answer_query = Answer.query.order_by(Answer.user_id)
answers = answer_query.all()

with open(cvs_file_name, "w", newline="") as csvDataFile:

    csvWriter = csv.writer(csvDataFile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(["Userid", "location_id", "answer_id", "land_usage", "expansion", "gold_standard_status", 
                        "bbox_left_top_lat", "bbox_left_top_lng", "bbox_bottom_right_lat", "bbox_bottom_right_lng", 
                        "zoom_level", "timestamp"])
    for answer in answers:
        csvWriter.writerow([answer.user_id, answer.location_id, answer.id, answer.land_usage,answer.expansion, 
        answer.gold_standard_status, answer.bbox_left_top_lat, answer.bbox_left_top_lng, answer.bbox_bottom_right_lat, 
        answer.bbox_bottom_right_lng, answer.zoom_level, answer.timestamp])

print("{} records reported.".format(len(answers)))
db.session.remove()
db.session.close()
