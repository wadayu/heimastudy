$(function () {
    var $username = $('#username');
    var $password = $('#password');
    var $errmsg = $('#errmsg');

    if ($errmsg.html()){
        $errmsg.show()
    }

    $username.focus(function () {
        $errmsg.hide()
    })

    $password.focus(function () {
        $errmsg.hide()
    })
});



