"use strict";

var dashboardItems = {
  api_url: "".concat(location.protocol, "//").concat(location.host, "/v1/api/my-domains/"),
  container: $('#domains_table'),
  pagination_container: $('.pagination'),
  fetch: function (_fetch) {
    function fetch() {
      return _fetch.apply(this, arguments);
    }

    fetch.toString = function () {
      return _fetch.toString();
    };

    return fetch;
  }(function () {
    var _this = this;

    var url = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.api_url;
    var page = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 1;
    fetch(url).then(function (response) {
      return response.json();
    }).then(function (data) {
      _this.pagination_container.empty();

      _this.append(n = data['started_from'], list = data['results']);

      if (data.max_page > 1) {
        _this.pagination(count = data.max_page, currentPage = page);
      }

      localStorage.setItem('endpoint', _this.api_url);
    });
  }),
  build_row: function build_row(n, domain) {
    var is_active;
    var featured;
    var update;
    var del;
    var deactive = '<span class="pending-circle"></span>';
    var active = '<span class="active-circle"></span>';

    if (domain['is_active'] === 'active') {
      is_active = active;
    } else {
      is_active = deactive;
    }

    ;

    if (domain['featured'] === false) {
      featured = deactive;
    } else {
      featured = active;
    } // If domain status is *SOLD* user can not delete or edit it.


    if (domain['status'] === 'sold') {
      update = "<a class=\"dropdown-item\">Edit</a>";
      del = "<a class=\"dropdown-item\">Delete</a>";
    } else {
      update = "<a class=\"dropdown-item\" href=\"".concat(location.protocol, "//").concat(location.host, "/marketplace/update/").concat(domain['id'], "\">Edit</a>");
      del = "<a class=\"dropdown-item\" href=\"".concat(location.protocol, "//").concat(location.host, "/marketplace/delete/").concat(domain['id'], "\">Delete</a>");
    }

    return "<tr>\n        <th scope=\"row\">".concat(n, "</th>\n        <td>").concat(domain['full_name'], "</td>\n        <td><span class=\"status\">").concat(domain['status'], "</span></td>\n        <td>").concat(domain['ranking'], "</td>\n        <td>$ ").concat(domain['price'], "</td>\n        <td>").concat(is_active, "</td>\n        <td>").concat(domain['favorite_count'], "</td>\n        <td>").concat(featured, "</td>\n        <td>").concat(domain['date_created'], "</td>\n\n        <td>\n          <div class=\"dropdown\">\n            <a class=\"dropdown-toggle\" href=\"#\" id=\"navbarDropdown\" role=\"button\" data-toggle=\"dropdown\"\n              aria-haspopup=\"true\" aria-expanded=\"false\">\n              <img src=\"").concat(location.protocol, "//").concat(location.host, "/static/images/more.svg\" class=\"more\" />\n            </a>\n            <div class=\"dropdown-menu\" aria-labelledby=\"navbarDropdown\">").concat(update, "\n              <div class=\"dropdown-divider\"></div>").concat(del, "\n            </div>\n          </div>\n        </td>\n      </tr>");
  },
  append: function append(n, list) {
    this.container.empty();

    for (var d in list) {
      n += 1;
      var domain = this.build_row(n = n, list[d]);
      $(domain).appendTo(this.container);
    }
  },
  getPage: function getPage(page) {
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
    return this.fetch(next_url, page = page);
  },
  pagination: function pagination(count) {
    var currentPage = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 1;
    this.pagination_container.empty();
    var navs = "\n        <li class=\"page-before page-item\">\n            <a class=\"page-link\" onclick=\"dashboardItems.getPage(".concat(currentPage - 1, ")\">\xAB</a>\n        </li>\n        <li class=\"page-next page-item\">\n            <a class=\"page-link\" onclick=\"dashboardItems.getPage(").concat(currentPage + 1, ")\">\xBB</a>\n        </li>");
    $(navs).appendTo(this.pagination_container);

    for (var i = 1; i < count + 1; i++) {
      var active = '';

      if (i === parseInt(currentPage)) {
        active = 'active';
      }

      var page = "<li class=\"page-item ".concat(active, "\"><a class=\"page-link\"\n                onclick=\"dashboardItems.getPage(").concat(i, ")\">").concat(i, "</a></li>");
      $(page).appendTo(this.pagination_container).insertBefore('.page-next');
    }
  }
};
dashboardItems.fetch();
$('#filter_options').on('change', function () {
  var value = $(event.currentTarget).val();
  var url = "".concat(dashboardItems.api_url, "?f=").concat(value);
  dashboardItems.fetch(url);
});