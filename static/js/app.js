$(document).ready(function(){

    // Initializing an empty array
    phoneArray = []
    $('#something tr').each(function() {
	    var something = $(this).find("td").eq(2).html();
	    phoneArray.push(something);	    
	    console.log(something);
    });
    console.log(phoneArray)

    $(".callBtn").click(function(event) {
        event.preventDefault();
        var id = this.id;

        $.ajax({
            type: "POST",
            data: {
                "phone_number": phoneArray[id],
                csrfmiddlewaretoken: csrf_token
            },
        });
    });

})