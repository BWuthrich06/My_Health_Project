import os
import json
from datetime import datetime

import crud
import server
import model

os.system("dropdb conditions")
os.system("createdb conditions")

model.connect_to_db(server.app)
model.db.create_all()


#Read json data
with open('data/health_conditions.json') as data:
    condition_data = json.loads(data.read())

#List to hold all conditions
conditions_in_db = []

#Loop through each condition: get title, synonyms and url
for condition in condition_data:
    
    title = condition["primary_name"]
    synonyms = condition["synonyms"]
    url = condition["info_link_data"]

    #create condition and add to list
    new_condition = crud.create_condition(title, synonyms, url)
    conditions_in_db.append(new_condition)

#Add and commit conditions to database
model.db.session.add_all(conditions_in_db)
model.db.session.commit()
