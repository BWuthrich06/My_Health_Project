'use strict';

let map;
let service;


let latLong;
let nearbyDoctors;
let allResults;


//Listens for search button to find physician.
const findPhysicianButton = document.querySelector("#search_result");
findPhysicianButton.addEventListener('click', async (evt) => {
    evt.preventDefault();
    
    // //Get zipcode user entered.
    let zipcode = document.querySelector('#zipcode');
    zipcode = zipcode.value;

    //Check if zipcode entered is 5 digits.
    const regexZipcode = /\d{5}/;

    if (zipcode.length === 5 && regexZipcode.test(zipcode)) {
        latLong = await getLatLong(zipcode)
        console.log(latLong)
    }
        if (latLong) {
            nearbyDoctors = await getNearbyDoctors(latLong);
                if (nearbyDoctors) {
                    // list to store all data from request
                    allResults = nearbyDoctors; 
                    console.log(allResults);
                    console.log("Type:", typeof allResults);

                } else {
                    console.error(error);
                }
            }; 
        
                    if (allResults) {

                        let allDetails = [];

                        for (const result of allResults) {

                            console.log('result', result);
                            console.log("type", typeof result);

                            //Get each results place_id
                            let placeId = result.place_id;
                            console.log(placeId);

                            //Get more details on each result from nearby doctors
                            let placeDetails = getPlaceDetails(placeId);
                            console.log(placeDetails);

                            if (placeDetails) {

                                //Dictionary of relevant data from place_details
                                let relDetails = {
                                    'name': placeDetails.name,
                                    'address': placeDetails.formatted_address,
                                    'phone': placeDetails.formatted_phone_number,
                                    'url': placeDetails.url,
                                    };

                                console.log(relDetails);
                    
                                //Add dictionary to all_details list
                                allDetails = allDetails.push(relDetails);
                                console.log(allDetails);
                                }
                            }
                        return allDetails;    
        }              
    });



function getPlaceDetails(placeId) {
    //Returns details of each place from location results."""
    return new Promise((resolve, reject) => {

    //Params I want back from request
    let fields=['name','formatted_address','formatted_phone_number','photos','url']

    //Required Params
    let request = {
        placeId: placeId,
        fields: fields,
        };

    //Request to place details
    service.getDetails(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            console.log(results);
            resolve(results);
         
        } else {
            reject("Error, request unsuccessful.");
        } 
    });
    });
}
        


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
    
    //Latitude
    const latitude = responseDATA.results[0].geometry.location.lat;
     
    //Longitude
    const longitude = responseDATA.results[0].geometry.location.lng;
            
    const latLongResult = {'latitude': latitude, 'longitude': longitude};
            
    return latLongResult;
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
            console.log(results)
            resolve(results)

        } else {
            reject("Error, request unsuccessfull.")
        }
        });

    });
}



        