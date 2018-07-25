/**
 * Created by jsb-yw02 on 2018/7/16.
 */
$(function () {
    //获取slide li标签的数量
    var $li = $('.slide li');
    //小圆点ul标签
    var $points = $('.points');
    //要运动过来的幻灯片的索引值
    var $nowli = 0;
    //要离开的幻灯片索引值
    var $prevli = 0;

    var ismove = false;

    var $prev = $('.prev'); //往right按钮
    var $next = $('.next'); //往left按钮

    //定时器
    var timer = null;

    //添加小圆点
    for (i=0;i<$li.length;i++){
        var $newli = $('<li>');
        if (i==0){
            $newli.addClass('active')
        }
        $newli.appendTo($points);
    }

    //第一个幻灯片不动，将其他的幻灯片放到右边去
    $li.not(':first').css({'left':760});

    //获取小圆点li
    var $points_li = $('.points li');

    $points_li.click(function () {
        $nowli = $(this).index();
        if($nowli==$prevli){ //修复重复点击的bug
            return;
        }
        $(this).addClass('active').siblings().removeClass('active');
        move();
    });

    //向前切换
    $prev.click(function () {
        if(ismove){
            return;
        }
        ismove = true;
        $nowli--;
        move();
        $points_li.eq($nowli).addClass('active').siblings().removeClass('active')
    });

    //向后切换
    $next.click(function () {
         if(ismove){
            return;
        }
        ismove = true;
        $nowli++;
        move();
        $points_li.eq($nowli).addClass('active').siblings().removeClass('active')
    });

    timer = setInterval(autoplay,1000);

    $('.slide_con').hover(function () {
        clearInterval(timer)
    },function () {
        timer = setInterval(autoplay,1000);
    });

    function autoplay() {
        $nowli++;
        move();
        $points_li.eq($nowli).addClass('active').siblings().removeClass('active')
    }

    function move() {
        if ($nowli<0){
            $nowli = $li.length-1;
            $prevli=0;
            $li.eq($nowli).css({'left': -760});
            $li.eq($prevli).animate({'left': 760});
            $li.eq($nowli).animate({'left': 0},function () {
                ismove=false;
            });
            $prevli = $nowli;
            return; //执行完之后不再执行后面的内容
        }

           if ($nowli>$li.length-1){
            $nowli = 0;
            $prevli=$li.length-1;
            $li.eq($nowli).css({'left': 760});
            $li.eq($prevli).animate({'left': -760});
            $li.eq($nowli).animate({'left': 0},function () {
                ismove=false;
            });
            $prevli = $nowli;
            return; //执行完之后不再执行后面的内容
        }


        if ($nowli > $prevli) {  //幻灯片从右边移过来
            $li.eq($nowli).css({'left': 760});
            $li.eq($prevli).animate({'left': -760});
        }
        else { //幻灯片从左边移过来
            $li.eq($nowli).css({'left': -760});
            $li.eq($prevli).animate({'left': 760});
        }

        $li.eq($nowli).animate({'left': 0},function () {
            ismove=false;
        });
        $prevli = $nowli;

    }
});