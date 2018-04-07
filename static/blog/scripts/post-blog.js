$(function() {
    active_sidebar("#blog-management", "#blog-post");
   $("#post_blog_content_input").markdown({language: 'zh'});
    $('#post-blog-form').validate({
        errorElement: 'span',
        errorClass: 'help-block',
        focusInvalid: false,
        rules: {
            source: {
                required: true
            },
            subclass: {
                required: true
            },
            title: {
                required: true
            },
            summary: {
                required: true
            },
            content: {
                required: true
            },
        },
        messages: {
            source: {
                required: "请选择博文类型"
            },
            subclass: {
                required: "请选择博文分类"
            },
            title: {
                required: "请输入博文标题"
            },
            summary: {
                required: "请输入博文摘要"
            },
            content: {
                required: "请输入博文内容"
            },
        },
        highlight: function (element) {
            $(element)
                .closest('.form-group').addClass('has-error');
        },
        errorPlacement: function(error, element) {
            if (element.attr("name") == "content") {
                error.insertBefore(".md-editor");
            } else {
                error.insertAfter(element);
            }
        }
    });
    
    $("#post_blog_source_select").select2({
        ajax: {
            url: "/api/blog_sources",
            type: 'GET',
            data: function (term) {
                return {search: term};
            },
            results: function (data) {
                return {
                    results: $.map(data.blog_sources, function (item) {
                        return {
                            id: item.id,
                            text: item.name
                        }
                    })
                };
            }
        }
    });
    
    $("#post_blog_subclass_select").select2({
        ajax: {
            url: "/api/blog_subclasses",
            type: 'GET',
            data: function (term) {
                return {search: term};
            },
            results: function (data) {
                groups = {}
                $.map(data.blog_subclasses, function (item) {
                    cls_name = item.cls;
                    group = groups[cls_name]
                    if (!group) {
                        group = groups[cls_name] = [];
                    }
                    group.push({id: item.id, text: item.name});
                });
                results = [];
                for (var cls_name in groups) {
                    results.push({text: cls_name, children: groups[cls_name]})
                }
                return {
                    results: results
                };
            }
        }
    });
    
    $("#confirm-post-blog").click(function() {
        post_blog();
    });
});

function post_blog() {
    if ($("#post-blog-form").valid()) {
        $.ajax({
            url: "/api/blogs",
            type: "POST",
            contentType: "application/json",
            dataType: "json",
            headers: xsrf_token_header(),
            data: JSON.stringify({
                    "blog": {
                        "title": $("#post_blog_title_input").val(),
                        "summary": $("#post_blog_summary_input").val(),
                        "content": $("#post_blog_content_input").val(),
                        "source_id": $("#post_blog_source_select").val(),
                        "subclass_id": $("#post_blog_subclass_select").val()
                    }
            }),
            success: function (responseJson) {
                console.log(responseJson);
                toastr.info("成功发表博文", "");
                return false;
            },
            error: function (request, status, error) {
                var error = request.responseJSON.error;
                toastr.error(error.message, error.code);
            }
        });
    }
    return false;
}