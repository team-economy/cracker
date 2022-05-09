$(document).ready(function () {
    get_place()
})

function get_address() {
    let matjip_name = $("#input-post").val()
    $("#input-post").val("");
    $("#place_list").empty();
    $.ajax({
        type: "GET",
        url: `/get_address?place_give=${matjip_name}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                if (response["msg"] == "input empty") {
                    alert("맛집이름을 입력해 주세요!")
                } else if (response["msg"] == "no result") {
                    alert("일치하는 정보가 없습니다.")
                } else {
                    $("#modal-post").addClass("is-active");
                    let places = response["places"]
                    for (let i = 0; i < places.length; i++) {
                        let place = places[i]

                        let html_temp = `<div class="form-check">
                                            <input class="form-check-input" type="radio" name="place" id="place${i}" value="${place['place_name']},${place['address_name']},${place['road_address_name']}">
                                            <label class="form-check-label" for="${place['place_name']}" id="label">
                                                <p id="place_name"><b>${place['place_name']}</b></a>
                                                <p>${place['category_name']}</p>
                                                <p>${place['address_name']} | ${place['road_address_name']}</p>
                                            </label>
                                        </div>`
                        $("#place_list").append(html_temp);
                    }
                }
            }
        }
    })
}

function save_place() {
    let radio_button = $('input[name="place"]:checked').val();
    let place = radio_button.split(',')[0];
    let addr = radio_button.split(',')[1];
    let addr_road = radio_button.split(',')[2];

    console.log(place)
    console.log(addr)
    console.log(addr_road)

    $.ajax({
        type: "POST",
        url: `/save_place`,
        data: {
            place_give: place,
            addr_give: addr,
            addr_road_give: addr_road
        },
        success: function (response) {
            $("#modal-post").removeClass("is-active")
            window.location.reload()
        }

    })
}

function get_place() {
    $('#matjip-box').empty();
    $.ajax({
        type: "GET",
        url: `/get_place`,
        data: {},
        success: function (response) {
            let matjips = response["matjip_list"]
            console.log(matjips.length)
            for (let i = 0; i < matjips.length; i++) {
                let matjip = matjips[i]
                make_card(i, matjip)
            }
        }
    });
}

function make_card(i, matjip) {
    let html_temp = `<div class="card" id="card-${i}">
                                <div class="card-body">
                                    <h5 class="card-title"><a href="#" class="matjip-title">${matjip['matjip_name']}</a></h5>
                                    <p class="card-text">지번 주소 : ${matjip['matjip_address']}</p>
                                    <p class="card-text">도로명 주소 : ${matjip['matjip_road_address']}</p>
                                </div>
                            </div>`

    $('#matjip-box').append(html_temp);
}
