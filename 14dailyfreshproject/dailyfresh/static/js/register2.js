/**
 * Created by jsb-yw02 on 2018/7/20.
 */
$(function () {
    var error_name = false;
    var error_passwd = false;
    var error_cpasswd = false;
    var error_email = false;
    var error_checked = false;

    var $user_name = $('#user_name');
    var $pass_word = $('#pwd');
    var $pass_again = $('#cpwd');
    var $email = $('#email');
    var $errmsg = $('#errmsg');

    // 如果有错误信息就显示信息
    if ($errmsg.html()){
        $errmsg.show()
    }

    $user_name.blur(function () {
        check_username();
    });

    $user_name.focus(function () {
        $user_name.next().hide();
        $errmsg.hide() // 隐藏错误
    });

    $pass_word.blur(function () {
        check_password();
    });

    $pass_word.focus(function () {
        $pass_word.next().hide();
        $errmsg.hide() // 隐藏错误
    });

    $pass_again.blur(function () {
    check_cpassword();
    });

    $pass_again.focus(function () {
        $pass_again.next().hide();
        $errmsg.hide() // 隐藏错误
    });

    $email.blur(function () {
    check_email();
    });

    $email.focus(function () {
        $email.next().hide();
        $errmsg.hide() // 隐藏错误
    });

    $('#allow').click(function () {
        if($(this).is(':checked')){
            $(this).siblings('span').hide();
            error_checked = false
        }
        else{
            $(this).siblings('span').html('请先勾选同意');
            $(this).siblings('span').show();
            error_checked = true
        }
    });

    function check_username() {
        var re = /^\w{6,15}(\@[a-z0-9]+(\.[0-9a-z]+){1,2})?$/;
        var val = $user_name.val();
        if (val == '') {
            $user_name.next().html('用户名不能为空');
            $user_name.next().show();
            error_name = true;
            return
        }

        if (re.test(val)) {
            $user_name.next().hide();
            error_name = false
        }
        else {
            $user_name.next().html('用户名是6到15个英文或数字，或者邮箱');
            $user_name.next().show();
            error_name = true;
            return
        }
    }

    function check_password() {
        var re = /^[\w@!#$%&^*]{6,15}$/;
        var val = $pass_word.val();

        if (val == '') {
            $pass_word.next().html('密码不能为空');
            $pass_word.next().show();
            error_passwd = true;
            return
        }

        if (re.test(val)) {
            $pass_word.next().hide();
            error_passwd = false
        }
        else{
            $pass_word.next().html('密码是6到15位字母、数字，还可包含@!#$%^&*字符');
            $pass_word.next().show();
            error_passwd = true;
            return
        }
    }

    function check_cpassword() {
        var password = $pass_word.val();
        var cpassword = $pass_again.val();

        if(cpassword==''){
            $pass_again.next().html('确认密码不能为空');
            $pass_again.next().show();
            error_cpasswd = true;
            return
        }

        if(password==cpassword){
            $pass_again.next().hide();
            error_cpasswd = false
        }
        else{
            $pass_again.next().html('两次输入的密码不一致');
            $pass_again.next().show();
            error_cpasswd = true;
            return
        }
    }

    function check_email() {
        var re = /^[a-z0-9][\w\.\-]{4,15}@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
        var val = $email.val();

        if (val==''){
            $email.next().html('邮箱不能为空');
            $email.next().show();
            error_email = true;
            return
        }

        if (re.test(val)){
            $email.next().hide();
            error_email = false;
        }
        else{
            $email.next().html('输入的邮箱不合法');
            $email.next().show();
            error_email = true;
            return
        }

    }


    $('#form').submit(function () {
        if(error_name == false && error_passwd == false && error_cpasswd == false && error_email == false && error_checked == false){
            return true
        }
        else{
            return false
        }
    })
});
