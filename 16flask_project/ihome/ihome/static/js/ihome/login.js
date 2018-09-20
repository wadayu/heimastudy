function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        data = {'mobile':mobile,'password':passwd};
        data_json = JSON.stringify(data);
        $.ajax({
            url:'/api/v1.0/user/login',
            type:'POST',
            data: data_json,
            dataType:'json',
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')}
        }).done(function (data) {
            if (data.errno == '0'){
                location.href = 'index.html'
            }else{
                alert(data.errmsg)
            }
        })
    });
})