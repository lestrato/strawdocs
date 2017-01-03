$( ".replies" ).each(function() {
  if ($(this).children(".row-fluid").length > 5) {
    // get count ofo number of children
    var replyNumber = $(this).children(".row-fluid").length - 5;
    // hide the other elements
    $(this).children(":gt(9)").hide();

    // create new expand button
    $(this).append("<a class='show-comments'>show <b>"+replyNumber+"</b> more comments </a>");
  }
});

$(function() {
  $(document).on('click', '.show-comments', function() {
    $(this).parent().children(":gt(9)").show();
    $(this).remove();
  });
});
