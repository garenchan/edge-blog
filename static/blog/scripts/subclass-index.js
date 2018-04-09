$(function() {
    _active_sidebar();
});

function _active_sidebar() {
    var pathname = window.location.pathname;
    var subclass_id = pathname.split("/").slice(-1)[0];
    var submenu = $("#subclass_" + subclass_id);
    var menu = submenu.parent().parent();
    $(".page-sidebar-menu li").removeClass('active open');
    menu.addClass('active open');
    menu.find(".arrow").addClass('open');
    submenu.addClass('active')
}