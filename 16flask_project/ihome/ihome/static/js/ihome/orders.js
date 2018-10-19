//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });

    // 查询所有的用户订单
    $.ajaxSettings.async = false; // 启用同步模式
    $.get('/api/v1.0/user/orders',function (data) {
        if (data.errno == '0'){
            var content = template('orders-list-tmpl',{orders:data.data.all_orders});
            $('.orders-list').append(content)
        }else{
            if (data.errno == '4101'){
                location.href='/login.html'
            }else{
                alert(data.errmsg)
            }
        }
    });
    $.ajaxSettings.async = true; // 启用异步模式

    // 提交用户的评论信息
    $('#wait_comment').click(function () {
        var orderId = $(this).attr('order_id');
        $('.modal-comment').attr('order_id',orderId)
    });

    $('.modal-comment').click(function () {
        var orderId = $(this).attr('order_id');
        var comment = $('#comment').val();
        if (!comment){
            alert('评价信息不能为空！');
            return false
        }
        $.ajax({
            'url': '/api/v1.0/order/comment/' + orderId,
            'type': 'put',
            'data':JSON.stringify({'comment':comment}),
            'contentType':'application/json',
            'dataType':'json',
            'headers':{'X-CSRFToken':getCookie('csrf_token')},
            'success':function (data) {
                if (data.errno == '0'){
                    $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul>li:eq(4)>span").html('已完成');
                    $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul").append("<li>我的评价：" + comment + "</li>");
                    $("#comment-modal").modal("hide");
                }else{
                    if (data.errno == '4101') {
                        location.href='/login.html'
                    }else{
                        alert(data.errmsg)
                    }
                }
            }
        })
    });

    // 用户支付信息
    $('#wait_pay').click(function () {
        var orderId = $(this).attr('order_id');
        $.ajax({
            'url':'/api/v1.0/order/pay',
            'type':'post',
            'data':JSON.stringify({'order_id':orderId}),
            'contentType':'application/json',
            'dataType':'json',
            'headers':{'X-CSRFToken':getCookie('csrt_token')},
            'success':function (data) {
                if (data.errno == '0'){
                    location.href = data.data.pay_url
                }else{
                    if (data.errno == '4101') {
                        location.href='/login.html'
                    }else{
                        alert(data.errmsg)
                    }
                }
            }
        })
    })

});