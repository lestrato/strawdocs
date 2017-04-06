function ajax_post(form, old_dom, new_dom){
      /* Take the the form, the dom ("#answers") for example, and the type of
      element to be saved */
    $.ajax({
        data: $(form).serialize(), // get the form data
        type: $(form).attr('method'), // GET or POST
        url: $(form).attr('action'), // the file to call
        // handle a successful response
        success : function(response) {
            $('#alert-absolute-div').html('');
            $(old_dom).replaceWith($(response).find(new_dom));
        },
        // handle a non-successful response
        error : function() {
            $('#alert-absolute-div').html(
              '<div class="alert alert-danger text-center"><strong>Uh oh!</strong> Something went wrong on our side. <strong>Please try again later.</strong><button type="button" class="close" data-dismiss="alert">×</button></div>'
            )
            $('html, body').animate({ scrollTop: 0 }, 'fast');
        }
    });
}
