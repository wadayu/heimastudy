function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    $.get('/api/v1.0/user/real_name_auth',function (data) {
        if (data.errno == 0){
            $('#real-name').val(data.data.real_name);
            $('#id_cart').val(data.data.id_cart);
            if (data.data.real_name && data.data.id_cart){
                $('#real-name').prop('disabled',true);
                $('#id_cart').prop('disabled',true);
                $('input[type=submit]').hide()
            }
        }else{
            if (data.errno == 4101){
                location.href = '/login.html';
                return
            }
            alert(data.errmsg)
        }
    });

    $('#real-name').focus(function () {
        $('.error-msg').hide();
    });

    $('#id_cart').focus(function () {
        $('.error-msg').hide();
    });

    //修改真实信息
    $('#form-auth').submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();

        var real_name = $('#real-name').val();
        var id_cart = $('#id_cart').val();

        if (!real_name || !id_cart){
            $('.error-msg').show();
            return
        }
        // 验证身份证
        var re = /^[1-9]\d{5}(18|19|2([0-9]))\d{2}(0[0-9]|10|11|12)([0-2][1-9]|30|31)\d{3}[0-9Xx]$/;
        if (!re.test(id_cart)){
            $('.error-msg').show();
            return
        }

        data_json = JSON.stringify({'real_name':real_name,'id_cart':id_cart});
        $.ajax({
            url:'/api/v1.0/user/real_name_auth',
            type:'POST',
            data:data_json,
            dataType:'json',
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')}
        }).done(function (data) {
            if (data.errno == 0){
                $('#real-name').val(data.data.real_name);
                $('#id_cart').val(data.data.id_cart);
                alert('设置成功')
            }else{
                if (data.errno == 4101){
                    location.href = '/login.html';
                    return
                };
                alert(data.errmsg)
            }
        })
    });


})

