'use strict';

//Listens for button clicked to add comments to user condition.
const commentButtons = document.querySelectorAll('button.comments-submit');
for (const commentButton of commentButtons) {
    commentButton.addEventListener('click', addComments);
} 

function addComments(evt) {
    evt.preventDefault();

    const parent = evt.target.parentElement
    
    let formInput = parent.querySelector('#comments-box');
        formInput = formInput.value;
        
    const comments = {
        favorite_id : evt.target.id,
        comment : formInput,
    }
       
    fetch('/addcomments', {
        method: "POST",
        body: JSON.stringify(comments),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            // const userComment = parent.querySelector('#user_comments')
            // userComment.insertAdjacentHTML('beforeend',`<li>${formInput}</li>`)
            window.location.pathname = ('/profile/saved')
        });
        
}