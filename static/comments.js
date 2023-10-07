'use strict';

const commentButtons = document.querySelectorAll('button.comments-submit');
for (const commentButton of commentButtons) {
    commentButton.addEventListener('click', addComments);
} 

function addComments(evt) {
    evt.preventDefault();

    console.log(evt.target.id);
    const parent = evt.target.parentElement
    

    let formInput = parent.querySelector('#comments-box');
        formInput = formInput.value;
        console.log(formInput);
        
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
            console.log(responseJSON)
            const userComment = parent.querySelector('#user_comments')
            console.log(userComment)
            console.log(parent)
            userComment.insertAdjacentHTML('beforeend',`<li>${formInput}</li>`)
        });
        
}