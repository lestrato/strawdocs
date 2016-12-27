$(function() {

    function mce_init() {
      tinymce.init({
        selector: 'textarea',
        height: 100,
        theme: 'modern',
        removed_menuitems: 'newdocument',
        plugins: [
          'advlist autolink lists link image charmap preview hr',
          'searchreplace code eqneditor',
          'insertdatetime save table contextmenu directionality',
          'paste textpattern imagetools'
        ],
        toolbar1: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image eqneditor',
       });
    }

    $(document).on('click', '.btn-reply', function(e) {
      // if the reply post already exists
      if ($(this).closest('.row-fluid').siblings(".reply-content").length == 1) {
        // do nothing
        console.log('already exists post reply');

      } else {
        //otherwise
          console.log('new post reply');
          var parentPanelCol = $(this).closest('.panel').parent().prop('className');
          var parentPanelColVal = parseInt(parentPanelCol.substring(7,parentPanelCol.length));
          var newPanelCol = 'col-xs-'.concat((parentPanelColVal-1).toString());
          var newPanelOffset = 'col-xs-offset-'.concat((37 - parentPanelColVal).toString());
          //console.log(newPanelCol, newPanelOffset);
          // add new blank reply
          $(this).closest('.row-fluid').after('<div class="reply-content"><hr class="hr-dotted">'+
            '<textarea></textarea>'+

            '<div class="row-fluid clearfix" style="margin-top: 10px;">'+
              '<button type="submit" class="btn btn-xs btn-default btn-cancel pull-left">'+
                'Cancel'+
              '</button>'+
              '<button type="submit" class="btn btn-xs btn-success pull-right">'+
                'Post'+
              '</button>'+
            '</div></div>');

          mce_init();

      }

    });

    $(document).on('click', '.btn-cancel', function(e) {
      e.preventDefault();
      $(this).closest('.reply-content').remove();
    });

    $(document).on('click', '.btn-answer-cancel', function(e) {
      $(this).closest('.post').remove();
      $(".btn-answer").toggleClass('hidden');
    });

    $(document).on('click', '.btn-answer', function(e) {
      $(".btn-answer").toggleClass('hidden');
      // if the reply post already exists
       if ($('#answers').find('.answer-post').length == 1) {
        // do nothing
        console.log('answer dialog already exists');
       } else {
        console.log('new answer');
        // add new blank reply
        $('#answers').append('<div class="post answer-post">'+
          '<div class="row">'+
            '<div class="col-xs-36">'+
              '<div class="panel panel-default panel-post">'+
                '<div class="panel-body">'+
                    '<textarea>'+
                    '</textarea>'+
                '</div>'+
                '<div class="panel-footer clearfix">'+
                  '<button type="submit" class="btn btn-xs btn-default btn-answer-cancel pull-left">'+
                    'Cancel'+
                  '</button>'+
                  '<button type="submit" class="btn btn-xs btn-success pull-right">'+
                    'Post'+
                  '</button>'+
                '</div>'+
              '</div>'+
            '</div>'+
          '</div><br>'+
        '</div>');
      }
      mce_init();

  });
});
