var blog_class_table = null;
var blog_subclass_table = null;

var selected_blog_class = null;
var selected_blog_subclass = null;


$(function() {
    active_sidebar("#blog-management", "#blog-class");
    
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
        "iDisplayLength": 10,
        "aoColumns": [
            {"mData": "name", "sWidth": "20%", "bSearchable": true, "bSortable": false, "mRender": function (data, type, row ){
                return  '<span id="class_$id_name" class="label label-success">'.replace('$id', row.id) + data + '</span>';
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
                var edit_action = '<a href="javascript:;" class="btn default btn-xs blue">  \
                                    <i class="fa fa-pencil-square-o"></i> 编辑 </a>';
                var delete_action = '<a href="javascript:;" class="btn default btn-xs red" onclick="on_delete_blog_class(\'$id\')"> \
                                    <i class="fa fa-trash-o"></i> 删除 </a>'.replace("$id", row.id);
                var actions = edit_action + delete_action;
                return actions;
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
                return  '<span id="subclass_$id_name" class="label label-success">'.replace('$id', row.id) + data + '</span>';;
            }},
            {"mData": "description", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "cls", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "protected", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                if (data) {
                    return '<span class="label label-success"> 隐藏 </span>';
                } else {
                    return '<span class="label label-danger"> 公开 </span>';
                }
            }},
            {"mData": "blogs_num", "sWidth": "10%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ){
                return data;
            }},
            {"mData": "id", "sWidth": "20%", "bSearchable": false, "bSortable": false, "mRender": function (data, type, row ) {
                var edit_action = '<a href="javascript:;" class="btn default btn-xs blue">  \
                                    <i class="fa fa-pencil-square-o"></i> 编辑 </a>';
                var delete_action = '<a href="javascript:;" class="btn default btn-xs red" onclick="on_delete_blog_subclass(\'$id\')"> \
                                    <i class="fa fa-trash-o"></i> 删除 </a>'.replace("$id", row.id);
                var actions = edit_action + delete_action;
                return actions;
            }},
        ],
        "aaSorting": [[1, 'desc']],
    });

    $('#tab_class_nav').click(function() {
        if (blog_class_table) {
            blog_class_table.fnDraw(true);
        }
    });
    
    $('#tab_subclass_nav').click(function() {
        if (blog_subclass_table) {
            blog_subclass_table.fnDraw(true);
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
    
    $('#add-subclass-form').validate({
        errorElement: 'span',
        errorClass: 'help-block',
        focusInvalid: false,
        rules: {
            name: {
                required: true
            },
            "class": {
                required: true
            },
            "protected": {
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
            "class": {
                required: "请选择所属大类"
            },
            "protected": {
                required: "请选择属性"
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
    
    $("#add_subclass_class_select").select2({
        ajax: {
            url: "/api/blog_classes",
            type: 'GET',
            data: function (term) {
                return {search: term};
            },
            results: function (data) {
                return {
                    results: $.map(data.blog_classes, function (item) {
                        return {
                            id: item.id,
                            text: item.name
                        }
                    })
                };
            }
        }
    });
    
    $("#add_class_btn").click(function() {
        $("#add-class-form").validate().resetForm();
        $("#add-class-dialog").modal("show");
    });
    
    $("#add_subclass_btn").click(function() {
        $("#add-subclass-form").validate().resetForm();
        $("#add_subclass_class_select").select2("val", "");
        $("#add-subclass-dialog").modal("show");
    });
    
    $("#confirm-add-class").click(function() {
        add_blog_class();
    });
    
    $("#confirm-add-subclass").click(function() {
        add_blog_subclass();
    });
    
    $("#confirm-delete-subclass").click(function() {
        delete_blog_subclass();
    });
    
    $("#confirm-delete-class").click(function() {
        delete_blog_class();
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
                blog_class_table.fnDraw(true);
            },
            error: function (request, status, error) {
                var error = request.responseJSON.error;
                toastr.error(error.message, error.code);
            }
        });
    }
}

function convert_radio_bool_value(value) {
    if (typeof value === "string") {
        if (value.toLowerCase() === "true")
            return true;
        else if (value.toLowerCase() === "false")
            return false;
    }
    throw "unknown radio bool value";
}

function add_blog_subclass() {
    if ($("#add-subclass-form").valid()) {
        $("#add-subclass-dialog").modal("hide");
        $.ajax({
            url: "/api/blog_subclasses",
            type: "POST",
            contentType: "application/json",
            dataType: "json",
            headers: xsrf_token_header(),
            data: 
                JSON.stringify({
                    "blog_subclass": {
                        "name": $("#add_subclass_name_input").val(),
                        "class_id": $('#add_subclass_class_select').val(),
                        "description": $("#add_subclass_desc_input").val(),
                        "protected": convert_radio_bool_value(
                            $("#add-subclass-form input[type='radio'][name='protected']:checked").val())
                    }
            }),
            success: function (responseJson) {
                toastr.info("成功添加小类", "");
                blog_subclass_table.fnDraw(true);
            },
            error: function (request, status, error) {
                var error = request.responseJSON.error;
                toastr.error(error.message, error.code);
            }
        });
    }
}

function delete_blog_class() {
    $("#delete-class-dialog").modal("hide");
    if (selected_blog_class == null) {
        toastr.error("请选择待删除的大类", "删除大类");
    } else {
        $.ajax({
            url: "/api/blog_classes/" + selected_blog_class,
            type: "DELETE",
            dataType: "json",
            headers: xsrf_token_header(),
            success: function (responseJson) {
                toastr.info("成功删除大类", "");
                blog_class_table.fnDraw();
            },
            error: function (request, status, error) {
                var error = request.responseJSON.error;
                if (error.status == 404) {
                    toastr.info("成功删除大类", "");
                    blog_class_table.fnDraw();
                }
                else {
                    toastr.error(error.message, error.code);
                }
            }
        });
    }
}

function delete_blog_subclass() {
    $("#delete-subclass-dialog").modal("hide");
    if (selected_blog_subclass == null) {
        toastr.error("请选择待删除的小类", "删除小类");
    } else {
        $.ajax({
            url: "/api/blog_subclasses/" + selected_blog_subclass,
            type: "DELETE",
            dataType: "json",
            headers: xsrf_token_header(),
            success: function (responseJson) {
                toastr.info("成功删除小类", "");
                blog_subclass_table.fnDraw();
            },
            error: function (request, status, error) {
                var error = request.responseJSON.error;
                if (error.status == 404) {
                    toastr.info("成功删除小类", "");
                    blog_subclass_table.fnDraw();
                }
                else {
                    toastr.error(error.message, error.code);
                }
            }
        });
    }
}

function on_delete_blog_class(id) {
    selected_blog_class = id;
    var name = $("#class_$id_name".replace("$id", id)).text();
    name = $.trim(name);
    $("#delete-class-dialog-prompt").html('<b>确认删除博文大类"$name"吗</b>'.replace("$name", name));
    $("#delete-class-dialog").modal("show");
}

function on_delete_blog_subclass(id) {
    selected_blog_subclass = id;
    var name = $("#subclass_$id_name".replace("$id", id)).text();
    name = $.trim(name);
    $("#delete-subclass-dialog-prompt").html('<b>确认删除博文小类"$name"吗</b>'.replace("$name", name));
    $("#delete-subclass-dialog").modal("show");
}