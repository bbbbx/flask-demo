$(function() {
    // 对于 POST 方法的 Ajax 需要设置 CSRF token 保护，
    // 设置在 HTTP 头部
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    function update_followers_count(id) {
        var $el = $('#followers-count-' + id);
        $.ajax({
            type: 'GET',
            url: $el.data('href'),
            success: function (data) {
                $el.text(data.count);
            }
        });
    }

    function follow(e) {
        var $el = $(e.target);
        var id = $el.data('id');

        $.ajax({
            type: 'POST',
            url: $el.data('href'),
            success: function(data) {
                $el.prev().show();
                $el.hide();
                update_followers_count(id);
                toast('关注成功。')
            }
        });
    }

    function unfollow(e) {
        var $el = $(e.target);
        var id = $el.data('id');

        $.ajax({
            type: 'POST',
            url: $el.data('href'),
            success: function(data) {
                $el.next().show();
                $el.hide();
                update_followers_count(id);
                toast('取消关注成功。')
            }
        });
    }

    var hoverTimer = null;
    var flash = null;
    
    function toast(body, category) {
        clearTimeout(flash);  // 清除未完成的计时
        var $toast = $('#toast');
        
        if (category === 'error') {
            $toast.css('background-color', 'red');   // 错误类型消息
        } else {
            $toast.css('background-color', '#333');  // 普通类型消息
        }

        $toast.text(body).fadeIn();  // 淡入
        flash = setTimeout(function() {
            $toast.fadeOut();   // 3 秒后淡出
        }, 3000);
    }

    $(document).on('click', '.follow-btn', follow.bind(this));
    $(document).on('click', '.unfollow-btn', unfollow.bind(this));
    $(document).ajaxError(function(event, request, settings) {  // 同一处理 ajax 的 error 回调
        if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
            message = request.responseJSON.message;
        } else if (request.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(request.responseText);   // 作为 JSON 解析
            } catch (err) {
                IS_JSON = false;
            }

            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(request.responseText).message;
            } else {
                message = DEFAULT_ERROR_MESSAGE;    // 使用默认错误消息
            }
        } else {
            message = DEFAULT_ERROR_MESSAGE;    // 使用默认错误消息
        }
        toast(message, 'error')
    })

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
    
    $("[data-toggle='tooltip']").tooltip({
        title: moment($(this).data('timestamp')).format('LL')
    });
})