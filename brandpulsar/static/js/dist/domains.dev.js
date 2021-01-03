"use strict";

// If not url described, main function gets default_url
var default_url = "".concat(location.origin, "/v1/api/domains/");
$(document).ready(function () {
  // Gets data on page load
  if (localStorage.getItem('autocomplete')) {
    var data = JSON.parse(localStorage.getItem('autocomplete'));
    main(redirectAutocomplete(default_url), currentPage = 1, key = data.name);
  } else {
    main();
  } // Sorting options


  $('#sort-filter').on('change', function () {
    var q = $(event.currentTarget).val();
    var sorting_url = "".concat(location.origin, "/v1/api/domains/?sort=").concat(q);
    main(url = sorting_url);
  }); // Filtering

  $('.filter-btn').on('click', function () {
    var filter_url = filtering(default_url);
    var kw = '';
    var kw_dict = {
      contains: $('#id_name').val(),
      tags: $('#id_tags').val()
    };

    for (var item in kw_dict) {
      if (kw_dict[item]) {
        kw = kw_dict[item];
      }
    }

    main(url = filter_url, currentPage = 1, key = kw);
    $("html").animate({
      scrollTop: 0
    }, "slow");
  });
});

function main() {
  var url = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : default_url;
  var currentPage = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 1;
  var key = arguments.length > 2 ? arguments[2] : undefined;
  var container = $('#domainRow');
  var info_box = $('#list-info');
  container.empty();
  info_box.empty(); //clearFilterValues();

  localStorage.setItem('endpoint', url); // FETCH : gets domain list

  fetch(url).then(function (response) {
    return response.json();
  }).then(function (data) {
    return getData(data);
  });

  function getData(data) {
    for (var domain in data.results) {
      var item = prepareDomain(data.results[domain]);
      $(item).appendTo(container);
    }

    ;
    $(prepareInfoBox(count = data['count'], keyword = key)).appendTo(info_box);
    pagination(data.max_page, currentPage);
  }

  ;
} // Helper functions


function saveFavourites(domain) {
  var url = "http://".concat(location.host, "/v1/api/favourite/?d=").concat(domain);
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

;

function removeFromArray(value, arr) {
  arr = arr.filter(function (item) {
    return item !== value;
  });
  return arr;
}

;

function prepareDomain(domain) {
  if (domain['discount_price']) {
    return "\n        <div class=\"col-md-3 col-sm-6 col-xs-6 col-6\">\n            <article class='domain position-relative'>\n                ".concat(checkDomainStatus(domain['status']), "\n                <a href=\"").concat(domain['url'], "\">\n                    <div class='domain-image-container'>\n                        <img src=\"").concat(domain['thumbnail_image'], "\"\n                            alt=\"").concat(domain['full_name'], "\" class='domain-image' />\n                    </div>\n                </a>\n                <div class='hit-info-container'>\n                    <a href=\"").concat(domain['url'], "\">\n                        <h5>").concat(domain['full_name'], "</h5>\n                    </a>\n                    <div class=\"domain-footer\">\n                        <p> <span class=\"purple\">$</span> ").concat(domain['discount_price'], " <s><span>$</span> ").concat(domain['price'], "</s > </p>\n                        <div class=\"followediv\">\n                            <p onclick='addFavourites()' data-domain-id=\"").concat(domain['id'], "\">\n                                <img id=\"like-btn\" src=\"").concat(getFavouriteStatus(id = domain['id']), "\"\n                                    alt=\"").concat(domain['full_name'], "\" />\n                            </p>\n                        </div>\n                    </div>\n                </div>\n            </article>\n        </div>");
  } else {
    return "\n        <div class=\"col-md-3 col-sm-6 col-xs-6 col-6\">\n            <article class='domain position-relative'>\n                ".concat(checkDomainStatus(domain['status']), "\n                <a href=\"").concat(domain['url'], "\">\n                    <div class='domain-image-container'>\n                        <img src=\"").concat(domain['thumbnail_image'], "\"\n                            alt=\"").concat(domain['full_name'], "\" class='domain-image' />\n                    </div>\n                </a>\n                <div class='hit-info-container'>\n                    <a href=\"").concat(domain['url'], "\">\n                        <h5>").concat(domain['full_name'], "</h5>\n                    </a>\n                    <div class=\"domain-footer\">\n                        <p><span class=\"purple\">$</span> ").concat(domain['price'], "</p>\n                        <div class=\"followediv\">\n                            <p onclick='addFavourites()' data-domain-id=\"").concat(domain['id'], "\">\n                                <img id=\"like-btn\" src=\"").concat(getFavouriteStatus(id = domain['id']), "\"\n                                    alt=\"").concat(domain['full_name'], "\" />\n                            </p>\n                        </div>\n                    </div>\n                </div>\n            </article>\n        </div>");
  }
}

;

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

function pagination(count, currentPage) {
  var pagination_container = $('.pagination');
  pagination_container.empty();
  var navs = "\n    <li class=\"page-before page-item\">\n        <a class=\"page-link\" onclick=\"getPage(".concat(currentPage - 1, ")\">\xAB</a>\n    </li>\n    <li class=\"page-next page-item\">\n        <a class=\"page-link\" onclick=\"getPage(").concat(currentPage + 1, ")\">\xBB</a>\n    </li>");
  $(navs).appendTo(pagination_container);

  for (var i = 1; i < count + 1; i++) {
    var active = '';

    if (i === parseInt(currentPage)) {
      active = 'active';
    }

    var page = "<li class=\"page-item ".concat(active, "\"><a class=\"page-link\"\n            onclick=\"getPage(").concat(i, ")\">").concat(i, "</a></li>");
    $(page).appendTo(pagination_container).insertBefore('.page-next');
  }
}

function getPage(page) {
  var offset = '';

  if (page) {
    offset = (page - 1) * 20;
  }

  var url = localStorage.getItem('endpoint');
  var next_url = "".concat(url, "?offset=").concat(parseInt(offset));

  if (url.includes('?')) {
    next_url = "".concat(url, "&offset=").concat(parseInt(offset));
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
    tags: $('#id_tags').val()
  };
} //function clearFilterValues() {
//    const filters = [
//        '#id_price_gt',
//        '#id_price_lt',
//        '#id_length_gt',
//        '#id_length_lt',
//        '#id_name',
//        '#id_tags'
//    ]
//    for (let i = 0; i < filters.length; i++) {
//        $(filters[i]).val("");
//    }
//}


function filtering(url) {
  var path = '';
  var lookup_query = getFilterValues();
  Object.keys(lookup_query).forEach(function (key) {
    if (lookup_query[key]) {
      path += "".concat(key, "=").concat(lookup_query[key], "&");
    }
  });
  return "".concat(url, "?").concat(path);
}

function redirectAutocomplete(url) {
  path = '';
  var autocomplete = localStorage.getItem('autocomplete');
  autocomplete = JSON.parse(autocomplete);
  var filters = getFilterValues();

  if (autocomplete.type in filters) {
    path += "".concat(autocomplete.type, "=").concat(autocomplete.name, "&");
  }

  localStorage.removeItem('autocomplete');
  return "".concat(url, "?").concat(path);
}

;

function prepareInfoBox(count, keyword) {
  var domain = 'domains';

  if (parseInt(count) <= 1) {
    domain = 'domain';
  }

  var result = "<span>Listing ".concat(count, " ").concat(domain, ".</span>");

  if (keyword) {
    result = "\n        <strong class=\"strong-text\">".concat(keyword, "</strong>: \n        <span>Listing ").concat(count, " ").concat(domain, "</span>.\n        <span class=\"clear-btn\" onclick=\"main()\">Clear</span>");
  }

  return result;
}