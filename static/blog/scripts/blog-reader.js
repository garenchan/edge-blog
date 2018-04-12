$(function() {
    _active_sidebar();
    render_markdown_to_html();
});

function _active_sidebar() {
    var subclass_id = $("#subclass-id").val();
    var submenu = $("#subclass_" + subclass_id);
    var menu = submenu.parent().parent();
    $(".page-sidebar-menu li").removeClass('active open');
    menu.addClass('active open');
    menu.find(".arrow").addClass('open');
    submenu.addClass('active');
}

function render_markdown_to_html() {
    var content = $(".blog-content").text();
    $('.blog-content').html(markdown.toHTML(content));
    codeHighLight();
}