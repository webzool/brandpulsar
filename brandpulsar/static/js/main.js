if (localStorage.getItem('cookieSeen') != 'shown') {
    $(".cookie-banner").delay(2000).fadeIn();
    localStorage.setItem('cookieSeen', 'shown')
}

$('.cookie-close').click(function (e) {
    $('.cookie-banner').fadeOut();
});

$(document).ready(() => {

    $('#search').on('keyup', () => {
        $('#search-results').empty();
        let value = $(event.currentTarget).val();
        let url = `${location.origin}/v1/api/autocomplete/?q=${value}`;
        $.get(url, function (data) {
            if (data.length > 0) {
                for (let item in data) {
                    let list_item = prepareResults(data[item]);
                    $(list_item).appendTo($('#search-results'));
                }
            } else {
                brainStormingAPI.fetchAll(value); // Fetching related words;
                const list_of_domains = new Array();
                setTimeout(() => {
                    brainStormingAPI.fetchCosmicDomains(word = value, industry = null, limit = 5);
                    setTimeout(() => {
                        $('#search-results').empty();
                        const domains = brainStormingAPI.cosmic_domains;
                        domains.forEach(item => list_of_domains.push(item.id));
                        localStorage.setItem("related_domain_ids", JSON.stringify(list_of_domains));
                    }, 1000);

                }, 1000);
            };
        });
    });

    $('#search').keypress(function (e) {
        var key = e.which;
        if (key == 13) {
            setTimeout(() => {
                window.location.href = '/domains/'
            }, 2000);
        }
    });

    getFavCount();

    //Get current time
    var currentTime = new Date().getTime();
    //Add hours function
    Date.prototype.addHours = function (h) {
        this.setTime(this.getTime() + (h * 60 * 60 * 1000));
        return this;
    }
    //Get time after 24 hours
    var after24 = new Date().addHours(10).getTime();
    //Hide notification click
    $('.close').click(function () {
        //Hide notification
        $('.notification').hide();
        //Set desired time till you want to hide notification
        localStorage.setItem('desiredTime', after24);
    });
    //If desired time >= currentTime, based on that HIDE / SHOW
    if (localStorage.getItem('desiredTime') >= currentTime) {
        $('.notification').hide();
    } else {
        $('.notification').show();
    }
});

function prepareResults(data) {
    let redirect_url = `${location.origin}/domains/`;
    if (data.url) {
        redirect_url = data.url;
    }
    return `<li class="autocomplete-item" onclick="storeType()">
        <a class="text-decoration-none" href="${redirect_url}">
        <p>${data.name}</p> <span>${data.type}</span></a>
    </li>`;
}

function storeType() {
    let type = $(event.currentTarget).find('span').text();
    let name = $(event.currentTarget).find('p').text();
    const dict = {
        'type': type,
        'name': name,
    }
    localStorage.setItem('autocomplete', JSON.stringify(dict));
}

function getFavCount() {
    let count = localStorage.getItem('fav_count');
    if (count) {
        $('#fav-nav-item').removeClass('d-none');
        $('#fav-count').text(count);
    } else {
        $('#fav-count').text('0');
    }
};