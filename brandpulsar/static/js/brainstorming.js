const brainStormingAPI = {
    api_domain: 'https://api.datamuse.com/',
    cosmic_endpoint: `${location.protocol}//${location.host}/v1/api/brainstorming/`,

    max_response_count: 10, // Max word per response
    min_score: 100, // Min score for fetched words
    min_length: 3, // Min length of the words

    api_jja: new Array,
    api_jjb: new Array,
    api_syn: new Array,
    api_trg: new Array,
    api_ant: new Array,
    api_spc: new Array,
    api_gen: new Array,
    api_com: new Array,
    api_par: new Array,
    api_bga: new Array,
    api_bgb: new Array,
    api_rhy: new Array,
    api_nry: new Array,
    api_hom: new Array,
    api_cns: new Array,

    cosmic_domains: new Object,

    storeResults(result, crop = true) {
        const words = new Array;
        // filters words which has score greater than 1000
        const related = result.filter(element => element.score > this.min_score && element.word.length > this.min_length);
        related.forEach((element) => {

            // For appropriate results, we need to cut long words
            // into small parts, and return domains which contain those parts
            if (crop && element.word.length >= 5) {
                const word = element.word.substring(0, 5);
                words.push(word);
            } else {
                words.push(element.word);
            }
        });
        return words;
    },
    clear() {
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
    clearRelated() {
        this.api_hom = [];
        this.api_cns = [];
        this.api_syn = [];
        this.api_spc = [];
        this.api_rhy = [];
    },
    fetcher(url, arr = null, crop = true) {
        let result;
        fetch(url)
            .then(response => response.json())
            .then((data) => {
                if (arr) {
                    if (crop) {
                        result = this.storeResults(data);
                    } else {
                        result = this.storeResults(data, crop = false);
                    }
                    result.forEach(element => arr.push(element));
                    return arr;
                } else {
                    this.cosmic_domains = data;
                }
            })
    },
    fetchJJA(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_jja=${word}&max=${this.max_response_count}`,
            arr = this.api_jja,
            crop = crop
        );
    },
    fetchJJB(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_jjb=${word}&max=${this.max_response_count}`,
            arr = this.api_jjb,
            crop = crop
        );
    },
    fetchSYN(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_syn=${word}&max=${this.max_response_count}`,
            arr = this.api_syn,
            crop = crop
        );
    },
    fetchTRG(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_trg=${word}&max=${this.max_response_count}`,
            arr = this.api_trg,
            crop = crop
        );
    },
    fetchANT(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_ant=${word}&max=${this.max_response_count}`,
            arr = this.api_ant,
            crop = crop
        );
    },
    fetchSPC(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_spc=${word}&max=${this.max_response_count}`,
            arr = this.api_spc,
            crop = crop
        );
    },
    fetchGEN(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_gen=${word}&max=${this.max_response_count}`,
            arr = this.api_gen,
            crop = crop
        );
    },
    fetchCOM(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_com=${word}&max=${this.max_response_count}`,
            arr = this.api_com,
            crop = crop
        );
    },
    fetchPAR(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_par=${word}&max=${this.max_response_count}`,
            arr = this.api_par,
            crop = crop
        );
    },
    fetchBGA(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_bga=${word}&max=${this.max_response_count}`,
            arr = this.api_bga,
            crop = crop
        );
    },
    fetchBGB(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_bgb=${word}&max=${this.max_response_count}`,
            arr = this.api_bgb,
            crop = crop
        );
    },
    fetchRHY(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_rhy=${word}&max=${this.max_response_count}`,
            arr = this.api_rhy,
            crop = crop
        );
    },
    fetchNRY(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_nry=${word}&max=${this.max_response_count}`,
            arr = this.api_nry,
            crop = crop
        );
    },
    fetchHOM(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_hom=${word}&max=${this.max_response_count}`,
            arr = this.api_hom,
            crop = crop
        );
    },
    fetchCNS(word, crop = true) {
        return this.fetcher(
            url = `${this.api_domain}words?rel_cns=${word}&max=${this.max_response_count}`,
            arr = this.api_cns,
            crop = crop
        );
    },
    fetchAll(word) {
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
        this.fetchBGB(word);
        //this.fetchRHY(word);
        //this.fetchNRY(word);
        //this.fetchHOM(word);
        //this.fetchCNS(word);
    },
    fetchRelated(word) {
        /*  Gets related words from listed endpoints.
        */
        this.clearRelated();
        this.fetchSYN(word, crop = false);
        this.fetchSPC(word, crop = false);
        this.fetchRHY(word, crop = false);
        this.fetchHOM(word, crop = false);
        this.fetchCNS(word, crop = false);
    },
    fetchCosmicDomains(word, industry = null, limit = null) {
        let q = `q=${word}&`;
        let industries = "";
        let limits = "";
        if(limit) {
            limits = `limit=${limit}`;
        }
        const keywords = this.getList();
        for (let key in keywords) {
            q += `q=${keywords[key]}&`;
        }
        for (let i in industry) {
            industries += `industry=${industry[i]}&`;
        }
        if (industry) {
            this.fetcher(url = `${this.cosmic_endpoint}?${industries}${q}${limits}`);
        } else {
            this.fetcher(url = `${this.cosmic_endpoint}?${q}${limits}`);
        }
    },
    getList() {
        return [
            ...this.api_jja, ...this.api_jjb, ...this.api_syn,
            ...this.api_trg, ...this.api_ant, ...this.api_spc,
            ...this.api_gen, ...this.api_com, ...this.api_par,
            ...this.api_bga, ...this.api_bgb, ...this.api_rhy,
            ...this.api_nry, ...this.api_hom, ...this.api_cns,
        ];
    },
    getRelated() {
        return {
            synonyms: this.api_syn,
            hypernyms: this.api_spc,
            rhymes: this.api_rhy,
            homophones: this.api_hom,
            consonant: this.api_cns,
        }
    }
};

const brainStormingResults = {
    checkDomainStatus(status) {
        let color = '';
        let display = 'AVAILABLE';

        if (status === 'sold') {
            color = 'bg-red';
            display = 'SOLD';
        }
        return `<div class="position-absolute status-box ${color}">${display}</div>`;
    },

    getFavouriteStatus(id) {
        let stored_data = localStorage.getItem('favourites');
        if (stored_data) {
            stored_data = JSON.parse(stored_data);
            let existed = stored_data.domains.filter(item => parseInt(item) === parseInt(id));
            if (existed.length > 0) {
                return `${window.origin}/static/images/like.svg`;
            } else {
                return `${window.origin}/static/images/like-2.svg`;
            }
        }
        return `${window.origin}/static/images/like-2.svg`;
    },

    prepareDomainBox(domain) {
        return `
        <div class="col-md-3 col-sm-6 col-xs-6 col-6">
            <article class='domain position-relative'>
                ${this.checkDomainStatus(domain['status'])}
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
                            <p onclick='addFavourites()' data-domain-id="${domain['id']}">
                                <img id="like-btn" src="${this.getFavouriteStatus(id = domain['id'])}"
                                    alt="${domain['full_name']}" />
                            </p>
                        </div>
                    </div>
                </div>
            </article>
        </div>`;
    },

    prepareDomainSearchBarResult(domain) {
        /* HOME PAGE SEARCH BAR RESULT */
        return `<li class="autocomplete-item">
            <a class="text-decoration-none" href="${domain.url}">
            <p>${domain.full_name}</p> <span>domain</span></a>
        </li>`;
    },

    prepareRelatedWordsBox(header, list) {
        let words_node = '';
        for (let i in list) {
            words_node += `<a class="idea-label">${list[i]}</a>`;
        }
        return `<div class="ideas-box mb-5">
        <h5>${header.toUpperCase()}</h5>
        <div class="ideas-labels">${words_node}</div>
    </div>`
    },

    prepareDomainList(list, container) {
        container.empty();
        for (let domain in list) {
            const item = this.prepareDomainBox(list[domain]);
            $(item).appendTo(container);
        }
    }
}

$(document).ready(() => {
    $('#submit-word').on('click', () => {
        const search = $('#id_word').val();
        const industry = $('#id_industry').val();
        brainStormingAPI.fetchAll(search);

        setTimeout(
            function () {
                if (industry) {
                    brainStormingAPI.fetchCosmicDomains(search, industry);
                } else {
                    brainStormingAPI.fetchCosmicDomains(search);
                };
                setTimeout(() => {
                    const domains = brainStormingAPI.cosmic_domains;
                    brainStormingResults.prepareDomainList(
                        list = domains,
                        container = $('#brainstorming_results')
                    );
                }, 1000);
            }, 1000);

        setTimeout(
            function () {
                brainStormingAPI.fetchRelated(search);
                setTimeout(() => {
                    const related_words_container = $('#related-words-container');
                    related_words_container.empty();
                    const words = brainStormingAPI.getRelated();
                    for (const [key, value] of Object.entries(words)) {
                        if (value.length > 0) {
                            const container = brainStormingResults.prepareRelatedWordsBox(
                                header = key, list = value);
                            $(container).appendTo(related_words_container);
                        }
                    }
                }, 1000);
            }, 1000);

    });

});