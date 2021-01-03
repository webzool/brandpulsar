$(document).ready(() => {

    const blur = '<div class ="blur"></div>'

    getDomainStatus()

    $('#check_domain').on('click', () => {
        getDomainStatus()
    });

    function getDomainStatus() {
        const d = $('#check_domain').attr('data-name');
        const url = `${location.origin}/v1/api/verify/?d=${d}`;

        fetch(url)
            .then(response => response.json())
            .then(function (data) {
                console.log(data)
                $('#check_domain').html(`<span class="spinner-grow mr-2 spinner-grow-sm" role="status" aria-hidden="true"></span>Checking...</div>`);
                setTimeout(() => {
                    if (data === 'pending' || data === 'listed') {
                        $('#check_domain').html(`<img src="${location.protocol}//${location.host}/static/images/check-white.svg" style="width: 20px!important;margin-right: 10px;margin-left: 0px;" />Your domain verified`);
                        $('#check_domain').addClass('btn-green');
                    } else {
                        $('#check_domain').html(`Please verify your domain`);
                        $('.step-2').append(blur)
                    }
                }, 3000);
            });
    }


});