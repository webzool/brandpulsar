// If not url described, main function gets default_url
let default_url;

if (industry_id) {
    // Also handles single industry domains. If page defined industy_id variable
    // all endpoints will start with industry id query parameter
    default_url = `${location.origin}/v1/api/domains/?industry=${industry_id}&`;
} else {
    default_url = `${location.origin}/v1/api/domains/`;
};

// Filtering for mobile
var mobileFilter = document.getElementById('mobileFilter');
var desktopFilter = document.getElementById('desktopFilter');
if ($(window).width() < 922) {
    desktopFilter.remove()
} else {
    mobileFilter.remove()
}

$(document).ready(() => {
    // Gets data on page load
    if (localStorage.getItem('related_domain_ids')) {
        let url = `${location.origin}/v1/api/domains/?`;
        const domains = JSON.parse(localStorage.getItem('related_domain_ids'));
        domains.forEach(pk => url += `ids=${pk}&`);
        main(url, currentPage = 1, key = "Related domains");
        localStorage.removeItem('related_domain_ids');
    } else if (localStorage.getItem('autocomplete')) {
        const data = JSON.parse(localStorage.getItem('autocomplete'));
        main(redirectAutocomplete(default_url), currentPage = 1, key = data.name);
    } else {
        main();
    }

    // Sorting options
    $('#sort-filter').on('change', () => {
        let q = $(event.currentTarget).val();
        let sorting_url = `${default_url}?sort=${q}`;
        main(url = sorting_url);
    });


    $('#id_name').keypress(function (e) {
        if (e.which == 13) {
            filterOnEnter(container = $('#id_name').val());
        }
    });

    $('#id_tags').keypress(function (e) {
        if (e.which == 13) {
            filterOnEnter(container = $('#id_tags').val());
        }
    });

    $('#id_length_gt').keypress(function (e) {
        if (e.which == 13) {
            filterOnEnter(container = $('#id_length_gt').val());
        }
    });

    $('#id_length_lt').keypress(function (e) {
        if (e.which == 13) {
            filterOnEnter(container = $('#id_length_lt').val());
        }
    });

    $('#id_price_gt').keypress(function (e) {
        if (e.which == 13) {
            filterOnEnter(container = $('#id_price_gt').val());
        }
    });

    $('#id_price_lt').keypress(function (e) {
        if (e.which == 13) {
            filterOnEnter(container = $('#id_price_lt').val());
        }
    });

    // Filtering
    $('.filter-btn').on('click', () => {
        const filter_url = filtering(default_url);
        let kw = '';
        const kw_dict = {
            contains: $('#id_name').val(),
            tags: $('#id_tags').val(),
        }
        for (let item in kw_dict) {
            if (kw_dict[item]) {
                kw = kw_dict[item];
            }
        }
        main(url = filter_url, currentPage = 1, key = kw, contains = kw_dict.contains);
        $("html").animate({
            scrollTop: 0
        }, "slow");
    });

});

function main(url = default_url, currentPage = 1, key, contains) {
    const container = $('#domainRow');
    const info_box = $('#list-info');
    container.empty();
    info_box.empty();
    //clearFilterValues();

    localStorage.setItem('endpoint', url);
    // FETCH : gets domain list
    fetch(url)
        .then(response => response.json())
        .then(data => getData(data));

    function getData(data) {
        for (let domain in data.results) {
            let item = prepareDomain(data.results[domain]);
            $(item).appendTo(container);
        };
        if (industry_id) {
            $(prepareInfoBox(count = data['count'], keyword = key, contains_keyword = contains, industry = industry_name)).appendTo(info_box);
        } else {
            $(prepareInfoBox(count = data['count'], keyword = key, contains_keyword = contains)).appendTo(info_box);
        }
        pagination(data.max_page, currentPage);
    };
}

function filterOnEnter(container) {
    const filter_url = filtering(default_url);
    main(url = filter_url, currentPage = 1, key = container);
    $("html").animate({
        scrollTop: 0
    }, "slow");
    return false;
}

function domainPrice(domain) {
    let priceBox = '';

    if (domain['discount_price']) {
        priceBox = `<p><span class="purple">$</span> ${domain['discount_price']} <div><div class="line"></div><span>$</span> ${domain['price']}</div></p>`;
    } else {
        priceBox = `<p><span class="purple">$</span> ${domain['price']}</p>`;
    }
    return priceBox
}


function removeFromArray(value, arr) {
    arr = arr.filter(item => item !== value);
    return arr;
};

function prepareDomain(domain) {
    return `
        <div class="col-md-3 col-sm-6 col-xs-6 ${checkDomainBox()} col-6">
            <article class='domain position-relative'>
                <a href="${domain['url']}">
                    <div class='domain-image-container'>
                        <img src="${domain['thumbnail_image']}"
                            alt="${domain['full_name']}" class='domain-image' />
                    </div>
                </a>
                <div class='hit-info-container'>
                    <a href="${domain['url']}">
                        <h5>${domain['full_name']}</h5>
                    </a>
                    <div class="domain-footer">
                        ${domainPrice(domain)}
                        <div class="followediv">
                            <a class="toggle-fav toggle-fav-thumbnail-icon" data-id="${domain['id']}" id="domain-${domain['id']}" href="#">
                                <img id="like-btn" src="${getFavouriteStatus(domain['id'])}" />
                            </a>
                        </div>
                    </div>
                </div>
            </article>
        </div>`
};

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

    $(document).on('click', '.toggle-fav', function (e) {
        e.preventDefault();
        toggleFavourite($(this).data('id'));

        return false;
    });

}


$(function () {
    bindFavouriteButtons();
    displayFavourites();
});

function toggleFavourite(favorite_id) {

    let favorites = loadFavourites();
    let fav_domain_id = `domain-${favorite_id}`
    let domain = document.getElementById(fav_domain_id);
    let index = favorites.indexOf(favorite_id);
    const btnLike = $(domain).find('#like-btn').attr('src');
    const favoriteEndpoint = `${location.origin}/ajax-favorite`;
    let data = {};
    const liked = `${window.origin}/static/images/like.svg`;
    const not_liked = `${window.origin}/static/images/like-2.svg`;

    if (btnLike === liked) {
        $(domain).find('#like-btn').attr('src', not_liked);
    } else {
        $(domain).find('#like-btn').attr('src', liked);
    };

    if (-1 === index) {
        favorites.push(favorite_id);

        $(this).removeClass('set');
        data = {
            'domain_id': favorite_id,
            'action': 'add'
        }
        $.ajax({
            data: data,
            url: favoriteEndpoint,
            method: "POST",
            success: function (data) {
                var successMsg = data.message;
                console.log('Success', successMsg)
            },
            error: function (error) {
                console.log(error);
            }
        })



        saveFavourites(favorites);
        displayFavourites();

    } else {

        $(this).addClass('set');


        data = {
            'domain_id': favorite_id,
            'action': 'remove'
        }
        $.ajax({
            data: data,
            url: favoriteEndpoint,
            method: "POST",
            success: function (data) {
                var successMsg = data.message;
                console.log('Success', successMsg)
            },
            error: function (error) {
                console.log(error);
            }
        })
        favorites.splice(index, 1);
        saveFavourites(favorites);

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

function getFavouriteStatus(id) {
    let favorites = loadFavourites();

    if (favorites.includes(id)) {
        return `${window.origin}/static/images/like.svg`;
    } else {
        return `${window.origin}/static/images/like-2.svg`;
    }
};

function checkDomainBox() {
    let domainClass = '';

    if ($(window).width() > 1900) {
        domainClass = 'col-xl-2';
    } else {
        domainClass = '';
    }

    return domainClass
}

function pagination(count, currentPage) {
    const pagination_container = $('.pagination');
    pagination_container.empty();
    let navs = `
    <li class="page-before page-item">
        <a class="page-link" onclick="getPage(${currentPage - 1})">«</a>
    </li>
    <li class="page-next page-item">
        <a class="page-link" onclick="getPage(${currentPage + 1})">»</a>
    </li>`;

    $(navs).appendTo(pagination_container);

    for (let i = 1; i < count + 1; i++) {
        let active = '';
        if (i === parseInt(currentPage)) {
            active = 'active';
        }
        let page = `<li class="page-item ${active}"><a class="page-link"
            onclick="getPage(${i})">${i}</a></li>`
        $(page).appendTo(pagination_container).insertBefore('.page-next');
    }
}

function getPage(page) {
    let offset = '';
    if (page) {
        offset = (page - 1) * 20;
    }
    let url = localStorage.getItem('endpoint');
    let next_url = `${url}?offset=${parseInt(offset)}`;
    if (url.includes('?')) {
        next_url = `${url}&offset=${parseInt(offset)}`;
    }
    $("html").animate({
        scrollTop: 0
    }, "slow");
    return main(next_url, page);
}

function getFilterValues() {
    return {
        min_price: $('#id_price_gt').val(),
        max_price: $('#id_price_lt').val(),
        min_length: $('#id_length_gt').val(),
        max_length: $('#id_length_lt').val(),
        contains: $('#id_name').val(),
        syllable: $('#id_syllable').val(),
        tags: $('#id_tags').val(),
    }
}

function filtering(url) {
    let path = '';
    const lookup_query = getFilterValues();
    Object.keys(lookup_query).forEach(function (key) {
        // If filter value has multiple choices, we should
        // append multiple same keys for each value.
        const is_array = Array.isArray(lookup_query[key]);

        if (lookup_query[key]) {
            if (is_array) {
                lookup_query[key].forEach(item => path += `${key}=${item}&`);
            } else {
                path += `${key}=${lookup_query[key]}&`;
            }
        }
    });
    return `${url}?${path}`;
}

function redirectAutocomplete(url) {
    path = '';
    let autocomplete = localStorage.getItem('autocomplete');
    autocomplete = JSON.parse(autocomplete);
    path += `${autocomplete.type}=${autocomplete.name}&`;
    localStorage.removeItem('autocomplete');
    return `${url}?${path}`;
};

function prepareInfoBox(count, keyword, industry, contains_keyword) {
    let result;

    let domain = 'domains';
    if (parseInt(count) <= 1) {
        domain = 'domain';
    }
    if (industry) {
        result = `<span>Listing ${count} ${domain} for ${industry}.</span>`;
    } else {
        result = `<span>Listing ${count} ${domain}.</span>`;
    }

    if (keyword) {

        let tag_array = []
        for (let item in keyword) {
            let selectedTag = document.getElementById(keyword[item]);
            let k = selectedTag.textContent;
            tag_array.push(k)
        }
        result = `
        <span>Listing ${count} ${domain} for ${tag_array}</span>.
        <div class="clear-btn btn-green btn-sm" onclick="main()">
           <img src="${window.origin}/static/images/refresh.svg" />
        Clear</div>`;
    }
    return result;
}