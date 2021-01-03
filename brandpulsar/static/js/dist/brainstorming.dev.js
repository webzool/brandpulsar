"use strict";

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance"); }

function _iterableToArray(iter) { if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } }

var brainStormingAPI = {
  api_domain: 'https://api.datamuse.com/',
  cosmic_endpoint: "".concat(location.protocol, "//").concat(location.host, "/v1/api/brainstorming/"),
  max_response_count: 10,
  // Max word per response
  min_score: 1000,
  // Min score for fetched words
  min_length: 3,
  // Min length of the words
  api_jja: new Array(),
  api_jjb: new Array(),
  api_syn: new Array(),
  api_trg: new Array(),
  api_ant: new Array(),
  api_spc: new Array(),
  api_gen: new Array(),
  api_com: new Array(),
  api_par: new Array(),
  api_bga: new Array(),
  api_bgb: new Array(),
  api_rhy: new Array(),
  api_nry: new Array(),
  api_hom: new Array(),
  api_cns: new Array(),
  cosmic_domains: new Object(),
  storeResults: function storeResults(result) {
    var _this = this;

    var words = new Array(); // filters words which has score greater than 1000

    var related = result.filter(function (element) {
      return element.score > _this.min_score && element.word.length > _this.min_length;
    });
    related.forEach(function (element) {
      // For appropriate results, we need to cut long words
      // into small parts, and return domains which contain those parts
      if (element.word.length >= 5) {
        var word = element.word.substring(0, 5);
        words.push(word);
      } else {
        words.push(element.word);
      }
    });
    return words;
  },
  clear: function clear() {
    this.api_jja = [];
    this.api_jjb = [];
    this.api_syn = [];
    this.api_trg = [];
    this.api_ant = [];
    this.api_spc = [];
    this.api_gen = [];
    this.api_com = [];
    this.api_par = [];
    this.api_bga = [];
    this.api_bgb = [];
    this.api_rhy = [];
    this.api_nry = [];
    this.api_hom = [];
    this.api_cns = [];
  },
  fetcher: function fetcher(url) {
    var _this2 = this;

    var arr = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
    fetch(url).then(function (response) {
      return response.json();
    }).then(function (data) {
      if (arr) {
        var result = _this2.storeResults(data);

        result.forEach(function (element) {
          return arr.push(element);
        });
        return arr;
      } else {
        _this2.cosmic_domains = data;
      }
    });
  },
  fetchJJA: function fetchJJA(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_jja=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_jja);
  },
  fetchJJB: function fetchJJB(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_jjb=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_jjb);
  },
  fetchSYN: function fetchSYN(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_syn=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_syn);
  },
  fetchTRG: function fetchTRG(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_trg=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_trg);
  },
  fetchANT: function fetchANT(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_ant=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_ant);
  },
  fetchSPC: function fetchSPC(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_spc=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_spc);
  },
  fetchGEN: function fetchGEN(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_gen=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_gen);
  },
  fetchCOM: function fetchCOM(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_com=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_com);
  },
  fetchPAR: function fetchPAR(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_par=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_par);
  },
  fetchBGA: function fetchBGA(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_bga=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_bga);
  },
  fetchBGB: function fetchBGB(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_bgb=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_bgb);
  },
  fetchRHY: function fetchRHY(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_rhy=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_rhy);
  },
  fetchNRY: function fetchNRY(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_nry=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_nry);
  },
  fetchHOM: function fetchHOM(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_hom=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_hom);
  },
  fetchCNS: function fetchCNS(word) {
    return this.fetcher(url = "".concat(this.api_domain, "words?rel_cns=").concat(word, "&max=").concat(this.max_response_count), arr = this.api_cns);
  },
  fetchAll: function fetchAll(word) {
    this.clear();
    this.fetchJJA(word);
    this.fetchJJB(word);
    this.fetchSYN(word);
    this.fetchTRG(word);
    this.fetchANT(word);
    this.fetchSPC(word);
    this.fetchGEN(word);
    this.fetchCOM(word);
    this.fetchPAR(word);
    this.fetchBGA(word);
    this.fetchBGB(word); //this.fetchRHY(word);
    //this.fetchNRY(word);
    //this.fetchHOM(word);
    //this.fetchCNS(word);
  },
  fetchCosmicDomains: function fetchCosmicDomains(word) {
    var industry = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
    var q = "q=".concat(word, "&");
    var industries = "";
    var keywords = this.getList();

    for (var key in keywords) {
      q += "q=".concat(keywords[key], "&");
    }

    for (var i in industry) {
      industries += "industry=".concat(industry[i], "&");
    }

    if (industry) {
      this.fetcher(url = "".concat(this.cosmic_endpoint, "?").concat(industries).concat(q));
    } else {
      this.fetcher(url = "".concat(this.cosmic_endpoint, "?").concat(q));
    }
  },
  getList: function getList() {
    return [].concat(_toConsumableArray(this.api_jja), _toConsumableArray(this.api_jjb), _toConsumableArray(this.api_syn), _toConsumableArray(this.api_trg), _toConsumableArray(this.api_ant), _toConsumableArray(this.api_spc), _toConsumableArray(this.api_gen), _toConsumableArray(this.api_com), _toConsumableArray(this.api_par), _toConsumableArray(this.api_bga), _toConsumableArray(this.api_bgb), _toConsumableArray(this.api_rhy), _toConsumableArray(this.api_nry), _toConsumableArray(this.api_hom), _toConsumableArray(this.api_cns));
  }
};
var brainStormingResults = {
  checkDomainStatus: function checkDomainStatus(status) {
    var color = '';
    var display = 'AVAILABLE';

    if (status === 'sold') {
      color = 'bg-red';
      display = 'SOLD';
    }

    return "<div class=\"position-absolute status-box ".concat(color, "\">").concat(display, "</div>");
  },
  getFavouriteStatus: function getFavouriteStatus(id) {
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
  },
  prepareDomainBox: function prepareDomainBox(domain) {
    return "\n        <div class=\"col-md-3 col-sm-6 col-xs-6 col-6\">\n            <article class='domain position-relative'>\n                ".concat(this.checkDomainStatus(domain['status']), "\n                <a href=\"").concat(domain['url'], "\">\n                    <div class='domain-image-container'>\n                        <img src=\"").concat(domain['thumbnail_image'], "\"\n                            alt=\"").concat(domain['full_name'], "\" class='domain-image' />\n                    </div>\n                </a>\n                <div class='hit-info-container'>\n                    <a href=\"").concat(domain['url'], "\">\n                        <h5>").concat(domain['full_name'], "</h5>\n                    </a>\n                    <div class=\"domain-footer\">\n                        <p><span class=\"purple\">$</span> ").concat(domain['price'], "</p>\n                        <div class=\"followediv\">\n                            <p onclick='addFavourites()' data-domain-id=\"").concat(domain['id'], "\">\n                                <img id=\"like-btn\" src=\"").concat(this.getFavouriteStatus(id = domain['id']), "\"\n                                    alt=\"").concat(domain['full_name'], "\" />\n                            </p>\n                        </div>\n                    </div>\n                </div>\n            </article>\n        </div>");
  },
  prepareDomainList: function prepareDomainList(list, container) {
    container.empty();

    for (var domain in list) {
      var item = this.prepareDomainBox(list[domain]);
      $(item).appendTo(container);
    }
  }
};
$(document).ready(function () {
  $('#submit-word').on('click', function () {
    var search = $('#id_word').val();
    var industry = $('#id_industry').val();
    brainStormingAPI.fetchAll(search);
    setTimeout(function () {
      if (industry) {
        brainStormingAPI.fetchCosmicDomains(search, industry);
      } else {
        brainStormingAPI.fetchCosmicDomains(search);
      }

      ;
      setTimeout(function () {
        var domains = brainStormingAPI.cosmic_domains;
        brainStormingResults.prepareDomainList(list = domains, container = $('#brainstorming_results'));
        console.log(brainStormingAPI.getList());
      }, 1000);
    }, 1000);
  });
});