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
            const userComment = parent.querySelector('#user_comments')
            userComment.insertAdjacentHTML('beforeend',`<li>${formInput}</li>`)
        });
        
}


//Listens for button clicked to delete comments to user condition.
const deleteCommentButtons = document.querySelectorAll('button.delete-comment');
for (const deleteCommentButton of deleteCommentButtons) {
    deleteCommentButton.addEventListener('click', deleteComments);
} 

function deleteComments(evt) {
    evt.preventDefault();

    const parent = evt.target.parentElement
    console.log(parent);
        
    const comment = {
        comment_id : evt.target.id,
    }
       
    fetch('/deletecomments', {
        method: "POST",
        body: JSON.stringify(comment),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            
            
        });
        
}



//Listens for delete condition button clicked in users saved conditions.
const deleteConditionButtons = document.querySelectorAll('button.delete-condition');
for (const deleteConditionButton of deleteConditionButtons) {
    deleteConditionButton.addEventListener('click', deleteCondition);
} 


function deleteCondition(evt) {
    evt.preventDefault();

    const data = {
        condition_id : evt.target.id,
    }
    fetch('/deletecondition', {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
           
        })

    }



