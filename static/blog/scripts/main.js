var STATIC_URL = "/static";

$(function() {
    Metronic.init(); // init metronic core components
    Layout.init(); // init current layout
    Demo.init(); // init demo features
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "positionClass": "toast-top-right",
        "onclick": null,
        "showDuration": "1000",
        "hideDuration": "1000",
        "timeOut": "3000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
});
function active_sidebar(menu, submenu){
    $(".page-sidebar-menu li").removeClass('active open');
    if (menu != null) {
        $(".page-sidebar-menu " + menu).addClass('active open');
    }
    if (submenu != null) {
        $(".page-sidebar-menu "+ menu + " " + submenu).addClass('active')
    }
}

function static_url(url) {
    return STATIC_URL + url;
}

function get_cookie(cookie_key) {
    return $.cookie(cookie_key);
}

function xsrf_token() {
    return get_cookie("_xsrf");
}

function xsrf_token_header() {
    return {
        "X-Xsrftoken": xsrf_token(),
    }
}