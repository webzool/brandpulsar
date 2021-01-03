"use strict";

var domainAppraisal = {
  api_url: "http://".concat(location.host, "/v1/api/appraisal/"),
  get_value: function get_value(domain) {
    var _this = this;

    var url = "".concat(this.api_url, "?d=").concat(domain);
    fetch(url).then(function (response) {
      return response.json();
    }).then(function (data) {
      _this.append(price = data['estimated_price']);
    });
  },
  append: function append(price) {
    $('#id_price').attr('placeholder', "Calculating...");
    setTimeout(function () {
      if (price) {
        $('#id_price').attr('placeholder', "Estimated price: ".concat(price, " USD"));
      } else {
        $('#id_price').attr('placeholder', "Can not find estimated price");
      }
    }, 3000);
  },
  handle: function handle(input, type) {
    var _this2 = this;

    input.on(type, function () {
      var name = $('#id_name').val();
      var extension = $('#id_extension').val();
      var domain = "".concat(name, ".").concat(extension);

      _this2.get_value(domain);
    });
  }
};
var name = $('#id_name');
var extension = $('#id_extension');
domainAppraisal.handle(name, type = 'keyup');
domainAppraisal.handle(extension, type = 'change');