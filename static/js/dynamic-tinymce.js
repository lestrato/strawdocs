var questionTotal = 1;

function create_tinymce(post_type, slug) {
  if (post_type == 'reply') {
    cancel_btn_name = 'btn-cancel-reply';
    submit_btn_name = 'createReplySubmit';
  } else {
    cancel_btn_name = 'btn-cancel-edit';
    submit_btn_name = 'editPostSubmit';
  }

  new_tinymce = '<div class="reply-content row-fluid">'+
  "<form method='POST' style='display: inline'>{% csrf_token %}" +
  '<textarea name="content" id="'+textareaId+'"></textarea>'+
  '<div class="row-fluid clearfix">'+
  '<button type=button class="btn btn-sm btn-default ' + cancel_btn_name +' pull-left" style="margin-top: 10px;">'+
  'Cancel'+
  '</button>'+
  '<button value='+slug+' name='+submit_btn_name+' onclick="tinyMCE.triggerSave(); removeRequired();" type="submit" class="btn btn-sm btn-success pull-right" style="margin-top: 10px;">'+
  'Save changes'+
  '</button>'+
  '</div>'+
  '</form>' +
  '</div>';

  return new_tinymce
}

/* FOR QUESTION AND ANSWER EDITING */
$(document).on('click', '.edit-comment', function(e) {
    questionTotal += 1;
    textareaId = "mceId"+questionTotal;
    slug = $(this).siblings('.slug').val()
    closest_editable =  $(this).closest('.editable-comment');
    $(closest_editable).after(create_tinymce('non-reply', slug));

    tinymce.EditorManager.execCommand('mceAddEditor', true, textareaId);
    // populate it with existing content
    tinyMCE.get( textareaId).setContent($(closest_editable).find('.rich-text').html());
    $(closest_editable).hide();

});

$(document).on('click', '.btn-cancel-edit', function(e) {
  $(this).closest('.parent-post').find('.editable-comment').show();

  tinymce.EditorManager.execCommand('mceRemoveEditor',true, $(this).closest('.parent-post').find('textarea').attr('id'));
  $(this).closest('.reply-content').remove();
});

/* FOR REPLIES */
$(document).on('click', '.add-comment', function(e) {
    questionTotal += 1;
    textareaId = "mceId"+questionTotal;
    slug = $(this).siblings('.slug').val()
    // add new blank reply
    $(this).closest('.replies').append(create_tinymce('reply', slug));

    tinymce.EditorManager.execCommand('mceAddEditor', true, textareaId);
    $(this).hide();

});

$(document).on('click', '.btn-cancel-reply', function(e) {
  $(this).closest('.replies').find('.add-comment').show();

  tinymce.EditorManager.execCommand('mceRemoveEditor',true, $(this).closest('.reply-content').find('textarea').attr('id'));
  $(this).closest('.reply-content').remove();
});
