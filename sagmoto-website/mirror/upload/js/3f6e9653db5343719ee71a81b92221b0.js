$(function () {
    var isNameVideo = $(".isName").prev().find(".s_list").children().children();
    var isNameBoxA = $(isNameVideo).is(".p_list");
    var isNameBoxB = $(isNameVideo).is(".p_rollContainer");
    var videoListC = $(".isName").parent();

    $('.p_video .cover').click(function () {
        if (isNameBoxA) {
            console.log("列表")
            let videoBox = $(this).next().html();
            $("body").append("<div class='videoBox show'>" + videoBox + "</div>");
          
            let video = $("body").children(".videoBox").find('.video')[0];
            $(video).attr('playsinline','true');
            $(video).attr('webkit-playsinline','true');
            if(video.paused == true){
                video.play();
            }else{
                video.pause();
            }

            // 关闭视频
            $("body > .videoBox > .closeVideo").click(function () {
                $(this).parent().remove();
            });
        }
    });

    $(videoListC).on("click", ".p_rollSlide", function () {
            console.log("滚动列表")

            // 轮播视频
            let videoBox = $(this).find(".videoBox").html();
            $("body").append("<div class='videoBox show'>" + videoBox + "</div>");
      
            let video = $("body").children(".videoBox").find('.video')[0];
            $(video).attr('playsinline','true');
            $(video).attr('webkit-playsinline','true');
            if(video.paused == true){
                video.play();
            }else{
                video.pause();
            }

            $("body > .videoBox > .closeVideo").click(function () {
                $(this).parent().remove();
            });
    });
  
  	$('.videoIBox').each(function(){
  		let videoImgHref = $(this).find('.videoimg img').attr('src');
  		$(this).find('.coverImage img').attr('src',videoImgHref);
  	}); 
});