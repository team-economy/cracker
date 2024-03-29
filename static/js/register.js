function sign_up() {
    let user_mail = $("#input-user_mail").val()
    let user_name = $("#input-user_name").val()
    let user_pw = $("#input-password").val()
    let user_pw2 = $("#input-password2").val()

    if ($("#help-mail").hasClass("is-danger")) {
        alert("이메일을 다시 확인해주세요.")
        return;
    } else if (!$("#help-mail").hasClass("is-success")) {
        alert("이메일 중복확인을 해주세요.")
        return;
    }

    if ($("#help-name").hasClass("is-danger")) {
        alert("별명을 다시 확인해주세요.")
        return;
    } else if (!$("#help-name").hasClass("is-success")) {
        alert("별명 중복확인을 해주세요.")
        return;
    }

    if (user_pw == "") {
        $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-password").focus()
        return;
    } else if (!is_password(user_pw)) {
        $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
        $("#input-password").focus()
        return
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
    }
    if (user_pw2 == "") {
        $("#help-password2").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-password2").focus()
        return;
    } else if (user_pw2 != user_pw) {
        $("#help-password2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
        $("#input-password2").focus()
        return;
    } else {
        $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
    }
    $.ajax({
        type: "POST",
        url: "/sign_up/save",
        data: {
            user_mail_give: user_mail,
            user_name_give: user_name,
            user_pw_give: user_pw
        },
        success: function (response) {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/login")
        }
    });

}

function toggle_sign_up() {
    $("#sign-up-name").toggleClass("is-hidden")
    $("#sign-up-box").toggleClass("is-hidden")
    $("#div-sign-in-or-up").toggleClass("is-hidden")
    $("#btn-check-dup-email").toggleClass("is-hidden")
    $("#btn-check-dup-username").toggleClass("is-hidden")
    $("#help-mail").toggleClass("is-hidden")
    $("#help-name").toggleClass("is-hidden")
    $("#help-password").toggleClass("is-hidden")
    $("#help-password2").toggleClass("is-hidden")
}

function is_mail(asValue) {
    var regExp = /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/;
    return regExp.test(asValue);
}

function is_name(asValue) {
    var regExp = /^([a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]).{1,10}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

function check_email_dup() {
    let user_mail = $("#input-user_mail").val()
    console.log(user_mail)
    if (user_mail == "") {
        $("#help-mail").text("이메일을 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-user_mail").focus()
        return;
    }
    if (!is_mail(user_mail)) {
        $("#help-mail").text("이메일의 형식을 확인해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-user_mail").focus()
        return;
    }
    $("#help-mail").addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/sign_up/check_email_dup",
        data: {
            user_mail_give: user_mail
        },
        success: function (response) {
            if (response["exists"]) {
                $("#help-mail").text("이미 존재하는 이메일입니다.").removeClass("is-safe").addClass("is-danger")
                $("#input-user_mail").focus()
            } else {
                $("#help-mail").text("사용할 수 있는 이메일입니다.").removeClass("is-danger").addClass("is-success")
            }
            $("#help-mail").removeClass("is-loading")

        }
    });
}

function check_user_dup() {
    let user_name = $("#input-user_name").val()
    console.log(user_name)

    $("#help-name").addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/sign_up/check_user_dup",
        data: {
            user_name_give: user_name
        },
        success: function (response) {
            if (response["exists"]) {
                $("#help-name").text("이미 존재하는 별명입니다.").removeClass("is-safe").addClass("is-danger")
                $("#input-user_name").focus()
            } else {
                $("#help-name").text("사용할 수 있는 별명입니다.").removeClass("is-danger").addClass("is-success")
            }
            $("#help-mail").removeClass("is-loading")

        }
    });
}