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
    get_place()
})

function get_place() {
    $('#matjip-box').empty();
    markers = []
    infowindows = []
    $.ajax({
        type: "GET",
        url: `/map/mark`,
        data: {},
        success: function (response) {
            let matjips = response["matjip_list"]
            console.log(matjips.length)
            for (let i = 0; i < matjips.length; i++) {
                let matjip = matjips[i]
                make_card(i, matjip)
                let marker = make_marker(matjip)
                add_info(i, marker, matjip)
            }
        }
    });
}

function make_marker(matjip) {
    let marker = new naver.maps.Marker({
        position: new naver.maps.LatLng(matjip["y"], matjip["x"]),
        map: map
    });
    markers.push(marker);
    return marker
}

function make_card(i, matjip) {
    let place_addr = matjip["matjip_address"]
    let html_temp = `<div class="card" id="card-${i}">
                                <div class="card-body" style="background-color: #FDF6EC">
                                    <h5 class="card-title"><a href="javascript:click2center(${i})" class="matjip-title">${matjip['matjip_name']}</a></h5>
                                    <p class="card-text">지번 주소 : ${matjip['matjip_address']}</p>
                                    <p class="card-text">도로명 주소 : ${matjip['matjip_road_address']}</p>
                                    <p class="community-delete">
                                    <button class="button is-success" style="background-color: #A0BCC2; font-family: 'Gowun Batang', serif">커뮤니티
                                    </button>&nbsp&nbsp&nbsp<button class="button is-danger" style="background-color: #ECA6A6; font-family: 'Gowun Batang', serif"" onclick="delete_place('${place_addr}')">삭제</button>
                                    </p>
                                </div>
                            </div>`

    $('#matjip-box').append(html_temp);
}

function add_info(i, marker, matjip) {
    let html_temp = `<div class="iw-inner">
                                    <h5><b>${matjip['matjip_name']}</b></h5>
                                    <p class="card-text">지번 주소 : <i>${matjip['matjip_address']}</i></p>
                                    <p class="card-text">도로명 주소 : <i>${matjip['matjip_road_address']}</i></p>
                                    <p class="card-text">전화번호 : <span class="place-phone">${matjip['phone']}</span></p>
                                    </div>`;
    let infowindow = new naver.maps.InfoWindow({
        content: html_temp,
        maxWidth: 200,
        backgroundColor: "#fff",
        borderColor: "#888",
        borderWidth: 2,
        anchorSize: new naver.maps.Size(15, 15),
        anchorSkew: true,
        anchorColor: "#fff",
        pixelOffset: new naver.maps.Point(10, -10)
    });
    infowindows.push(infowindow)
    naver.maps.Event.addListener(marker, "click", function (e) {
        console.log("clicked", infowindows.length)
        if (infowindow.getMap()) {
            infowindow.close();
        } else {
            infowindow.open(map, marker);
            map.setCenter(infowindow.position)
            $("#matjip-box").animate({
                scrollTop: $("#matjip-box").get(0).scrollTop + $(`#card-${i}`).position().top
            }, 500);
        }
    });
}

function click2center(i) {
    let marker = markers[i]
    let infowindow = infowindows[i]
    if (infowindow.getMap()) {
        infowindow.close();
    } else {
        infowindow.open(map, marker);
        map.setCenter(infowindow.position)
    }
}