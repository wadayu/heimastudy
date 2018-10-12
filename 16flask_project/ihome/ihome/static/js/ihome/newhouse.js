function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // 获取地区
    $.get('/api/v1.0/areas',function (data) {
        if (data.errno == "0"){
            // var content = '';
            // $.each(data.data,function (k,v) {
            //     content += "<option value="+ k +">"+ v +"</option>"
            // });
            //
            // $('#area-id').append(content)
            // 使用js模板（template.js）
            var html = template('areas_tmp',{areas:data.data});
            $('#area-id').append(html)
        }else{
            alert(data.errmsg)
        }
    });

    //新建房屋信息
    $('#form-house-info').submit(function (e) {
        e.preventDefault(); // 阻止默认提交行为
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name]=x.value}); //获取提交的参数

        var facility_li = []; // 收集房屋设施id
        $(':checkbox[name=facility]:checked').each(function(index,x){facility_li[index]=$(this).val()});

        data.facility = facility_li; // 更新data的房屋设置列表
        data.address = '北京市' + $('#area-id').find("option:selected").html() + data.address;
        $.ajax({
            url:'/api/v1.0/houses/info',
            type:'post',
            data: JSON.stringify(data),
            contentType: 'application/json',
            dataType: 'json',
            headers:{'X-CSRFToken':getCookie('csrf_token')}
        }).done(function (data) {
            if (data.errno == '4101'){
                location.href = '/login.html'
            }else if (data.errno == '0'){
                $('#form-house-info').hide();
                $('#form-house-image').show();
                $('#house-id').val(data.data.house_id)
            }else{
                alert(data.errmsg)
            }
        })
    });

    // 房屋图片上传
    $('#form-house-image').submit(function (e) {
        e.preventDefault();
        // 上传图片的ajax
        $(this).ajaxSubmit({
            url: '/api/v1.0/houses/images',
            type: 'post',
            dataType: 'json',
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (data) {
                if (data.errno == '4101') {
                    location.href = '/login.html'
                } else if (data.errno == '0') {
                    var html = "<img src=" + data.data.image_url + ">";
                    $('.house-image-cons').append(html)
                } else {
                    alert(data.errmsg)
                }
            }
        });
    });
})