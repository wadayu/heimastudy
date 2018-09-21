function logout() {
    $.get("/api/v1.0/user/logout", function(data){
        if (0 == data.errno) {
            location.href = "index.html";
        }
    })
}

// 个人主页详情信息
$(document).ready(function(){
    $.get('/api/v1.0/user/user_home',function (data) {
        if (data.errno == 0){
            $('#user-name').html(data.data.username);
            $('#user-mobile').html(data.data.mobile);
            $('#user-avatar').attr('src',data.data.image_url)
        }else{
            if (data.errno == 4101){
                location.href = '/login.html';
            }
            alert(data.errmsg)
        }
    })
})