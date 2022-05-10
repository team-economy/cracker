let y_cen = 37.4981125   // lat
let x_cen = 127.0379399  // long
let map;
let markers = [];
let infowindows = [];
$(document).ready(function () {
    map = new naver.maps.Map('map', {
        center: new naver.maps.LatLng(y_cen, x_cen),
        zoom: 12,
        zoomControl: true,
        zoomControlOptions: {
            style: naver.maps.ZoomControlStyle.SMALL,
            position: naver.maps.Position.TOP_RIGHT
        }
    });
    get_posts()
})

function get_posts() {
    $('#posts-box').empty();
    $.ajax({
        type: "GET",
        url: '/maps',
        data: {},
        success: function (response) {
            let matjips = response["matjip_list"]
            for (let i = 0; i < matjips.length; i++) {
                let matjip = matjips[i]
                console.log(matjip)
                make_marker(matjip);
            }
        }
    })
}

function make_marker(matjip) {
    let marker = new naver.maps.Marker({
        position: new naver.maps.LatLng(matjip["y"], matjip["x"]),
        map: map
    });
    markers.push(marker);
}
