function MesFormulaires(){
    console.log('MesFormulaires');
    redirectUrl = '/' + loginCust;
    document.location.href = redirectUrl;
}

function newForm(myCustomer) {
    console.log(myCustomer.loginCust);
    $.ajax({
        type: 'POST',
        url: '{% url "details" loginCust=myCustomer.loginCust %}',
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'action': 'newForm',
            'Customer': myCustomer
        },
        success: function(response) {
            if (response.success) {
                //Redirection vers la page qui cherche le formulaire
                var redirectUrl = '{% url "redirection" loginCust=myCustomer.loginCust %}';
                document.location.href = redirectUrl;
            } else {
                console.log("Échec");
            }
        }
    });
}