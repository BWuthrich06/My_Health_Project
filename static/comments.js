'use strict';

const commentButtons = document.querySelectorAll('button.comments-submit');
for (const commentButton of commentButtons) {
    commentButton.addEventListener('click', addComments);
} 

function addComments(evt) {
    evt.preventDefault();

    let formInput = document.querySelector('#comments-box');

    formInput = formInput.value;

    // const comments = {
    //     comment : evt.target.id
    // }

    fetch('/addcomments', {
        method: "POST",
        body: JSON.stringify(formInput),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            responseJSON.insertAdjacentHTML('beforeend', '<li>Comment goes here</li>')
        })
        
}