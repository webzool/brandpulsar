// Default form data url
const negotiate_url = `${location.origin}/v1/api/negotiate/`;

// Initialize form data
function initializeNegotiationFormData(data) {
    let negotiation_form = new FormData();
    negotiation_form.append('domain', data.domain);
    negotiation_form.append('email', data.email);
    negotiation_form.append('first_name', data.first_name);
    negotiation_form.append('last_name', data.last_name);
    negotiation_form.append('phone', data.phone);
    negotiation_form.append('price', data.price);
    negotiation_form.append('message', data.message);
    console.log(data.message);
    return negotiation_form;
};

function getNegotiationFormData() {
    const data = {
        domain: $('#n_domain').val(),
        email: $('#n_email').val(),
        first_name: $('#n_first_name').val(),
        last_name: $('#n_last_name').val(),
        phone: $('#n_phone').val(),
        price: $('#n_price').val(),
        message: $('#n_message').val(),
    }
    console.log(data);
    return initializeNegotiationFormData(data);
};

function sendNegotiateForm() {
    let csrftoken = getCookie('csrftoken');
    fetch(negotiate_url, {
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: getNegotiationFormData(),
            method: "POST"
        })
        .then((response) => {
            handleResult(response.status)
        })
};

function handleResult(status) {
    if (status === 201) {
        $('.modal-title').hide();
        $('#negotiation-form').hide();
        $('#thanks-negotiation').show();
        window.location.replace(`${location.origin}/thank-you/`);
    } else {
        const msg = `<p class="color-red pt-2">There was an error. Please try again</p>`;
        $(msg).appendTo('.negotiation-form-body');
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
    $("#thanks-negotiation").hide();

    $('#submit_negotiation').on('click', () => {
        sendNegotiateForm();
    });
    $('.wrong-icon').on('click', () => {
        $('.modal-layer').hide();
    });
});