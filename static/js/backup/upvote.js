success : function(response) {
  if (response.constructor == {}.constructor) {
     // some error message TODO: maybe there's a more delicate way to do this
      $.each( response, function( key, value ) {
        $('#error_div').html('<div class="alert alert-danger">'+value+'</div>');
      });
  } else {
      // change the values of the buttons
      $(self).closest('.btn-group').find('button').each( function() {
        count_div = $(this).find('div');
        if ($(this).hasClass('btn-success') || $(this).hasClass('btn-danger')) {
          curr_vote_count = parseInt($(count_div).text());
          $(count_div).text((curr_vote_count - 1).toString() + ' ');
        }
        $(this).removeClass('btn-default');
        $(this).removeClass('btn-success');
        $(this).removeClass('btn-danger');
        $(this).addClass('btn-default');
      });
      // color the right button and change the value of the pressed button
      button = $(self).find('button');
      count_div = $(button).find('div');
      if (response == 'upvote' || response == 'downvote') {
        $(button).removeClass('btn-default');
        curr_vote_count = parseInt($(count_div).text());
        $(count_div).text((curr_vote_count + 1).toString() + ' ');
        if (response == 'upvote'){ $(button).addClass('btn-success'); }
        else if (response == 'downvote') { $(button).addClass('btn-danger'); }
      }
  }
},
