// Default form data url
const form_url = `${location.origin}/v1/api/contacts/`;

// Initialize form data
function initializeFormData(data) {
    let formData = new FormData();
    formData.append('domain', data.domain);
    formData.append('email', data.email);
    formData.append('name', data.name);
    formData.append('surname', data.surname);
    formData.append('message', data.message);
    return formData;
};

function getFormData() {
    const data = {
        domain: $('#domain-id').val(),
        email: $('#email-id').val(),
        name: $('#name-id').val(),
        surname: $('#surname-id').val(),
        message: $('#message-id').val(),
    }
    return initializeFormData(data);
};

function sendForm() {
    let csrftoken = getCookie('csrftoken');
    fetch(form_url,
        {
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: getFormData(),
            method: "POST"
        })
        .then((response) => { handleResult(response.status) })
};

function handleResult(status) {
    if (status === 201) {
        $('#form-context').hide();
        $('#thanks').show();
    } else {
        const msg = `<p class="color-red pt-2">There was an error. Please try again</p>`;
        $(msg).appendTo('#form-context');
    }
}

//Cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(() => {
    $(".modal-layer").hide();
    $('#contact-owner').on('click', () => {
        $('.modal-layer').show();
    });
    $('#contact-btn').on('click', () => {
        sendForm();
    });
    $('.wrong-icon').on('click', () => {
        $('.modal-layer').hide();
    });
    $("body").on('click', (e) => {
        if (e.target.childNodes[1] === document.querySelector('.form-modal')) {
            $(".modal-layer").hide();
        };
    });
});