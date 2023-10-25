'use strict';


//Listens for submit vitals button clicked on vitals page
const addVital = document.querySelector('button.submit-vitals'); 
addVital.addEventListener('click', addVitals);


function addVitals(evt) {
    evt.preventDefault();

    //Get values entered by user
    const systolic = document.querySelector('#systolic').value;
    const diastolic = document.querySelector('#diastolic').value;
    const heartRate = document.querySelector('#heart_rate').value;
    const oxygen = document.querySelector('#oxygen').value;
    const weight = document.querySelector('#weight').value;
    const glucose = document.querySelector('#glucose').value;
    
    //values entered into dictionary to send in fetch request
    const data = {
        systolic: systolic,
        diastolic: diastolic,
        heartRate: heartRate,
        oxygen: oxygen,
        weight: weight,
        glucose: glucose        
    }

    fetch('/vitals/results', {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            window.location.pathname = ('/vitals/allrecords');
        })

}

