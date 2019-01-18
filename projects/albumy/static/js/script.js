$('#confirm-delete').on('show.bs.modal', function(e) {
    console.log($(e.relatedTarget).data('href'))
    $('.delete-form').attr('action', $(e.relatedTarget).data('href'))  // 修改 <form> 的 action 为 <button> 的 data-href
});
