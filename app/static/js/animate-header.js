$(window).scroll(function() {    
    var scroll = $(window).scrollTop();

    if (scroll >= 220) {
        $(".avatar").addClass("avatar-shrink")
        $(".header").addClass("header-shrink")
        $(".site-title").addClass("site-title-shrink")
        $(".navbar-default").addClass("navbar-shrink");
    } else {
        $(".avatar").removeClass("avatar-shrink")
        $(".header").removeClass("header-shrink")
        $(".site-title").removeClass("site-title-shrink")
        $(".navbar-default").removeClass("navbar-shrink");
    }
});