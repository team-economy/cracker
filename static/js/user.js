$(document).ready(function () {
    get_user_place()
})

function update_profile() {
    let name = $('#input-user_name').val()
    let file = $('#input-pic')[0].files[0]
    let about = $("#textarea-about").val()

    if (name != $('#user_name').text()) {
        if ($("#help-name").hasClass("is-danger")) {
            alert("별명을 다시 확인해주세요.")
            return;
        } else if (!$("#help-name").hasClass("is-success")) {
            alert("별명 중복확인을 해주세요.")
            return;
        }
    }

    let form_data = new FormData()
    form_data.append("file_give", file)
    form_data.append("name_give", name)
    form_data.append("about_give", about)
    console.log(name, file, about, form_data)
    $.ajax({
        type: "POST",
        url: "/user/update_profile",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"])
                window.location.reload()

            }
        }
    });

}

function get_user_place() {
    $('#matjip-box').empty();
    let user_mail = $("#user_mail").text()
    $.ajax({
        type: "GET",
        url: `/user/place?user_mail_give=${user_mail}`,
        data: {},
        success: function (response) {
            let places = response["user_place"]
            console.log(places.length)
            for (let i = 0; i < places.length; i++) {
                let place = places[i]
                make_card(i, place)
            }
        }
    });

}

function update_marker() {
    let marker = $('#input-marker')[0].files[0]
    let form_marker_data = new FormData()
    form_marker_data.append("marker_give", marker)
    $.ajax({
        type: "POST",
        url: "/user/update_marker",
        data: form_marker_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"])
                window.location.reload()
            }
        }
    });
}

function make_card(i, matjip) {
    let place_addr = matjip["matjip_address"]
    let html_temp = `<div class="card" id="card-${i}">
                                <div class="card-body" style="background-color: #FDF6EC">
                                    <h5 class="card-title"><b>${matjip['matjip_name']}</b></h5>
                                    <p class="card-text category">카테고리 : ${matjip['category']}</p>
                                    <p class="card-text">지번 주소 : ${matjip['matjip_address']}</p>
                                    <p class="card-text">도로명 주소 : ${matjip['matjip_road_address']}</p>
                                    <div>
                                    <span class="card-text phone">전화 번호 : ${matjip['phone']}</span>
                                    <div class = "user-btn-community">
                                    <button class="button is-success" style="background-color: #A0BCC2; font-family: 'Gowun Batang', serif" onclick="location.href='/community/${matjip['matjip_name']}'">커뮤니티
                                    </button>&nbsp&nbsp&nbsp<button class="button is-danger" style="background-color: #ECA6A6; font-family: 'Gowun Batang', serif"" onclick="delete_place('${place_addr}')">삭제</button>
                                    </div>                     
                                    </p>
                                </div>
                            </div>`

    $('#matjip-box').append(html_temp);
}