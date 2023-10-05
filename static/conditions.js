'use strict';


//Show search results
// function showResults(evt) {
//     evt.preventDefault();

//     const searchResults = document.querySelector('#').value;

//     fetch(`/conditions/results?result=${searchResults}`)
//         .then((response) => response.json())
//         .then((responseJSON) => {
//             const results = document.querySelector('#')
//             results.innerHTML = responseJSON})
// }

// const searchButton = document.querySelector('#search_result');
// searchButton.addEventListener('click', showResults);



const addButtons = document.querySelectorAll('button.condition_add');
for (const addButton of addButtons) {
    addButton.addEventListener('click', addCondition);
} 

function addCondition(evt) {
    const data = {
        condition : evt.target.id,
    }
    fetch('/addcondition', {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            alert(responseJSON.message);
            window.location.pathname = ('/profile/saved')
        })





}

