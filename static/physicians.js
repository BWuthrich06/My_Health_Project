'use strict';

let map;
let service;


let latLong;
let nearbyDoctors;
let allResults;
let allDetails;
let zipcode;


//Listens for search button to find physician.
const findPhysicianButton = document.querySelector("#search_result");
findPhysicianButton.addEventListener('click', async (evt) => {
    evt.preventDefault();
    
    // //Get zipcode user entered.
    zipcode = document.querySelector('#zipcode');
    zipcode = zipcode.value;

    //Check if zipcode entered is 5 digits.
    const regexZipcode = /\d{5}/;

    if (zipcode.length === 5 && regexZipcode.test(zipcode)) {
        latLong = await getLatLong(zipcode)
        console.log(latLong)
    
        if (latLong) {
            nearbyDoctors = await getNearbyDoctors(latLong);
                if (nearbyDoctors) {
                    // list to store all data from request
                    allResults = nearbyDoctors; 
                    console.log(allResults);
                  

                } else {
                    console.error(error);
                }
        };
        
                    if (allResults) {

                        allDetails = [];

                        for (const result of allResults) {

                            //Get each results place_id
                            let placeId = result.place_id;

                            //Get more details on each result from nearby doctors
                            let placeDetails = await getPlaceDetails(placeId);
                            console.log(placeDetails);
                            
                            if (placeDetails) {

                                //Dictionary of relevant data from place_details
                                let relDetails = {
                                    'name': placeDetails.name,
                                    'address': placeDetails.formatted_address,
                                    'phone': placeDetails.formatted_phone_number,
                                    'url': placeDetails.url,
                                    'place_id': placeDetails.place_id
                                    };

                                console.log(relDetails);
                    
                                //Add dictionary to all_details list
                                allDetails = allDetails.concat(relDetails);
                                }
                            }
                        console.log(allDetails)   
                        physicianResults();    

                    } else {
                        console.error("error");
                    };
    } else {
        const invalidZipcode = document.querySelector('#invalid_zipcode');
        const message = document.createElement('h5');
        invalidZipcode.appendChild(message);
        message.innerHTML = "Please enter valid 5 digit zipcode."

    };   
});

          


function initialize() { 
    map = new google.maps.Map(document.getElementById('physician_map'))
    service = new google.maps.places.PlacesService(map); // One object to represent the connection to Google Places
};




async function getLatLong(zipcode) {
//Takes in a zipcode and returns latitude,longitude.

    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${zipcode}&key=${key}`;

    //Make request to Google Geocode API to get latitude/longitude from zipcode
    const response = await fetch(url);
    const responseDATA = await response.json();

    if (responseDATA.results && responseDATA.results.length === 0) {
        const invalidZipcode = document.querySelector('#invalid_zipcode');
        const message = document.createElement('h5');
        invalidZipcode.appendChild(message);
        message.innerHTML = "Please enter valid 5 digit zipcode."

    } else {

        //Clear error message on browser
        const invalidZipcode = document.querySelector('#invalid_zipcode');
        invalidZipcode.innerHTML = ""

        //Latitude
        const latitude = responseDATA.results[0].geometry.location.lat;
     
        //Longitude
        const longitude = responseDATA.results[0].geometry.location.lng;
        const latLongResult = {'latitude': latitude, 'longitude': longitude};
             
        return latLongResult;
        

    }    
    
};



function getNearbyDoctors(latLong) {
//find all nearby doctors from zipcode entered, add data to allResults list
    return new Promise((resolve, reject) => {

    // //Get latitude and longitude
    const latitude = latLong.latitude;
    const longitude = latLong.longitude;

    // //Params to pass through to API request
    const dataType = "doctor";
    const radius = 16000;
    const destination = new google.maps.LatLng(latitude,longitude);

    const request = {
        location: destination,
        radius: radius,
        type: [dataType],
        };

    //Request to find all nearby doctors from zipcode entered, add data to allResults list
    service.nearbySearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            resolve(results)

        } else {
            reject("Error, request unsuccessfull.")
        }
        });

    });
};



function getPlaceDetails(placeId) {
    //Returns details of each place from location results."""
    return new Promise((resolve, reject) => {

    //Params I want back from request
    let fields=['place_id','name','formatted_address','formatted_phone_number','photos','url']

    //Required Params
    let request = {
        placeId: placeId,
        fields: fields,
        };

    //Request to place details
    service.getDetails(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            resolve(results);
         
        } else {
            reject("Error, request unsuccessful.");
        } 
    });
    });
};



function physicianResults() {
    //Renders details on webpage of each physician result.

    let physicianDetails = document.querySelector("#physicianResultsContainer");

    let searchResults = document.createElement('h2');
        physicianDetails.appendChild(searchResults);
        
        if (allDetails) {
            searchResults.innerHTML = `Search Results for ${zipcode}:`

        } else {
            searchResults.innerHTML = `No results near ${zipcode}`
        }
    
    for (const detail of allDetails) {

        let physicianHTML = document.createElement('div');
        physicianDetails.appendChild(physicianHTML);
        let individualDetail = document.createElement('p');
        physicianHTML.appendChild(individualDetail);
        
        //Concat string of name, address, phone, url with <br> between each.
        let detailString = ""

        if (detail.name) {
            let string1 = detail.name;
            detailString += '<br>' + string1;
        }

        if (detail.address) {
            const string2 = detail.address;
            detailString += '<br>'
            detailString += string2;
        }

        if (detail.phone) {
            const string3 = detail.phone;
            detailString += '<br>'
            detailString += string3;
        }

        if (detail.url) {
            const url = document.createElement('a');
            url.href = detail.url;
            url.innerText = "View on Map";
            const string4 = url.outerHTML;
            detailString += '<br>' + string4 + '<br>'
        }

        individualDetail.innerHTML = detailString;

        //Create add physician button for each entry
        const physicianButton = document.createElement('button');
        individualDetail.appendChild(physicianButton);
        physicianButton.innerText = "+ Add";
        physicianButton.classList.add('addPhysician');
};
};








//Event listoner for each Add Physician button
const addPhysicianButtons = document.querySelectorAll('button.addPhysician');
for (const addPhysicianButton of addPhysicianButtons) {
    addPhysicianButton.addEventListener('click', addPhysician);
    }



function addPhysician(evt) {
//Add physician to user profile page

    const data = {
        place_id : evt.target.id,
    }
    fetch('/add_physician', {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            window.location.pathname = ('/profile')
        })

    }
    
    
    




