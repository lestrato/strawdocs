$(function() {

    $(document).on('click', '.btn-question-cancel', function(e) {
      $(this).closest('.question').remove();
      $(".btn-question-add").toggleClass('hidden');
    });

    $(document).on('click', '.btn-question-add', function(e) {
      $(".btn-question-add").toggleClass('hidden');
      // if the reply post already exists
       if ($('#question-group').children().length == 1) {
        // do nothing
       } else {

        // add new blank question with remove button
        $('<div class="question">'+
            '<div class="row-fluid">'  +
              '<div class="panel panel-default box-shadow">' +
                '<div class="panel-heading" style="padding-top: 2px; padding-bottom: 2px;">' +
                  '<div class="input-group">' +
                    '<input type="text" class="form-control question-title-input" placeholder="Question Title" maxlength="30" area-describedby="basic-addon2">' +
                  '</div>' +
                '</div>' +
                '<div class="panel-body">' +
                  '<div class="question-content">' +
                    '<textarea></textarea>' +
                  '</div>' +
                '</div>' +
                '<div class="panel-footer clearfix">'+
                  '<button type="submit" class="btn btn-xs btn-default btn-question-cancel pull-left">'+
                    'Cancel'+
                  '</button>'+
                  '<button type="submit" class="btn btn-xs btn-success pull-right">'+
                    'Add'+
                  '</button>'+
                '</div>'+
              '</div>' +
            '</div>' +
          '</div>').appendTo( "#question-group" );

      }
      mce_init();

  });
});
