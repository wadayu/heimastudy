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
    // 更新用户头像
    $('#form-avatar').submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
        $(this).ajaxSubmit({
            url:'/api/v1.0/user/update_image',
            type:'POST',
            dataType:'json',
            headers:{"X-CSRFToken":getCookie('csrf_token')},
            success:function (data) {
            if (data.errno == 0){
                $('#user-avatar').attr('src',data.data.image_url)
            }else{
                if (data.errno == 4101){
                    location.href = '/login.html';
                }
                alert(data.errmsg)
            }}
        })
    });

    // 展示头像及用户名信息
    $.get('/api/v1.0/user/info',function (data) {
        if (data.errno == 0){
            $('#user-avatar').attr('src',data.data.image_url);
            $('#user-name').val(data.data.username)
        }else{
            if (data.errno == 4101){
                location.href = '/login.html';
            }
            alert(data.errmsg)
            
        }
    });

    // 修改用户的用户名
    $('#form-name').submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();

        var username = $('#user-name').val();
        // 序列化json格式
        data_json = JSON.stringify({'username':username});
        $.ajax({
            url:'/api/v1.0/user/info',
            type: 'POST',
            data:data_json,
            contentType:'application/json',
            dataType:'json',
            headers:{'X-CSRFToken':getCookie('csrf_token')}
        }).done(function (data) {
            if (data.errno == 0){
                $('#user-name').val(data.data.username);
                alert('修改成功')
            }else{
                if (data.errno == 4101){
                    location.href = '/login.html';
                }
                alert(data.errmsg)
            }
        })
    })
})

