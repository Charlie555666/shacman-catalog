$require(['swiper'], function () {
    var honorSwip = new Swiper('.honorSwip', {
        effect: 'coverflow',
        slidesPerView: 3,
        loop: true,
        loopAdditionalSlides: 3,
        loopedSlides: 5,
        coverflowEffect: {
            rotate: 20,
            stretch: "50%",
            depth: 20,
            modifier: 1,
            slideShadows: true
        },
        speed: 800,
        autoplay: {
            delay: 3000
        },
        mousewheel: true,
        pagination: {
            el: '.honorSwip .swiper-pagination',
            clickable: true,
        },
        breakpoints: { 
          768: {
            slidesPerView: 5,
          }
        }
    })
});

// 图片放大
Fancybox.bind('.fancyboxIMHhonor .showihonor', {
    groupAll: true,

    Image: {
        wheel: "slide",
    },
});