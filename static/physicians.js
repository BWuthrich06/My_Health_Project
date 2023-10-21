'use strict';

let map;
let service;

function initialize() {
 
    map = new google.maps.Map(document.getElementById('physician_map'))
    service = new google.maps.places.PlacesService(map); // One object to represent the connection to Google Places
}

//Takes in a zipcode and returns latitude,longitude.
async function getLatLong(zipcode) {

    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${zipcode}&key=${key}`;

    //Make request to Google Geocode API to get latitude/longitude from zipcode
    const response = await fetch(url);
    const responseDATA = await response.json();
    
    //Latitude
    const latitude = responseDATA.results[0].geometry.location.lat;
    console.log("Latitude:", latitude);
     
    //Longitude
    const longitude = responseDATA.results[0].geometry.location.lng;
    console.log("Longitude:", longitude);
            
    const latLongResult = {'latitude': latitude, 'longitude': longitude};
            
    return latLongResult;
};



function getNearbyDoctors(latLong, callback) {

    // //Get latitude and longitude
    const latitude = latLong.latitude;
    const longitude = latLong.longitude;

    // //Params to pass through to API request
    const dataType = "doctor";
    const radius = 16000;
    const destination = new google.maps.LatLng(latitude,longitude);

    // list to store all data from request
    let allResults = [];

    const request = {
        location: destination,
        radius: radius,
        type: [dataType]
        };

    //Request to find all nearby doctors from zipcode entered, add data to allResults list
    service.nearbySearch(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {

            console.log(results);
            let doctorData = results;
            allResults.push(doctorData);
            console.log(allResults);
            callback(allResults);
            }   
        })
       
}



let latLong;

//Listens for search button to find physician.
const findPhysicianButton = document.querySelector("#search_result");
findPhysicianButton.addEventListener('click', async (evt) => {
    evt.preventDefault();
    
    // //Get zipcode user entered.
    let zipcode = document.querySelector('#zipcode');
    zipcode = zipcode.value;
    console.log(zipcode)

    //Check if zipcode entered is 5 digits.
    const regexZipcode = /\d{5}/;

    if (zipcode.length === 5 && regexZipcode.test(zipcode)) {

         latLong = await getLatLong(zipcode)
         console.log(latLong)
    }
            if (latLong) {

                const nearbyDoctors = getNearbyDoctors(latLong, function() {
                    console.log(nearbyDoctors);
                    })
                   
            }
                
        
})
                        
 