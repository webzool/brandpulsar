// Ponounce domain name

var txtInput = document.querySelector('#txtInput');
var voiceList = document.querySelector('#voiceList');
var btnSpeak = document.querySelector('#btnSpeak');
var synth = window.speechSynthesis;
var voices = [];

PopulateVoices();
if (speechSynthesis !== undefined) {
    speechSynthesis.onvoiceschanged = PopulateVoices;
}

btnSpeak.addEventListener('click', () => {
    var toSpeak = new SpeechSynthesisUtterance(txtInput.textContent);
    var selectedVoiceName = 'Google US English';
    // var selectedVoiceName = voiceList.selectedOptions[0].getAttribute('data-name');
    voices.forEach((voice) => {
        if (voice.name === selectedVoiceName) {
            toSpeak.voice = voice;
        }
    });
    synth.speak(toSpeak);
});

function PopulateVoices() {
    voices = synth.getVoices();
    var selectedIndex = voiceList.selectedIndex < 0 ? 0 : voiceList.selectedIndex;
    voiceList.innerHTML = '';
    voices.forEach((voice) => {
        var listItem = document.createElement('option');
        listItem.textContent = voice.name;
        listItem.setAttribute('data-lang', voice.lang);
        listItem.setAttribute('data-name', voice.name);
        voiceList.appendChild(listItem);
    });

    voiceList.selectedIndex = selectedIndex;
}

// FAVORITE


function saveFavourites(favorites) {
    window.localStorage.setItem('cosmic-favs', JSON.stringify(favorites));
}

function displayFavourites() {
    let favorites = loadFavourites();
    $('.toggle-fav').each(function () {
        let id = $(this).data('favorite_id');

        if (-1 === favorites.indexOf(id)) {

            $(this).removeClass('set');
        } else {

            $(this).addClass('set');
        }
    });
    if (favorites.length) {
        // We only have room for 2 digits
        let num = favorites.length;
        if (num > 99) {
            num = "";
        }

        $('.fav-link #fav-count').remove();
        let counter = '<span id="fav-count">' + num + '</span>';
        $('.fav-link').show();
        $('.fav-link a').append(counter);
        $('.fav-link-mobile').show();
    } else {
        $('.fav-link').hide();
        $('.fav-link-mobile').hide();
    }
}

function bindFavouriteButtons() {

    $(document).on('click', '.toggle-fav', function () {
        toggleFavourite($(this).data('id'));
        return false;
    });

}

// function loadAndRenderFavourites() {
//     let favorites = loadFavourites();
//     $('#favs-content').load(
//         window.getPath + "?favorites=" + JSON.stringify(favorites)
//     );
// }
$(function () {
    bindFavouriteButtons();
    displayFavourites();
});

function toggleFavourite(favorite_id) {
    let favorites = loadFavourites();
    let index = favorites.indexOf(favorite_id);
    const btnLike = $('#like-btn').attr('src');
    const favoriteEndpoint = `${location.origin}/ajax-favorite`;
    let data = {};
    const liked = `${window.origin}/static/images/like.svg`;
    const not_liked = `${window.origin}/static/images/like-2.svg`;
    if (btnLike === liked) {
        $('#like-btn').attr('src', not_liked);
    } else {
        $('#like-btn').attr('src', liked);
    };
    if (-1 === index) {
        favorites.push(favorite_id);
        data = {
            'domain_id': favorite_id,
            'action': 'add'
        }
        $.ajax({
            data: data,
            url: favoriteEndpoint,
            method: "POST",
            async: false,
            success: function (data) {
                var successMsg = data.message;
            },
            error: function (error) {
                console.log(error);
            }
        })
        saveFavourites(favorites);
        getFavoriteCount(favorite_id);
        displayFavourites();

    } else {

        data = {
            'domain_id': favorite_id,
            'action': 'remove'
        }
        $.ajax({
            data: data,
            url: `${location.origin}/ajax-favorite`,
            async: false,
            method: "POST",
            success: function (data) {
                var successMsg = data.message;
            },
            error: function (error) {
                console.log(error);
            }
        })
        favorites.splice(index, 1);
        saveFavourites(favorites);
        getFavoriteCount(favorite_id)

        // if ($('body').hasClass('favorites')) {
        //     $('#domain-' + favorite_id).fadeOut(200);
        //     loadAndRenderFavourites();
        // } else {
        //     displayFavourites();
        // }
    }
    return false;
}

function loadFavourites() {
    let favorites = window.localStorage.getItem('cosmic-favs');
    if (!favorites) {
        return [];
    }

    return JSON.parse(favorites).map(function (favorite) {
        return favorite
    });
}

function getFavouriteStatus(domain_id) {
    let favorites = window.localStorage.getItem('cosmic-favs');
    if (favorites == null) {
        return `${window.origin}/static/images/like-2.svg`;
    } else if (favorites.includes(domain_id)) {
        return `${window.origin}/static/images/like.svg`;
    }

    // return `${window.origin}/static/images/like-2.svg`;
};

function getFavoriteCount(favorite_id) {
    let domain;
    $.ajax({
        url: `${location.origin}/ajax-favorite`,
        type: "GET",
        datatype: "json",
        async: false,
        data: {
            'domain': favorite_id
        },
        success: function (data) {
            domain = data.domain;
            $('.fav-count').text(domain);
        }
    });

    return domain;
};

function favoriteBox() {
    const domain_id = $('#like').attr('data-id');

    return `
    <img id="like-btn" src="${getFavouriteStatus(domain_id)}" />
    <span class="fav-count">${getFavoriteCount(domain_id)}</span>
    <span>Likes</span>
    `
}

$(document).ready(() => {
    const like_container = $('#like');
    let box = favoriteBox();
    $(box).appendTo(like_container);

});


// Payment options

$("input[name='portion_selection']:radio")
    .change(function () {
        $("#portion_one").toggle($(this).val() == "button_one");
        $("#portion_two").toggle($(this).val() == "button_two");
        $("#portion_three").toggle($(this).val() == "button_three");
    });

function showPaymentOptions(checkedObj) {

    let buyNowBtn = document.getElementById("buy-now");
    let buyInstalmentsBtn = document.getElementById("buy-instalments");
    let buyBankWireBtn = document.getElementById("buy-bank-wire");
    let payment = document.querySelectorAll('input[name=payment]:checked');

    var checked = checkedObj;

    if (checked.hasAttribute("checked")) {
        checked.removeAttribute("checked");
    } else {
        checked.setAttribute("checked", "checked");
    }
}
$('#copy').click(function () {
    var url = window.location.href;
    var text = $('#page-url');
    var copyText = "";
    copyText = text.val(url);
    copyText.focus();
    copyText.select();
    document.execCommand("copy");
    $("#copy span").text("Copied!")
});

function copyURL() {
    var input = document.getElementById("page-url");
    var url = window.location.href;
    input.val(url)
}

// Stripe

const pub_key = $("#buy-button").attr("stripe");
const stripe = Stripe(pub_key);
const stripe_one_time_id = $("#buy-button").attr("one-time-id");
let paymentType = '';
const productImg = $('.product-img').attr("src");
const productName = $('#txtInput').text();
const productPrice = $('#one-time-price').text();
const productDescription = $('.domain-description').text();
const buyButton = document.getElementById("buy-button");
buyButton.addEventListener("click", function (event) {
    paymentType = 'onetime'
    createCheckoutSession(stripe_one_time_id, paymentType)
        .then(function (session) {
            return stripe.redirectToCheckout({
                sessionId: session.id
            });
        })
        .then(function (result) {
            if (result.error) {
                alert(result.error.message);
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
});

var createCheckoutSession = function (priceId, paymentType) {
    return fetch("/create-checkout-session/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            priceId: priceId,
            paymentType: paymentType,
            product_image: productImg,
            product_name: productName,
            product_price: productPrice,
            product_description: productDescription
        })
    }).then(function (result) {
        return result.json();
    });
};

var handleResult = function (result) {
    if (result.error) {
        var displayError = document.getElementById("error-message");
        displayError.textContent = result.error.message;
    }
};

const planBtns = document.querySelectorAll('#plan');
Array.from(planBtns, planBtn =>
    planBtn.addEventListener('click', function () {

        let plan_id = $(this).attr('plan-id');

        paymentType = 'instalment'

        createCheckoutSession(plan_id, paymentType).then(function (data) {
            stripe
                .redirectToCheckout({
                    sessionId: data.id
                })
                .then(handleResult);
        });
    })
);