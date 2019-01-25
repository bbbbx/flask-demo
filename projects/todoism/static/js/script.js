
$(window).on('hashchange', function() {
    // 有些浏览器不返回 #，这里统一去掉 #
    var hash = window.location.hash.replace('#', '');
    var url = null;
    
    if (hash === 'login') {
        url = loginPageUrl;
    } else if (hash === 'app') {
        url = appPageUrl;
    } else {
        url = introPageUrl;
    }

    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            $('#main').hide().html(data).fadeIn(800);   // 插入子页面
            activeM();     // 激活新插入的页面中的 Materialize 组件
        }
    })
});

if (window.location.hash === '') {
    window.location.hash = '#intro';
} else {
    $(window).trigger('hashchange');   // 触发 hashchange 事件
}

$(document).ajaxError(function(e, request, settings) {
    if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
        message = request.responseJSON.message;
    } else {
        message = DEFAULT_ERROR_MESSAGE;    // 使用默认错误消息
    }
    M.toast({ html: message, classes: 'red accent-4 grey-text text-lighten-5 rounded' });

});

function register() {
    $.ajax({
        type: 'GET',
        url: registerUrl,
        success: function(data) {
            $('#username-input').val(data.username);   // 将用户名插入用户名字段
            $('#password-input').val(data.password);
            M.toast({html: data.message});   // 弹出提示消息
        }
    })
}