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
            window.location.reload(true);
        });
        
}





//Listens for button clicked to delete comments to user condition.
const deleteCommentButtons = document.querySelectorAll('button.delete-selected');

deleteCommentButtons.forEach(button => {
    button.addEventListener('click', deleteComments);
});

function deleteComments(evt) {
    console.log('Delete selected clicked');
    evt.preventDefault();
}


for (const deleteCommentButton of deleteCommentButtons) {
    deleteCommentButton.addEventListener('click', deleteComments);
} 


function deleteComments(evt) {
    evt.preventDefault();

    const parent = evt.target.parentElement
    console.log(parent);
    const checkedBoxes = parent.querySelectorAll('input.delete-comment:checked');
    console.log(checkedBoxes);

    let commentIds = []
    for (let box of checkedBoxes) {
        box = box.value;
        commentIds.push(box);
    }
        
    const comments = {
        comment_ids : commentIds,
    }
       
    fetch('/deletecomments', {
        method: "POST",
        body: JSON.stringify(comments),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            window.location.reload(true);
            
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
        favorite_id : evt.target.id,
    }
    fetch('/deleteusercondition', {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responseJSON) => {
            window.location.reload(true);
           
        })

    }



