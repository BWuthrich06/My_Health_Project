'use strict';

let map;
let service;

let latLong;
let nearbyDoctors;
let allResults;
let allDetails;
let zipcode;
let searchResults;
let relDetails;


//Listens for search button to find physician.
const findPhysicianButton = document.querySelector("#search_result");
if (findPhysicianButton) {
    findPhysicianButton.addEventListener('click', async (evt) => {
        evt.preventDefault();

        let physicianDetails = document.querySelector('#physicianResultsContainer');
        physicianDetails.innerHTML = "";
        let invalidZipcode = document.querySelector('#invalid_zipcode');
        invalidZipcode.innerHTML = "";
        
        // //Get zipcode user entered.
        zipcode = document.querySelector('#zipcode');
        zipcode = zipcode.value;
    
        //Check if zipcode entered is 5 digits.
        const regexZipcode = /^\d{5}$/;
    
        if (zipcode.length === 5 && regexZipcode.test(zipcode)) {
            latLong = await getLatLong(zipcode)

        } else{

            //Message to appear on browser for invalid zipcode.
            invalidZipcode = document.querySelector('#invalid_zipcode');
            invalidZipcode.innerHTML = "";
            const message = document.createElement('h5');
            invalidZipcode.appendChild(message);
            message.innerHTML = "Please enter valid 5 digit zipcode."
        }
        
            if (latLong) {
                nearbyDoctors = await getNearbyDoctors(latLong);
            
                    if (nearbyDoctors.results.length > 0) {

                        // list to store all data from request
                        allResults = [];

                        for (let result in nearbyDoctors.results) {
                            allResults.push(nearbyDoctors.results[result]);
                        };

                        physicianDetails = document.querySelector("#physicianResultsContainer");
                        physicianDetails.innerHTML = "";
                        searchResults = document.createElement('h2');
                        physicianDetails.appendChild(searchResults);

                        if (allResults.length !== 0) {
                            //Show results for entered zipcode on webpage
                            let physicianDetails = document.querySelector("#physicianResultsContainer");
                            searchResults = document.createElement('h2');
                            physicianDetails.appendChild(searchResults);
                            searchResults.innerHTML =`Results near ${zipcode}:`
                        
                            //Array to hold all relDetails
                            allDetails = []
    
                            //Loop through each result
                            for (let result of allResults) {
    
                                //Get each results place_id
                                let placeId = result.place_id;
                            
                                //Get details on each result from nearby doctors
                                let placeDetails = await getPlaceDetails(placeId);
                                
                                if (placeDetails) {
    
                                    //Dictionary of relevant data from placeDetails
                                    relDetails = {
                                        'name': placeDetails.name,
                                        'address': placeDetails.formatted_address,
                                        'phone': placeDetails.formatted_phone_number,
                                        'url': placeDetails.url,
                                        'place_id': placeDetails.place_id
                                        }
    
                                        //Add each relDetials to allDetails array
                                        allDetails = allDetails.concat(relDetails);
    
                                        //Call function that renders result to webpage
                                        physicianResults(relDetails);
                                }
                            }
                            console.log(allDetails);
                            return allDetails;
    
                    } else {
                        //Show no results on webpage.
                        physicianDetails = document.querySelector("#physicianResultsContainer");
                        physicianDetails.innerHTML = "";
                        searchResults = document.createElement('h2');
                        physicianDetails.appendChild(searchResults);
                        searchResults.innerHTML = "";
                        searchResults.innerHTML = `No results near ${zipcode}`
                    }};


}})}
;



function initialize() { 
    map = new google.maps.Map(document.getElementById('physician_map'));
    service = new google.maps.places.PlacesService(map); // One object to represent the connection to Google Places
};



async function getLatLong(zipcode) {
//Takes in a zipcode and returns latitude,longitude.

    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${zipcode}&key=${key}`;

    //Make request to Google Geocode API to get latitude/longitude from zipcode
    const response = await fetch(url);
    const responseDATA = await response.json();

    //If results empty
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
             
        console.log(latLongResult)
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
        const radius = 5000;
        const destination = new google.maps.LatLng(latitude,longitude);

        const request = {
            location: destination,
            radius: radius,
            type: [dataType],
            };

        //counter for requests
        let count = 0

        //List to hold all results
        let allResults = []

        //Request to find all nearby doctors from zipcode entered, add data to allResults list
        service.nearbySearch(request, async (results, status, pagination) => {
        
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                for (let result of results) {
                    allResults.push(result)
                };
                
                if (pagination && pagination.hasNextPage && count < 3) {
                    //Sleep delay for next page request
                    // const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
                    // await sleep(1000);
                    
                    //next page request
                    count += 1;
                    console.log(count);
                    pagination.nextPage();
                        
                } else {
                    resolve({results: allResults});
                }

            } else {
                resolve({results: []});
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



function physicianResults(relDetails) {
    //Renders details on webpage of each physician result.

    let physicianDetails = document.querySelector("#physicianResultsContainer");
    let physicianHTML = document.createElement('div');
    physicianDetails.appendChild(physicianHTML);
    let individualDetail = document.createElement('p');
    physicianHTML.appendChild(individualDetail);
    
    //Concat string of name, address, phone, url with <br> between each.
    let detailString = ""

    //Add name to string
    if (relDetails.name) {
        let string1 = relDetails.name;
        detailString += '<br>' + string1;
    }

    //Add address to string
    if (relDetails.address) {
        const string2 = relDetails.address;
        detailString += '<br>';
        detailString += string2;
    };

    //Add phone number to string
    if (relDetails.phone) {
        const string3 = relDetails.phone;
        detailString += '<br>';
        detailString += string3;
    };

    //Add url to string
    if (relDetails.url) {
        const url = document.createElement('a');
        url.href = relDetails.url;
        url.innerText = "View Map";
        url.classList.add('hyperlink');
        const string4 = url.outerHTML;
        detailString += '<br>' + string4 + '<br>';
    };

    //Render string to webpage
    individualDetail.innerHTML = detailString;


    //Create add physician button for each entry
    const physicianButton = document.createElement('button');
    physicianButton.id = relDetails.place_id;
    physicianButton.classList.add('addPhysician');
    physicianButton.innerText = "+ Add";
    individualDetail.appendChild(physicianButton);

    physicianButton.addEventListener('click', () => {
        addPhysician(relDetails);
    });
};


function addPhysician(relDetails) {
//Add physician to user profile page

    const data = {
        place_id : relDetails.place_id,
        name: relDetails.name,
        address: relDetails.address,
        phone: relDetails.phone,
        url: relDetails.url
    };

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

        .catch((error) =>
            console.log('Error', error))
    };