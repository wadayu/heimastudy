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

    // 获取客户下自己房子的订单
    $.ajaxSettings.async = false; // 改为同步模式
    $.get('/api/v1.0/user/customer/orders',function (data) {
        if (data.errno == '0'){
            var content = template('order_lists_tmpl',{orders:data.data.all_orders});
            $('.orders-list').html(content)
        }else{
            if (data.errno == '4101') {
                location.href='/login.html'
            }else{
                alert(data.errmsg)
            }
        }
    });
    $.ajaxSettings.async = true;

    // 接单
    $(".order-accept").on('click',function(){
        var orderId = $(this).parents('li').attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    });

    $(".modal-accept").click(function () {
        var orderId = $(this).attr('order-id');
        $.ajax({
            'url':'/api/v1.0/order/status/' + orderId,
            'type':'put',
            'data':JSON.stringify({'action':'accept'}),
            'contentType':'application/json',
            'dataType':'json',
            'headers':{'X-CSRFToken':getCookie('csrf_token')},
            'success':function (data) {
                if (data.errno == '0'){
                    $('.order-operate').hide();
                    $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul>li:eq(4)>span").html('待支付');
                    $("#accept-modal").modal("hide");
                }else{
                       if (data.errno == '4101') {
                            location.href='/login.html'
                       }else{
                            alert(data.errmsg)
                       }
                }
            }
        });
    }) ;

    // 拒单
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    });


    $(".modal-reject").click(function () {
        var orderId = $(this).attr('order-id');
        var reason = $('#reject-reason').val();
        if (!reason){
            alert('原因必填')
            return false
        }
        $.ajax({
            'url':'/api/v1.0/order/status/' + orderId,
            'type':'put',
            'data':JSON.stringify({'action':'reject','reason':reason}),
            'contentType':'application/json',
            'dataType':'json',
            'headers':{'X-CSRFToken':getCookie('csrf_token')},
            'success':function (data) {
                if (data.errno == '0'){
                    $('.order-operate').hide();
                    $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul>li:eq(4)>span").html('已拒绝');
                    $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul").append("<li>拒单原因："+reason+"</li>");
                    $("#reject-modal").modal("hide");
                }else{
                    if (data.errno == '4101') {
                        location.href='/login.html'
                    }else{
                        alert(data.errmsg)
                    }
                }
            }
        });
    }) ;

});