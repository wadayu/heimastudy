$(function () {
    var err_name = false;
    var err_pwd = false;

    var $login = $('#login');
    var $username = $('#username');
    var $password = $('#password');
    var $errmsg = $('#errmsg');

    if ($errmsg.html()){
        $errmsg.show()
    }

    $username.blur(function () {
        check_username();
    });

    $username.focus(function () {
        $username.next().hide();
        $errmsg.hide()
    });

    $password.blur(function () {
        check_password();
    });

    $password.focus(function () {
        $password.next().hide();
        $errmsg.hide()
    });

    function check_username() {
        var re = /^\w{6,15}(\@[a-z0-9]+(\.[0-9a-z]+){1,2})?$/;
        var val = $username.val();
        if (val == '') {
            $username.next().html('用户名不能为空');
            $username.next().show();
            err_name = true;
            return false
        }

        if (re.test(val)) {
            $username.next().hide();
            err_name = false
        }
        else {
            $username.next().html('用户名是6到15个英文或数字，或者邮箱');
            $username.next().show();
            err_name = true;
            return false
        }
    }

    function check_password() {
        var re = /^[\w@!#$%&^*]{6,15}$/;
        var val = $password.val();

        if (val == '') {
            $password.next().html('密码不能为空');
            $password.next().show();
            err_pwd = true;
            return false
        }

        if (re.test(val)) {
            $password.next().hide();
            err_pwd = false;
        }
        else{
            $password.next().html('密码是6到15位字母、数字');
            $password.next().show();
            err_pwd = true;
            return false
        }
    }

    $login.submit(function () {
        if($username.val() == '' || $password.val() == ''){
            $errmsg.html('用户名或者密码不能为空').show();
            return false
        }

        if(err_name == false && err_pwd == false){
            return true
        }else{
            return false
        }
    })

});



