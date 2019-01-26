
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

function displayDashboard() {
    var all_count = $('.item').length;
    if (all_count === 0) {
        $('#dashboard').hide();
    } else {
        $('#dashboard').show();
        $('ul.tabs').tabs();
    }
}

function activeM() {
    $('.sidenav').sidenav();
    $('ul.tabs').tabs();
    $('.modal').modal();
    $('.tooltipped').tooltip();
    $('.dropdown-trigger').dropdown({
            constrainWidth: false,
            coverTrigger: false
        }
    );
    displayDashboard();
}

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

function newItem(e) {
    var $input = $('#item-input');
    var value = $input.val().trim();
    if (e.which !== ENTER_KEY || !value) {
        return;     // 如果没有按下 Enter 键或输入为空，则直接返回
    }
    $input.focus().val('')
    $.ajax({
        type: 'POST',
        url: newItemUrl,
        data: JSON.stringify({ "body": value }),
        // 如果没有指定，默认为 application/x-www-form-urlencodeed，即以表单的类型
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
            M.toast({ html: data.message, classes: 'rounded' });
            $('.items').append(data.html);
            activeM();          // 激活新插入 HTML 的 Meterialize 组件
            refresh_count();    // 更新页面上的各个计数
        }
    })
}

$(document).on('keydown', '#item-input', newItem.bind(this));

activeM();     // 初始化 Materialize