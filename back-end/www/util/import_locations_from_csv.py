"""
The script loads the CSV and import the data into the location table.

Config
------
CSV_FILE_NAME : The CSV file to be import. Ensure the IDs are in row 1 (index from 0)
CFG_NAME : The config name can be Develpment, Production

Output
------
The total location numbers after import.

"""
CSV_FILE_NAME = "production_20220505.csv"
CFG_NAME = "config.config.ProductionConfig"


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import csv
from models.model import db
from models.model_operations import location_operations
from config.config import Config
from flask import Flask
from controllers import root

# init db
app = Flask(__name__)
app.register_blueprint(root.bp)
app.config.from_object(CFG_NAME)
db.init_app(app)
app.app_context().push()

# If need to re-create the tables
#db.drop_all()
#db.create_all()

# open file for reading
with open(CSV_FILE_NAME) as csvDataFile:

    # read file as csv file 
    csvReader = csv.reader(csvDataFile)

    # Skip the first row of the field name
    next(csvReader)
    loc_count = 0;
    
    # for every row, insert the id(row 1) into the location table
    for row in csvReader:
        location = location_operations.get_location_by_factory_id(row[0])
        #print("location is", row[0])
        if location is None:
            location_operations.create_location(row[0]) 
            #print("import location ", row[0])
            loc_count = loc_count + 1
        

print("Import locations :", loc_count)
count = location_operations.get_location_count()
print("Location count is ", count)

db.session.remove()
db.session.close()
