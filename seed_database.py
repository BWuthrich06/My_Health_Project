import os
import json

import crud
import server
import model

from datetime import date

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
        all_synonyms = all_synonyms.lower()
        all_synonyms = all_synonyms.title()
    else:
        all_synonyms = None     #if no synonyms exist



    #create condition and add to list
    new_condition = crud.create_condition(title, all_synonyms, url)
    conditions_in_db.append(new_condition)

#Add and commit conditions to database
model.db.session.add_all(conditions_in_db)
model.db.session.commit()



#Test user for test cases
user1 = model.User(email='hello@123.com', name="Briana", password="hello")
model.db.session.add(user1)
model.db.session.commit()

user2 = model.User(email="goodbye@123.com", name="Paul", password="goodbye")
model.db.session.add(user2)
model.db.session.commit()

user3 = model.User(email="wonderful@123.com", name="Wonder", password="wonderful")
model.db.session.add(user3)
model.db.session.commit()

#Test conditions
condition = model.Condition.query.get(1)

#Test user_conditions
user_condition1 = model.User_condition(user_id=1, condition_id=1, date_added=date.today())
model.db.session.add(user_condition1)
model.db.session.commit()

user_condition2 = model.User_condition(user_id=1, condition_id=2, date_added=date.today())
model.db.session.add(user_condition2)
model.db.session.commit()

user_condition3 = model.User_condition(user_id=2, condition_id=3, date_added=date.today())
model.db.session.add(user_condition3)
model.db.session.commit()

#Test comments
comment1 = model.Comment(comment="This is a comment", favorite_id=1)
model.db.session.add(comment1)
model.db.session.commit()

comment2 = model.Comment(comment="This is a second comment", favorite_id=1)
model.db.session.add(comment2)
model.db.session.commit()

comment3 = model.Comment(comment="This is a third comment", favorite_id=2)
model.db.session.add(comment3)
model.db.session.commit()

