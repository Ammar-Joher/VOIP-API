$(document).ready(function(){

    // Initializing an empty array
    phoneArray = []
    $('#something tr').each(function() {
	    var something = $(this).find("td").eq(2).html();
	    phoneArray.push(something);	    
	    console.log(something);
    });
    console.log(phoneArray)

    // Sends POST Request to Django On Call Button Click.
    $(".callBtn").click(function(event) {
        event.preventDefault();
        var id = this.id;

        $.ajax({
            type: "POST",
            data: {
                "data": "call",
                "phone_number": phoneArray[id],
                csrfmiddlewaretoken: csrf_token
            },
        });
    });

})