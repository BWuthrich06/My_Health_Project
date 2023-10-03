import os
import json
# from datetime import datetime

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
    synonyms = condition["synonyms"]    #this is a list
    word_synonyms = condition["word_synonyms"]
    url = condition["info_link_data"] 


    if url and url[0]:
        url = url[0][0]     #url is at index 0 in list at index 0
    else:
        url = None


    if synonyms:
        all_synonyms = ','.join(synonyms)   #joining as a string
    else:
        all_synonyms = None     #if no synonyms exist


    if not word_synonyms:   #check to see if no word_synonyms exist
        word_synonyms = None


    #create condition and add to list
    new_condition = crud.create_condition(title, all_synonyms, word_synonyms, url)
    conditions_in_db.append(new_condition)

#Add and commit conditions to database
model.db.session.add_all(conditions_in_db)
model.db.session.commit()


