$('#confirm-delete').on('show.bs.modal', function(e) {
    // 修改 <form> 的 action 为 <button> 的 data-href
    $('.delete-form').attr('action', $(e.relatedTarget).data('href'));
});

$('#description-btn').click(function() {
    $('#description').hide();
    $('#description-form').show();
});

$('#cancel-description').click(function() {
    $('#description-form').hide();
    $('#description').show();
});

$('#tag-btn').click(function() {
    $('#tags').hide();
    $('#tag-form').show();
});

$('#cancel-tag').click(function() {
    $('#tag-form').hide();
    $('#tags').show();
});

var hoverTimer = null;
var flash = null;

function toast(body) {
    clearTimeout(flash);  // 清除未完成的计时
    var $toast = $('#toast');
    $toast.text(body).fadeIn();  // 淡入
    flash = setTimeout(function() {
        $toast.fadeOut();   // 3 秒后淡出
    }, 3000);
}

function show_profile_popover(e) {
    var $el = $(e.target);

    hoverTimer = setTimeout(function() {
        hoverTimer = null;
        $.ajax({
            type: 'GET',
            url: $el.data('href'),
            success: function(data) {
                // https://getbootstrap.com/docs/4.2/components/popovers/#usage
                $el.popover({
                    html: true,
                    content: data,
                    trigger: 'manual',
                    animation: false
                });
                $el.popover('show');
                $('.popover').on('mouseleave', function() {
                    setTimeout(function() {
                        $el.popover('hide');
                    }, 200);
                });
            },
            error: function(error) {
                toast('服务器出错，请稍后再试。');
            }
        });
    }, 500);
}

function hide_profile_popover(e) {
    var $el = $(e.target);

    if (hoverTimer) {
        clearTimeout(hoverTimer);
        hoverTimer = null;
    } else {
        setTimeout(function() {
            if (!$('.popover:hover').length) {
                $el.popover('hide');
            }
        }, 200);
    }
}

$('.profile-popover').hover(show_profile_popover.bind(this), hide_profile_popover.bind(this));
