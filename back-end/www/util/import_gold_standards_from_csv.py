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
CSV_FILE_NAME = "answer_gold_standard_update20220419.csv"
#CSV_FILE_NAME = "50_answer_gold_standard.csv"

# For Staging server
CFG_NAME = "config.config.DevelopmentConfig"

# For production server
#CFG_NAME = "config.config.ProductionConfig" 

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
update_count = 0
u1 = user_operations.get_user_by_client_id("admin")
if u1 is None:
    print("Create admin.")
    u1 = user_operations.create_user("admin")
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
        if location is None:
            location = location_operations.create_location(row[0])
            print("Create location : {}".format(location.id))

        gold_answer = answer_operations.get_gold_answer_by_location(location.id)

        # If the gold answer exists, and the new gold_standard_status is specified
        if gold_answer is not None and len(row) >5 and row[5] is not None:
            answer_operations.set_answer_gold_standard_status(gold_answer.id, int(row[5]))
            print("Update gold_standard_status of answer of location {}".format(row[0]))
            update_count = update_count + 1
        elif gold_answer is None:
            # If the gold standard doesn't exist, and the file specify a gold standard, or in old format to create one
            if (len(row) > 5 and int(row[5]) == 0) or (len(row) <= 5):
                answer = answer_operations.create_answer(u1.id, location.id, int(row[2]), int(row[1]), "", int(row[3]), int(row[4]), 0)
                print("create answer")
                ans_count = ans_count + 1
        

print("Updated {} gold standards.".format(update_count))
print("Insert {} gold standards. ".format(ans_count))
total_ans_count = answer_operations.get_gold_answer_count()
print("Total gold standard cout is : {} ".format(total_ans_count))

db.session.remove()
db.session.close()
