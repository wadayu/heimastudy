$(document).ready(function(){
    $(".auth-warn").show();
    // 验证用户是否实名制
    $.get('/api/v1.0/user/real_name_auth',function (data) {
        if (data.errno == '0'){
            if (data.data.real_name && data.data.id_cart){
                $('#user_auth').hide();
            } else{
                $('#new_house').hide()
            }
        }else{
            alert(data.errmsg)
        }
    });

    // 获取用户发布的房源
    $.get('/api/v1.0/user/houses',function (data) {
        if (data.errno == '0'){
            var content = template('user_houses',{houses:data.data});
            $('#houses-list li').eq(1).html(content)
        }else{
            alert(data.errmsg)
        }
    })
})