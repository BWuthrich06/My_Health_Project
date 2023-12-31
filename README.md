# Continuing Care
Continuing Care enables individuals to gain more knowledge about their health and a convenient place to keep saved health information. Users can set up a personal account and search health conditions or view a page of all health conditions listed A to Z . Users will be able to view educational resources on each condition, add condition to personal profile and add/delete personalized comments to each condition. Users can also search for physicians nearby, add physician to profile for easy contact information and view location on map. Users can input their daily vitals to keep a record to bring to their physician. Additionally, all vitals will be viewable on a graph to observe a visual trend.

# View Demo Video: https://www.youtube.com/watch?v=wj3K6HyL52I

![Continuing Care Homepage](/static/images/Login.PNG)



# Learn more about the developer: www.linkedin.com/in/briana-wuthrich-dev

## Table of Contents
* [Technologies Used](#technologiesused)
* [Features of Continuing Care](#use)

## <a name="technologiesused">Technologies Used</a>

* Python
* Flask
* JavaScript
* AJAX
* PostgreSQL
* SQLAlchemy
* HTML
* Jinja
* CSS
* Bootstrap
* Passlib
* RegEx
* JSON
* ChartJS
* National Library of Medicine API
* Google Maps Geocode API
* Google Maps Places API

(dependencies are listed in requirements.txt)


## <a name="use">Features of Continuing Care</a>

Continuing Care is a full stack web application built with Python and Flask on the back end, and JavaScript on the front end. 
All pages were styled using a combination of CSS and Bootstrap components, ensuring a responsive layout for a user-friendly experience. 

* Create Account/Login 
    * To begin, users will be prompted to create a new account if they haven’t already, and login. 
    * A dedicated flask route handles the POST request and securely stores the login credentials in the session and in a Postgres database. 
    * Once logged in, users are directed to their profile page.

    ![Continuing Care Homepage](/static/images/Login.PNG)

    ![Continuing Care Homepage](/static/images/Create_New_Account.PNG)
    



* Search for Health Condition 
    * Users have the ability to search for specific health conditions. They can input the full or partial name or body part of the health condition, which will be sent to the server in a form submission. 

    ![Continuing Care Search for Health Condition](/static/images/Search_Health_Condition.PNG)

    * Utilizing SQLAlchemy queries on the Postgres, parsed with data from National Library of Medicine API, results are filtered and dynamically rendered to HTML using Jinja templating.  

    ![Continuing Care Search for Health Condition Results](/static/images/Search_Condition_Results.PNG)

    * Additionally, users can click on any health condition that will open a new browser tab with educational resources about the condition. 
    * If a user wishes to keep track of a health condition, they can add it to their personal profile for convenient reference. When the user clicks Add, an AJAX request will be sent to the server to query the database for the user and update Postgres with the user's saved condition. 
    * Users profile page will then render with the added health condition. 

    ![Continuing Care Profile Page Saved Health Conditions](/static/images/Profile_Health_Conditions.PNG)

    * Users will then be able to add and delete comments to conditions if they wish. 




* All Health Conditions A to Z

    * Users can view all health conditions listed out alphabetically.  
    * User can jump to section with "startswith" letter link.

    ![Continuing Care All Health Conditions A to Z](/static/images/Conditions_A_to_Z.PNG)



* Document Vitals 

    * Users will be able to record and store vital signs in Postgres.

    ![Continuing Care Document Vitals](/static/images/Record_Vitals.PNG)

    * View a detailed log with timestamps.

    ![Continuing Care All Vital Sign Results](/static/images/All_vitals.PNG)

    * Analyze trends with ChartJS easy-to-read graphs. 

    ![Continuing Care Vital Sign Graphs](/static/images/Vital_Graph.PNG)

    *Most Recent documented vital signs will be visible on user profile page.

    ![Continuing Care Profile Page Most Recent Vitals](/static/images/Profile_Vitals.PNG)
 
* Find Physician

    * The “Find Physician” feature allows users to input a zip code to retrieve nearby doctors.

    ![Continuing Care Find Physicians Nearby](/static/images/Search_Physician.PNG)

    * This feature proved to be my biggest challenge while building my web application since I needed to make 3 consecutive API calls: one to Google Maps Geocode API for latitude and longitude retrieval, the second and third to Google Maps Places API for detailed information on each nearby doctor. To manage this, I structured three functions to handle the API calls.  These were all asynchronous functions, so I needed to manage promises and make sure they were resolved in the right order. 

    ![Continuing Care Physicians Nearby Results](/static/images/Physician_Results.PNG)

    * Users can then save a physician to their profile, which also happens with a fetch request to my server. 
    * Users can now readily have available the contact information of each physician and can view their location on Google Maps for directions.

    ![Continuing Care Profile Saved Physicians](/static/images/Profile_Physicians.PNG)

* Logout
    * Users can logout once they are finished which will clear their login session.



