function get_address() {
    let matjip_name = $("#input-post").val()
    $("#input-post").val("");
    $("#place_list").empty();
    $.ajax({
        type: "GET",
        url: `/place/search?place_give=${matjip_name}`,
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
                                            <input class="form-check-input" type="radio" name="place" id="place${i}" 
                                            value="${place['place_name']},${place['address_name']},${place['road_address_name']},${place['x']},${place['y']},${place['phone']}">
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

    let x = radio_button.split(',')[3];
    let y = radio_button.split(',')[4];

    let phone = radio_button.split(',')[5];

    console.log(place)
    console.log(addr)
    console.log(addr_road)

    $.ajax({
        type: "POST",
        url: `/place/save`,
        data: {
            place_give: place,
            addr_give: addr,
            addr_road_give: addr_road,
            x_give: x,
            y_give: y,
            phone_give: phone
        },
        success: function (response) {
            if (response["msg"] == "저장 완료!!") {
                alert(response["msg"])
                $("#modal-post").removeClass("is-active")
                window.location.reload()
            } else {
                alert(response["msg"])
                $("#modal-post").removeClass("is-active")
            }
        }

    })
}

function delete_place(addr) {
    $.ajax({
        type: "DELETE",
        url: `/place/delete`,
        data: {
            addr_give: addr
        },
        success: function (response) {
            if (response["msg"] == "삭제 완료!!") {
                alert(response["msg"])
                window.location.reload()
            } else {
                alert(response["msg"])
            }
        }

    })
}