var blog_table = null;
var selected_blog = null;

$(function() {
    active_sidebar("#blog-management", "#blogs-manage");
    
    blog_table = $("#blog_table").dataTable({
        "bServerSide": true,
        "bProcessing": true,
        "sAjaxSource": "/api/blogs",
        "language": {
           url: static_url('/blog/i18n/jquery.dataTables.json')
        },
        "lengthMenu": [
            [10, 25, 50, 100],
            [10, 25, 50, 100],
        ],
        "iDisplayLength": 10,
        "aoColumns": [
            {"mData": "title", "sWidth": "25%", "bSearchable": true, "bSortable": true, "mRender": function (data, type, row ){
                return  '<span id="blog_$id_title" title="$title" class="label label-success">'.replace('$id', row.id).replace('$title', data) + data + '</span>';
            }},
            {"mData": "source", "sWidth": "10%", "bSearchable": true, "bSortable": true, "mRender": function (data, type, row ){
                return  '<span id="blog_$id_source" class="label label-success">'.replace('$id', row.id) + data + '</span>';
            }},
            {"mData": "subclass", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "updated_at", "sWidth": "20%", "bSearchable": true, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "view_counter", "sWidth": "10%", "bSearchable": false, "bSortable": true, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "id", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ) {
                var edit_action = '<a href="javascript:;" class="btn default btn-xs blue">  \
                                    <i class="fa fa-pencil-square-o"></i> 编辑 </a>';
                var delete_action = '<a href="javascript:;" class="btn default btn-xs red" onclick="on_delete_blog(\'$id\')"> \
                                    <i class="fa fa-trash-o"></i> 删除 </a>'.replace("$id", row.id);
                var actions = edit_action + delete_action;
                return actions;
            }},
        ],
        "aaSorting": [],
    });
    
    $("#confirm-delete-blog").click(function() {
        delete_blog();
    });
});

function delete_blog() {
    $("#delete-blog-dialog").modal("hide");
    if (selected_blog == null) {
        toastr.error("请选择待删除的博文", "删除博文");
    } else {
        $.ajax({
            url: "/api/blogs/" + selected_blog,
            type: "DELETE",
            dataType: "json",
            headers: xsrf_token_header(),
            success: function (responseJson) {
                toastr.info("成功删除博文", "");
                blog_table.fnDraw();
            },
            error: function (request, status, error) {
                var error = request.responseJSON.error;
                if (error) {
                    if (error.status == 404) {
                        toastr.info("成功删除博文", "");
                        blog_table.fnDraw();
                    }
                    else {
                        toastr.error(error.message, error.code);
                    }
                } else {
                    toastr.error("未知错误, 请稍后重试！");
                }
            }
        });
    }
}

function on_delete_blog(id) {
    selected_blog = id;
    var title = $("#blog_$id_title".replace("$id", id)).text();
    title = $.trim(title);
    $("#delete-blog-dialog-prompt").html('<b>确认删除博文"$title"吗？</b>'.replace("$title", title));
    $("#delete-blog-dialog").modal("show");
}