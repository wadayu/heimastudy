function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    // 获取当前房屋的详情信息
    var house_id = decodeQuery()['id'];
    $.get('/api/v1.0/house/detail/' + house_id,function (data) {
        var content = template('house_info',{house:data.data.house_info})
        $('.house-info').append(content)
    });

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    //订单提交
    $('.submit-btn').click(function () {
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        parms = {'house_id':house_id,'sd':startDate,'ed':endDate};
        json_data = JSON.stringify(parms);

        $.ajax({
            'url':'/api/v1.0/place/order',
            'type':'post',
            'data':json_data,
            'contentType':'application/json',
            'dataType':'json',
            'headers':{'X-CSRFToken':getCookie('csrf_token')}
        }).done(function (data) {
            if (data.errno == '0'){
                location.href = '/orders.html'
            }else{
                if(data.errno == '4101'){
                    location.href = '/login.html'
                }else{
                    alert(data.errmsg)
                }
            }
        })
    })

})
