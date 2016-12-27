$(function() {
      $(".post-collapse").click( function() {
        // find status of post to be collapsed
        var isCollapsed = $(this).closest('.panel-post').find('.post-content').hasClass('hidden');

        // change direction of glyphs
        $(this).closest('.post').find('i').each(function() {
          if (isCollapsed && $(this).hasClass('fa-angle-double-down')) {
              $(this).parent().html('<i class="fa fa-angle-double-up fa-fw"></i> Collapse');

          } else if (!isCollapsed && $(this).hasClass('fa-angle-double-up')) {
            $(this).parent().html('<i class="fa fa-angle-double-down fa-fw"></i> Expand');
          }
        });

        // collapse comments
        $(this).closest('.post').find('.post-content').each(function() {
          if (isCollapsed && $(this).hasClass('hidden')) {
              $(this).removeClass('hidden');
          } else if (!isCollapsed && !($(this).hasClass('hidden'))) {
              $(this).addClass('hidden');
          }
        });

        // toggle border-top of collapsed comments
        $(this).closest('.post').find('.panel-footer').each(function() {
          if (isCollapsed && $(this).hasClass('footer-no-border')) {
              $(this).removeClass('footer-no-border');
          } else if (!isCollapsed && !($(this).hasClass('footer-no-border'))) {
              $(this).addClass('footer-no-border');
          }
        });

      });
});
