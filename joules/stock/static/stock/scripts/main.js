
// Submit post on submit
$('#post form').on('submit', function(event){
    event.preventDefault();
    name = this.className
    sku = $('.' + name + ' div input').val()
    create_post(sku, name);
});


function create_post(sku, name) {
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
        data : { sku : sku },

        success : function(json) {
            $('.prod-cont').val('');

            var htm = []
            htm +='<h4>Sizes:</h4>'
            for (const [key, value] of Object.entries(json.stock)) {
                htm +='<div class="size"><span>' + key + ': </span><span class="stock-value">' + value + ' </span></div>'
            }

            prod_list = '<tr><td align="center">' + json.id + '</td>'
            for (const [key, value] of Object.entries(json.stock)) {
                prod_list +='<td>' + key + ': ' + value + '</td>'
            }
            prod_list += '</tr>'
            console.log(prod_list)

            $('.prod-list table').prepend(prod_list)
            $('.prod-cont div.' + name + '-stock').html(htm)
            $('.prod-cont div.' + name).html('<h3>' + json.id + '</h3><a target="_blank" href="' + json.href + '"><img src="' + json.image + '" style="width:300px;" alt=""></a><p>' + json.name + '</p><p>' + json.price + '</p>');
            console.log("success");

            highlight_low_stock(name);
        },

        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+ errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


function highlight_low_stock(name) {
    console.log('.' + name + '-stock span.stock-value')
    $('.' + name + '-stock span.stock-value').each(function() {
        if ($(this).text() <= 20) {
            console.log(this)
            $(this).css("color", "red");
            $('.prod-cont div.' + name + ' img').css("filter", "grayscale(100%)");
        }
    });
}
