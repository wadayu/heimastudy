/**
 * Created by jsb-yw02 on 2018/7/9.
 */

window.onload = function () {
    var oSlide = document.getElementById('slide');
    oSlide.innerHTML = oSlide.innerHTML + oSlide.innerHTML;

    var iLeft = 0;
    var iSpeed = 3;

    var timer = setInterval(function () {
        oSlide.style.left = iLeft + 'px';
        iLeft += 3;
    },30);

    if (iLeft > 0){
        iLeft = -2280;
    };

    if (iLeft < -2280){
        iLeft = 0;
    }


};
