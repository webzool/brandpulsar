"use strict";

$(document).ready(function () {
  var items = localStorage.getItem('favourites');

  if (items) {
    items = JSON.parse(items);

    if (items.domains.length > 0) {
      getFavourites(items.domains);
    }
  }
});

function saveFavourites(domain) {
  var url = "http://".concat(location.host, "/v1/api/favourite/favourite/?d=").concat(domain);
  fetch(url).then(function (response) {
    return response.json();
  }).then(function (data) {
    console.log(data);
  });
}

function addFavourites() {
  var id = $(event.currentTarget).attr('data-domain-id');
  saveFavourites(id);
  var stored_data = localStorage.getItem('favourites');

  if (stored_data) {
    stored_data = JSON.parse(stored_data);
    var existed = stored_data.domains.filter(function (item) {
      return item === id;
    });

    if (existed.length > 0) {
      stored_data.domains = removeFromArray(value = id, arr = stored_data.domains);
    } else {
      stored_data.domains.push(id);
    }

    stored_data.domains = Array.from(new Set(stored_data.domains));
    localStorage.setItem('favourites', JSON.stringify(stored_data));
    localStorage.setItem('fav_count', stored_data.domains.length);

    if (stored_data.domains.length == 0) {
      localStorage.removeItem('fav_count');
      $('#fav-nav-item').addClass('d-none');
    }
  } else {
    var data = {
      'domains': [id]
    };
    localStorage.setItem('favourites', JSON.stringify(data));
    localStorage.setItem('fav_count', data.domains.length);
  }

  updateFavouriteStatus(event.currentTarget);
  getFavCount();
}

; // Helper functions

function checkDomainStatus(status) {
  var color = '';
  var display = 'AVAILABLE';

  if (status === 'sold') {
    color = 'bg-red';
    display = 'SOLD';
  }

  return "<div class=\"position-absolute status-box ".concat(color, "\">").concat(display, "</div>");
}

;

function prepareDomain(domain) {
  return "\n        <div class=\"col-md-3 col-sm-6 col-xs-6 col-6\">\n            <article class='domain position-relative'>\n                ".concat(checkDomainStatus(domain['status']), "\n                <a href=\"").concat(domain['url'], "\">\n                    <div class='domain-image-container'>\n                        <img src=\"").concat(domain['thumbnail_image'], "\"\n                            alt=\"").concat(domain['full_name'], "\" class='domain-image' />\n                    </div>\n                </a>\n                <div class='hit-info-container'>\n                    <a href=\"").concat(domain['url'], "\">\n                        <h5>").concat(domain['full_name'], "</h5>\n                    </a>\n                    <div class=\"domain-footer\">\n                        <p><span class=\"purple\">$</span> ").concat(domain['price'], "</p>\n                        <div class=\"followediv\">\n                            <p onclick='addFavourites()' data-domain-id=\"").concat(domain['id'], "\">\n                                <img id=\"like-btn\" src=\"").concat(getFavouriteStatus(id = domain['id']), "\"\n                                    alt=\"").concat(domain['full_name'], "\" />\n                            </p>\n                        </div>\n                    </div>\n                </div>\n            </article>\n        </div>");
}

;

function getFavourites(ids) {
  var default_url = "".concat(location.origin, "/v1/api/domains/?");
  var container = $('#domainRow');

  for (var item in ids) {
    default_url += "ids=".concat(ids[item], "&");
  }

  $.get(default_url, function (data) {
    for (var domain in data.results) {
      var domain_node = prepareDomain(data.results[domain]);
      $(domain_node).appendTo(container);
    }
  });
}

function updateFavouriteStatus(item) {
  var btnLike = $(item).find('#like-btn').attr('src');
  var liked = "".concat(window.origin, "/static/images/like.svg");
  var not_liked = "".concat(window.origin, "/static/images/like-2.svg");

  if (btnLike === liked) {
    $(event.currentTarget).find('#like-btn').attr('src', not_liked);
  } else {
    $(event.currentTarget).find('#like-btn').attr('src', liked);
  }

  ;
}

;

function getFavouriteStatus(id) {
  var stored_data = localStorage.getItem('favourites');

  if (stored_data) {
    stored_data = JSON.parse(stored_data);
    var existed = stored_data.domains.filter(function (item) {
      return parseInt(item) === parseInt(id);
    });

    if (existed.length > 0) {
      return "".concat(window.origin, "/static/images/like.svg");
    } else {
      return "".concat(window.origin, "/static/images/like-2.svg");
    }
  }

  return "".concat(window.origin, "/static/images/like-2.svg");
}

;

function removeFromArray(value, arr) {
  arr = arr.filter(function (item) {
    return item !== value;
  });
  return arr;
}

;