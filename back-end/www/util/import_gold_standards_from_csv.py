"""
The script loads the CSV and import the data into the answer table as gold standards.

Config
------
CSV_FILE_NAME : The CSV file to be import. Ensure the IDs are in row 1 (index from 0)
CFG_NAME : The config name can be Develpment, Staging, Testing

Output
------
The total location numbers after import.

"""
CSV_FILE_NAME = "gold_answers.csv"
CFG_NAME = "config.config.DevelopmentConfig"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import csv
from models.model import db
from models.model_operations import location_operations
from models.model_operations import answer_operations
from models.model_operations import user_operations
from config.config import Config
from flask import Flask
from controllers import root

# init db
app = Flask(__name__)
app.register_blueprint(root.bp)
app.config.from_object(CFG_NAME)
db.init_app(app)
app.app_context().push()

# If need to re-create the tables:
#db.drop_all()
#db.create_all()

admin_id = 0
ans_count = 0
u1 = user_operations.create_user("1117")
# open file for reading
with open(CSV_FILE_NAME) as csvDataFile:

    # read file as csv file 
    csvReader = csv.reader(csvDataFile)

    # Skip the first row of the field name
    next(csvReader)
    
    # for every row, insert the id(row 1) into the location table
    for row in csvReader:
        if row[0] is None:
            break
        location = location_operations.get_location_by_factory_id(row[0])
        if location is not None:
            print("location_id is: {}".format(row[0]))
            answer = answer_operations.create_answer(u1.id, location.id, int(row[2]), int(row[1]), "", int(row[3]), int(row[4]), 0)
            ans_count = ans_count + 1
        else:
            print("Cannot insert {}".format(row[0]))


print("Insert {} gold standards. ".format(ans_count))
total_ans_count = answer_operations.get_gold_answer_count()
print("Total gold standard cout is : {} ".format(total_ans_count))

db.session.remove()
db.session.close()
