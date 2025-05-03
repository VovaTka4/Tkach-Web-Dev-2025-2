'use strict';

function modalShown(event) {
    let button = event.relatedTarget;
    let newUrl =  button.dataset.deleteUrl;
    form.action = newUrl;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);
