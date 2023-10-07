import os
import json


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


    if url != [] and url[0]:
        url = url[0][0]     #url is at index 0 in list at index 0
    else:
        url = None
    

    list_word_synonyms = word_synonyms.split(';')  #turns word_synonyms into list
    combined_synonyms = synonyms + list_word_synonyms  #combine both synonym lists into one
    set_synonyms = set(combined_synonyms)   #turn into set to remove duplicates
    list_all_synonyms = list(set_synonyms)   #turn back into list


    if list_all_synonyms:
        all_synonyms = ', '.join(list_all_synonyms)
    else:
        all_synonyms = None     #if no synonyms exist



    #create condition and add to list
    new_condition = crud.create_condition(title, all_synonyms, url)
    conditions_in_db.append(new_condition)

#Add and commit conditions to database
model.db.session.add_all(conditions_in_db)
model.db.session.commit()


