/**
 * Created by root on 17-9-8.
 */


function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

$(document).ready(function () {
    // $('.nav_main li a').each(function () {
    //     $this = $(this);
    //     if ($this[0].href === String(window.location.href)) {
    //         $this.addClass('active');
    //     }
    // });
    $(function(){
        var navLi=$('.nav_main li a') ;//此处填写你的导航html对象
        var proAhref=$('.tag a');
        var windowUrl=String(window.location.href); //获取当前url链接
        navLi.each(function(){
            $this = $(this);
            var t = $this[0].href;
            if(t === windowUrl) {
                $(this).addClass('active');  //添加当前位置样式
            }
        });
        // proAhref.each(function(){
        //     $this = $(this);
        //     var t = $this[0].href;
        //     if(t === windowUrl) {
        //         $('.index_recruit').addClass('active');  //添加当前位置样式
        //     }
        // });
    });

    var user_img = document.getElementById('user_img');
    var username = getCookie('username');
    if (username === null || username === '') {
        var hidden_item = document.getElementById('login_status_false');
        hidden_item.style.display = '';
    } else {
        var hidden_item = document.getElementById('login_status_true');
        hidden_item.style.display = '';
        var email = $.cookie('email');
        var username = $.cookie('username');
        document.getElementById("username").innerHTML = username;
        var data = {
            'email': email,
            'username': username
        };
        $.post('/idear/getimg', {}, function (result) {
            result = JSON.parse(result);
            if (result['status'] === 1) {
                var img_path = result['img_path'];
                var message = result['message'];
                user_img.src = '/static' + img_path;
                document.getElementById('user_img').style.src= user_img.src;
            } else if (result['status'] === 0) {
                // var message = result['message'];
                // alert(message);
            } else {}
        });
    }
});

(function($){
    $.fn.typer = function(options){
        var defaults = $.extend({
            search: '',
            replace: [],
            speed: 50,
            delay: 2000
        }, options);
        var bintext = function(length){
            var text = '';
            for(var $i = 0; $i<=length;$i++) {
                text = text + Math.floor(Math.random() * 2)
            }
            return text;
        };
        this.each(function(){
            var $this = $(this);
            var $text = $this.data('text');
            var position = 0;
            var indexOf = $text.indexOf( defaults.search );
            var normal = $text.substr(0, indexOf);
            var changer = $text.substr(indexOf, $text.length);
            defaults.replace.push(changer);
            var interval = setInterval(function(){
                var $bintext = '';
                if( position === indexOf ) {
                    $bintext = bintext(changer.length-1);
                    $this.html( $text.substr(0, normal.length) );
                    $this.append('<span>' + $bintext + '</span>')
                } else if( position > indexOf ) {
                    $bintext = bintext($text.length-1);
                    $this.delay(defaults.speed).find('span').html(
                        changer.substring(0, position - indexOf) +
                        $bintext.substring(position, ($bintext.length))
                    );
                } else if( position < indexOf ) {
					$bintext = bintext($text.length-1);
                    $this.delay(defaults.speed).html(
                        normal.substring(0, position) +
                        $bintext.substring(position, ($bintext.length))
                    );
                }
                if( position < $text.length ) {
                    position++;
                } else {
                    clearInterval(interval);
                    var index = 0;
                    setInterval(function(){
                        var position = 0;
                        var newText = defaults.replace[index];
                        var changeInterval = setInterval(function(){
                            var $bintext = '';
                            for(var $i = 0; $i<=newText.length-1;$i++) {
                                $bintext = $bintext + Math.floor(Math.random() * 2)
                            }
                            $this.delay(defaults.speed).find('span').html(
                                newText.substring(0, position) +
                                $bintext.substring(position, ($bintext.length))
                            );
                            if( position < $text.length ) {
                                position++;
                            } else {
                                clearInterval(changeInterval);
                            }
                        }, defaults.speed);
                        if( index < defaults.replace.length-1 ) {
                            index++;
                        } else {
                            index = 0;
                        }
                    }, defaults.delay)
                }
            }, defaults.speed)
        });
    }
})(jQuery);

     function block() {
         document.getElementsByClassName("list_all")[0].style.display = "block";
     }
     function none() {
         document.getElementsByClassName("list_all")[0].style.display = "none";
     }



