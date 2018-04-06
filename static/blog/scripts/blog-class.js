var blog_class_table = null;
var blog_subclass_table = null;

$(function() {
    active_sidebar("#blog-management", "#blog-class");
    $('.bs-select').selectpicker({
        iconBase: 'fa',
        tickIcon: 'fa-check'
    });
    
    blog_class_table = $('#blog_class_table').dataTable({
        "bServerSide": true,
        "bProcessing": true,
        "sAjaxSource": "/api/blog_classes",
        "language": {
           url: static_url('/blog/i18n/jquery.dataTables.json')
        },
        "lengthMenu": [
            [10, 25, 50, 100],
            [10, 25, 50, 100],
        ],
        "pageLength": 10,
        "aoColumns": [
            {"mData": "name", "sWidth": "20%", "bSearchable": true, "bSortable": false, "mRender": function (data, type, row ){
                return  '<span class="label label-success">' + data + '</span>';
            }},
            {"mData": "subclasses", "sWidth": "30%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "description", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "order", "sWidth": "10%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "id", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ) {
                return  '<a href="javascript:;" class="btn default btn-xs blue"> \
                                    <i class="fa fa-pencil-square-o"></i> 编辑 </a>'
                        + '<a href="javascript:;" class="btn default btn-xs red" onclick=""> \
                                    <i class="fa fa-trash-o"></i> 删除 </a>';
            }},
        ],
        "aaSorting": [[3, 'desc']],
    });
    
    blog_subclass_table = $('#blog_subclass_table').dataTable({
        "bServerSide": true,
        "bProcessing": true,
        "sAjaxSource": "/api/blog_subclasses",
        "language": {
           url: static_url('/blog/i18n/jquery.dataTables.json')
        },
        "lengthMenu": [
            [10, 25, 50, 100],
            [10, 25, 50, 100],
        ],
        "pageLength": 10,
        "aoColumns": [
            {"mData": "name", "sWidth": "20%", "bSearchable": true, "bSortable": false, "mRender": function (data, type, row ){
                return  '<span class="label label-success">' + data + '</span>';;
            }},
            {"mData": "description", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "cls", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "protected", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                if (data) {
                    return '<span class="label label-success"> 公开 </span>';
                } else {
                    return '<span class="label label-danger"> 隐藏 </span>';
                }
            }},
            {"mData": "blogs_num", "sWidth": "10%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "id", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ) {
                return  '<a href="javascript:;" class="btn default btn-xs blue"> \
                                    <i class="fa fa-pencil-square-o"></i> 编辑 </a>'
                        + '<a href="javascript:;" class="btn default btn-xs red" onclick=""> \
                                    <i class="fa fa-trash-o"></i> 删除 </a>';
            }},
        ],
        "aaSorting": [[1, 'desc']],
    });

    $('#tab_class_nav').click(function() {
        if (blog_class_table) {
            blog_class_table.fnDraw();
        }
    });
    
    $('#tab_subclass_nav').click(function() {
        if (blog_subclass_table) {
            blog_subclass_table.fnDraw();
        }
    });
    
    $('#add-class-form').validate({
        errorElement: 'span',
        errorClass: 'help-block',
        focusInvalid: false,
        rules: {
            name: {
                required: true
            },
            description: {
                required: true
            },
        },
        messages: {
            name: {
                required: "请输入大类名称"
            },
            description: {
                required: "请输入分类简介"
            }
        },
        highlight: function (element) {
            $(element)
                .closest('.form-group').addClass('has-error');
        },
    });
    
    $("#add_class_btn").click(function() {
        $("#add-class-form").validate().resetForm();
        $("#add-class-dialog").modal("show");
    });
    
    $("#add_subclass_btn").click(function() {
        $("#add-subclass-dialog").modal("show");
    });
    
    $("#confirm-add-class").click(function() {
        add_blog_class();
    });
});

function add_blog_class() {
    if ($("#add-class-form").valid()) {
        $("#add-class-dialog").modal('hide');
        $.ajax({
            url: "/api/blog_classes",
            type: "POST",
            data: $("#add-class-form").serialize(),
            success: function (responseJson) {
                toastr.info('成功添加大类', '');
                blog_class_table.fnDraw();
            },
            error: function (request, status, error) {
                var error = request.responseJSON.error;
                toastr.error(error.message, error.code);
            }
        });
    }
}