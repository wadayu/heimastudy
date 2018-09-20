function logout() {
    $.get("/api/v1.0/user/logout", function(data){
        if (0 == data.errno) {
            location.href = "index.html";
        }
    })
}

$(document).ready(function(){
    $.get('/api/v1.0/user/user_home',function (data) {
        if (data.errno == 0){
            $('#user-name').html(data.data.username);
            $('#user-mobile').html(data.data.mobile)
        }else{
            alert(data.errmsg)
        }
    })
})