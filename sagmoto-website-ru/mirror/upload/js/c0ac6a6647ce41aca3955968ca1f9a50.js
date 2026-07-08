//top fixed
$(window).scroll(function () {
    if ($(window).scrollTop() > 0) {
        $('.fIxBox').parent().addClass('active')
    } else {
        $('.fIxBox').parent().removeClass('active')
    }
})
$('.fIxBox').parent().mouseenter(function () {
    $(this).addClass('active')
}).mouseleave(function () {
    if ($(window).scrollTop() == 0) {
        $(this).removeClass('active')
    }
});

//top nav
$(function () {
    var wind_w = $(window).width();
    $('.e_navigationF-24 .p_navItem1 .sj_warp').find('.p_level3Box').parents('.p_navItem1').addClass('pro_li');
    $('.e_navigationF-24 .pro_li .dropdown .left ul .p_navItem2').eq(0).addClass('cur');
    $('.e_navigationF-24 .pro_li .dropdown .center .sj_warp ul').eq(0).addClass('pro_cur');
    if (wind_w > 768) {
        $('.e_navigationF-24 .pro_li .dropdown .left ul').on('mouseenter', 'li', function () {
            $(this).addClass('cur').siblings().removeClass('cur');
            var index = $(this).index();
            $(this).closest('.dropdown').find('.sj_warp ul').eq(index).stop().fadeIn().siblings().hide();
        })
    }

    $('.search_warp').click(function(){
        if($('.boxForm').hasClass('active')){
            $('.boxForm').removeClass('active');
        }else{
            $('.boxForm').addClass('active');
        }
     })

     $('.closeFrom').click(function(){
        $('.boxForm').removeClass('active');
    })
});