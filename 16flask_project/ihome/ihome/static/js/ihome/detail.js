function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(function(){
    // 房屋详情页面
    var queryData = decodeQuery();
    var houseId = queryData['id']; // 获取房屋的id
    $.get('/api/v1.0/house/detail/'+houseId ,function (data) {
        if (data.errno == 0){
            var img_content = template('image_path',{image_urls:data.data.house_info.img_urls,price:data.data.house_info.price});
            $('.swiper-container').html(img_content);
            var house_content = template('house_info',{house:data.data.house_info});
            $('.detail-con').html(house_content);
            if (data.data.user_id != data.data.house_info.user_id ){
                $(".book-house").show();
            }
            // 图片轮播
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
        }else{
            alert(data.errmsg)
        }

    })



})