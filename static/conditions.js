'use strict';


//Show search results
function showResults(evt) {
    evt.preventDefault();

    const searchResults = document.querySelector('#').value;

fetch(`/conditions/results?result=${searchResults}`)
    .then((response) => response.json())
    .then((responseJSON) => {
        const results = document.querySelector('#')
        results.innerHTML = responseJSON})
}

const searchButton = document.querySelector('#search_result');
searchButton.addEventListener('click', showResults);