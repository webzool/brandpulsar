$(document).ready(() => {
    let items = localStorage.getItem('cosmic-favs');
    console.log('items', items)
    if (items) {
        items = JSON.parse(items);
        if (items.length > 0) {
            getFavourites(items);
            console.log(' ITEMS Domains ', items)
        }
    } else {
        let emptyMessage = "You don't have favorite domains.";
        $('#empty-message').html(emptyMessage);
    }
});

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

function loadAndRenderFavourites() {
    let favorites = loadFavourites();
    $('#favs-content').load(
        window.getPath + "?favorites=" + JSON.stringify(favorites)
    );
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

        $('#domain-' + favorite_id).fadeOut(200);
        let favorites_s = window.localStorage.getItem('cosmic-favs');
        getFavourites(favorites_s);


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

// function saveFavourites(domain) {
//     const url = `http://${location.host}/v1/api/favourite/favourite/?d=${domain}`;
//     fetch(url)
//         .then(response => response.json())
//         .then((data) => {
//             console.log(data);
//         });
// }

function saveFavourites(favorites) {
    window.localStorage.setItem('cosmic-favs', JSON.stringify(favorites));
}


// function addFavourites() {
//     const id = $(event.currentTarget).attr('data-domain-id');
//     saveFavourites(id);
//     let stored_data = localStorage.getItem('cosmic-favs');
//     if (stored_data) {
//         stored_data = JSON.parse(stored_data);
//         let existed = stored_data.domains.filter(item => item === id);
//         if (existed.length > 0) {
//             stored_data.domains = removeFromArray(value = id, arr = stored_data.domains);
//         } else {
//             stored_data.domains.push(id);
//         }
//         stored_data.domains = Array.from(new Set(stored_data.domains));
//         localStorage.setItem('cosmic-favs', JSON.stringify(stored_data));
//         localStorage.setItem('fav_count', stored_data.domains.length);

//         if (stored_data.domains.length == 0) {
//             localStorage.removeItem('fav_count');
//             $('#fav-nav-item').addClass('d-none');
//         }
//     } else {
//         let data = {
//             'domains': [id, ]
//         }
//         localStorage.setItem('cosmic-favs', JSON.stringify(data));
//         localStorage.setItem('fav_count', data.domains.length);
//     }
//     updateFavouriteStatus(event.currentTarget);
//     getFavCount();
// };

function prepareDomain(domain) {
    return `
        <div class="col-md-3 col-sm-6 col-xs-6 col-6" id="domain-${domain['id']}">
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
                        <p><span class="purple">$</span> ${domain['price']}</p>
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

function getFavourites(ids) {
    let default_url = `${location.origin}/v1/api/domains/?`;
    const container = $('#domainRow');
    for (let item in ids) {
        default_url += `ids=${ids[item]}&`;
    }
    $.get(default_url, (data) => {
        for (let domain in data.results) {
            console.log("FAV domains", data.results.length);
            let domain_node = prepareDomain(data.results[domain]);
            $(domain_node).appendTo(container);
        }
    });
}

function updateFavouriteStatus(item) {
    const btnLike = $(item).find('#like-btn').attr('src');

    const liked = `${window.origin}/static/images/like.svg`;
    const not_liked = `${window.origin}/static/images/like-2.svg`;

    if (btnLike === liked) {
        $(event.currentTarget).find('#like-btn').attr('src', not_liked);
    } else {
        $(event.currentTarget).find('#like-btn').attr('src', liked);
    };

};

function getFavouriteStatus(id) {
    let favorites = window.localStorage.getItem('cosmic-favs');

    if (favorites.includes(id)) {
        return `${window.origin}/static/images/like.svg`;
    } else {
        return `${window.origin}/static/images/like-2.svg`;
    }

    return `${window.origin}/static/images/like-2.svg`;
};

function removeFromArray(value, arr) {
    arr = arr.filter(item => item !== value);
    return arr;
};