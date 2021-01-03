$(document).ready(() => {
    console.log('stripe')




    // const stripe = Stripe(pub_key);

    // var createCheckoutSession = function (priceId, paymentType) {
    //     return fetch("/create-checkout-session/", {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json"
    //         },
    //         body: JSON.stringify({
    //             priceId: priceId,
    //             paymentType: paymentType,
    //             product_image: productImg,
    //             product_name: productName,
    //             product_price: productPrice,
    //             product_description: productDescription
    //         })
    //     }).then(function (result) {
    //         return result.json();
    //     });
    // };

    // var handleResult = function (result) {
    //     if (result.error) {
    //         var displayError = document.getElementById("error-message");
    //         displayError.textContent = result.error.message;
    //     }
    // };


    // $('#featured-plan').each(function () {

    //     $(this).addEventListener('click', function () {
    //         console.log("click")
    //         let plan_id = $(this).attr('plan-id');

    //         let paymentType = 'instalment'

    //         createCheckoutSession(plan_id, paymentType).then(function (data) {
    //             stripe
    //                 .redirectToCheckout({
    //                     sessionId: data.id
    //                 })
    //                 .then(handleResult);
    //         });
    //     })

    // });

});