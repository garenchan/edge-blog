$(function() {
    _active_sidebar();
});

function _active_sidebar() {
    var pathname = window.location.pathname;
    pathname = pathname.split("/");
    var subclass_id = pathname.slice(-2)[0];
    var submenu = $("#subclass_" + subclass_id);
    var menu = submenu.parent().parent();
    $(".page-sidebar-menu li").removeClass('active open');
    menu.addClass('active open');
    menu.find(".arrow").addClass('open');
    submenu.addClass('active')
}