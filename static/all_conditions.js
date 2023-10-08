'use strict';


//Listens for add condition button clicked on search result page
const addAllButtons = document.querySelectorAll('button.all_condition_add');
for (const addButton of addAllButtons) {
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
            window.location.pathname = ('/profile/saved')
        })

}

