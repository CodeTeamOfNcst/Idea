 $(function () {
            $(".block").slice(0, 12).show();
           if($(".block").length <= 12) {
           $(".more").hide();
           }
            $(".more").on('click', function (e) {
              
              if ($(".block:hidden").length == 0) {
               $(".more").css('display', 'none');
              }
                e.preventDefault();
                $(".block:hidden").slice(0, 4).slideDown();
                if ($(".block:hidden").length == 0) {
                    $(".more").fadeOut('slow');
                }
            });
        });


$(function () {

$.cookie("user",3)

userId = $.cookie("user")
		
$(".follow").click(function(){
   Id = $(this).attr("creation")
   $.post("attend",{userId:userId,attendType:"1",Id:Id},function(data){
    if(data == 1)
    	alert("感谢关注")
    else if(data == 0)
    	alert("操作失败")
    else
      alert("取消关注")
    location.reload()

})

})


$(".like").click(function(){
   Id = $(this).attr("creation")
   $.post("star",{userId:userId,starType:"1",Id:Id},function(data){
    if(data == 1)
    	alert("感谢您的点赞")
    else if(data == 0)
    	alert("操作失败")
    else 
      alert("取消点赞")
    location.reload()
})

})



})

