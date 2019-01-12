$(function() {
    $('[data-toggle="tooltip"]').tooltip({
        title: moment($(this).data('timestamp')).format('lll')
    });
});
