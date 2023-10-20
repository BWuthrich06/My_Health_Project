'use strict';

//Listens for search button to find physician.
const findPhysicianButton = document.querySelector("#search_result");
findPhysicianButton.addEventListener('click', () => {

    //Get zipcode user entered.
    let zipcode = document.querySelector('#zipcode');
    zipcode = zipcode.value;

    //Check if zipcode entered is 5 digits.
    const regexZipcode = /\d{5}/;
    if (zipcode.length === 5 && regexZipcode.test(zipcode)) {

        const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${zipcode}&key=${key}`;

        //Make request to Google Geocode API to get latitude/longitude from zipcode
        fetch(url)
            .then(response => response.json())
            .then(responseDATA => {
                const latitude = responseDATA.results[0].geometry.location.lat;
                console.log("Latitude:", latitude);
            
                const longitude = responseDATA.results[0].geometry.location.lng;
                console.log("Longitude:", longitude);
                
                const latLongResult = {'latitude': latitude, 'longitude': longitude}
            })

            .catch(error => {
                console.error("Error:", error);
            })
            
    } else {
        flash("Please enter a valid 5-digit zipcode.");
    }

});

                if (latLongResult) {
                    //Get results of doctors nearby location
                    function findNearbyDoctors(latLongResult, API_KEY, pageToken = null)

                        const latitude = str(latLongResult.latitude);
                        const longitude = str(latLongResult.longitude);

                        const dataType = "doctor"
                        const radius = 16000
                        const location = `${latitude},${longitude}`
                        const pageToken = "next_page_token" 

                        let allResults = []

                        const url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${location}&type=${dataType}&radius=${radius}&key=${API_KEY}&pageToken=${pageToken}`

                        


                

                    //Append data to all_results list
                    all_results.extend(data['results'])

                    //Check to see if there is more results
                    more_data = data.get('next_page_token')

                        if (more_data) {

                            time.sleep(2)
                            data_2 = crud.find_nearby_doctors(location, API_KEY, page_token=more_data)
                            pprint(data_2)

                            all_results.extend(data_2['results'])
                        }
                        
}


  
def find_nearby_doctors(location, API_KEY, page_token=None):
    """Returns nearby doctors that match location."""
    
  
   
    params = {
            "location": location,
            "type": data_type,
            "radius": radius,
            "key": API_KEY,
            "pageToken": "next_page_token"      
        }
    
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    res = requests.get(url, params=params)

    if res.status_code == 200:
        nearby_data = res.json()
        print(nearby_data)

        return nearby_data
    
    else:
        return "Error, data request unsuccessful."
    



    



