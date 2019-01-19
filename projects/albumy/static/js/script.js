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
