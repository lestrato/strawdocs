function ajax_post(form, old_dom, new_dom){
      /* Take the the form, the dom ("#answers") for example, and the type of
      element to be saved */
    $.ajax({
        data: $(form).serialize(), // get the form data
        type: $(form).attr('method'), // GET or POST
        url: $(form).attr('action'), // the file to call
        // handle a successful response
        success : function(response) {
            $(old_dom).replaceWith($(response).find(new_dom));
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
