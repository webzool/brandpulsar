const dashboardItems = {
    api_url: `${location.protocol}//${location.host}/v1/api/my-domains/`,
    container: $("#domains_table"),
    pagination_container: $(".pagination"),

    fetch(url = this.api_url, page = 1) {
        fetch(url)
            .then((response) => response.json())
            .then((data) => {
                this.pagination_container.empty();
                this.append((n = data["started_from"]), (list = data["results"]));
                if (data.max_page > 1) {
                    this.pagination((count = data.max_page), (currentPage = page));
                }
                console.log("data", data);
                if (data.count < 1) {}
                localStorage.setItem("endpoint", this.api_url);
            });
    },

    build_row(n, domain) {
        let is_active;
        let featured;
        let update;
        let del;
        let setup = '';

        const deactive = '<span class="pending-circle"></span>';
        const waiting =
            '<a href="#" class="link" style="font-size: 8px;color: #ff5e16;font-weight: 700;text-transform: uppercase;letter-spacing: 0.5px;">Verify domain</a>';
        const active = '<span class="active-circle"></span>';
        const pending = `<img src="${location.protocol}//${location.host}/static/images/pending.svg" style="width: 20px;" />`;
        const featured_false = `<button plan-id="${domain["featured_plan_id"]}" class="link featured-plan" style="font-size: 8px;font-weight: 700;text-transform: uppercase;letter-spacing: 0.5px;">Make featured</button>`;
        const featured_true = '<span class="active-circle"></span>';

        if (domain["is_active"] === "listed") {
            is_active = active;
        } else if (domain["is_active"] === "waiting") {
            is_active = waiting;
        } else {
            is_active = pending;
        }

        if (domain["featured"] === false) {
            featured = featured_false;
        } else {
            featured = featured_true;
        }

        // If domain status is *SOLD* user can not delete or edit it.
        if (domain["status"] === "sold" || domain["is_active"] === "listed") {
            update = `<a class="dropdown-item">Edit</a>`;
            del = `<a class="dropdown-item">Delete</a>`;
        } else {
            setup = `<a class="dropdown-item" href="${location.protocol}//${location.host}/marketplace/setup/${domain["id"]}">Setup</a>`;
            update = `<a class="dropdown-item" href="${location.protocol}//${location.host}/marketplace/update/${domain["id"]}">Edit</a>`;
            del = `<a class="dropdown-item" href="${location.protocol}//${location.host}/marketplace/delete/${domain["id"]}">Delete</a>`;
        }

        return `<tr>
        <th scope="row">${n}</th>
        <td id="domain-name">${domain["full_name"]}</td>
        <td><span class="status">${domain["status"]}</span></td>
        <td>${domain["ranking"]}</td>
        <td id="domain-price">$ ${domain["price"]}</td>
        
        <td>${domain["favorite_count"]}</td>
        <td>${featured}</td>
        <td>${domain["date_created"]}</td>
        <td>${is_active}</td>
        <td>
          <div class="dropdown">
            <a class="dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown"
              aria-haspopup="true" aria-expanded="false">
              <img src="${location.protocol}//${location.host}/static/images/more.svg" class="more" />
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            ${setup}
            <div class="dropdown-divider"></div>
              ${update}
              <div class="dropdown-divider"></div>
              ${del}
            </div>
          </div>
        </td>
      </tr>
      `;
    },

    append(n, list) {
        this.container.empty();

        for (let d in list) {
            n += 1;
            const domain = this.build_row((n = n), list[d]);
            $(domain).appendTo(this.container);
        }
    },

    getPage(page) {
        let offset = "";
        if (page) {
            offset = (page - 1) * 20;
        }
        let url = localStorage.getItem("endpoint");
        let next_url = `${url}?offset=${parseInt(offset)}`;
        if (url.includes("?")) {
            next_url = `${url}&offset=${parseInt(offset)}`;
        }
        $("html").animate({
                scrollTop: 0,
            },
            "slow"
        );
        return this.fetch(next_url, (page = page));
    },

    pagination(count, currentPage = 1) {
        this.pagination_container.empty();
        let navs = `
        <li class="page-before page-item">
            <a class="page-link" onclick="dashboardItems.getPage(${
              currentPage - 1
            })">«</a>
        </li>
        <li class="page-next page-item">
            <a class="page-link" onclick="dashboardItems.getPage(${
              currentPage + 1
            })">»</a>
        </li>`;

        $(navs).appendTo(this.pagination_container);

        for (let i = 1; i < count + 1; i++) {
            let active = "";
            if (i === parseInt(currentPage)) {
                active = "active";
            }
            let page = `<li class="page-item ${active}"><a class="page-link"
                onclick="dashboardItems.getPage(${i})">${i}</a></li>`;
            $(page).appendTo(this.pagination_container).insertBefore(".page-next");
        }
    },
};

dashboardItems.fetch();

$("#filter_options").on("change", () => {
    const value = $(event.currentTarget).val();
    const url = `${dashboardItems.api_url}?f=${value}`;
    dashboardItems.fetch(url);

});

const stripe = Stripe(pub_key);

var createCheckoutSession = function (priceId, paymentType) {
    return fetch("/create-checkout-session/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            priceId: priceId,
            paymentType: paymentType
        }),
    }).then(function (result) {
        return result.json();
    });
};


window.addEventListener("load", function () { // when the page has loaded
    let buttons = document.querySelectorAll('.featured-plan')

    buttons.forEach((btn) => {

        btn.addEventListener("click", (event) => {
            let planId = btn.getAttribute("plan-id");
            let paymentType = "featured";
            createCheckoutSession(planId, paymentType).then(function (data) {
                stripe.redirectToCheckout({
                    sessionId: data.id,
                }).then(function (result) {
                    if (result.error) {
                        var displayError = document.getElementById("error-message");
                        displayError.textContent = result.error.message;
                    }
                });
            });
        });
    });
});