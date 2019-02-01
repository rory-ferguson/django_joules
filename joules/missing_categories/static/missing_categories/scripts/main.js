
// Submit post on submit
$('#content form').on('submit', function(event){
    event.preventDefault();
    $('#content div.uk i').removeClass('hidden')
});

function validateFunc() {
    formData = $('form').serializeArray();
    env = formData[1].value
    create_post(env)
    return false;
}

function create_post(env) {
    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        url : "",
        type : "POST",
        data : { env : env },
        async: true,
        success : function(json) {
            prod_list = ''
            for (const [key, value] of Object.entries(json.uk)) {
                prod_list += '<p>' + value + '</p>'
            }
            $('#content div.uk').append(prod_list)

            prod_list = ''
            for (const [key, value] of Object.entries(json.us)) {
                prod_list += '<p>' + value + '</p>'
            }
            $('#content div.us').append(prod_list)

            prod_list = ''
            for (const [key, value] of Object.entries(json.de)) {
                prod_list += '<p>' + value + '</p>'
            }
            $('#content div.de').append(prod_list)

            $('#content div.uk i').addClass('hidden')
        },

        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+ errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};