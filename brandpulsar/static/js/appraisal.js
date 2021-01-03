const domainAppraisal = {
    api_url: `http://${location.host}/v1/api/appraisal/`,

    get_value(domain) {
        const url = `${this.api_url}?d=${domain}`;
        fetch(url)
            .then(response => response.json())
            .then((data) => {
                this.append(price = data['estimated_price']);
            });
    },

    append(price) {
        $('#estimated-price').html(`<div class="form-alert-box"><span class="spinner-grow mr-2 spinner-grow-sm" role="status" aria-hidden="true"></span>Calculating...</div>`);
        setTimeout(() => {
            if (price) {
                $('#estimated-price').html(`<div class="form-alert-box"><div><span>Your domain estimated price is</span>${price} USD</div></div>`);
            } else {
                $('#estimated-price').attr(`Can not find estimated price`);
            }
        }, 3000);
    },

    handle(input, type) {
        input.on(type, () => {
            const name = $('#id_name').val();
            const extension = $('#id_extension').val();
            const domain = `${name}.${extension}`;
            this.get_value(domain);
        });
    }
}

const negotiationField = document.getElementById('id_negotiation');
const lowestPriceField = document.getElementById('lowest_price_field');

negotiationField.onchange = function () {
    if (this.value === 'yes') {
        lowestPriceField.style.display = 'block';
    } else if (this.value === 'no' || this.value === 'Choose') {
        lowestPriceField.style.display = 'none';
    }
}

const name = $('#id_name');
const extension = $('#id_extension');

domainAppraisal.handle(name, type = 'keyup');
domainAppraisal.handle(extension, type = 'change');