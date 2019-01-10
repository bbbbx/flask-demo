$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip({
        delay: { "show": 500, "hide": 0 },
        title: render_time
    });
});
