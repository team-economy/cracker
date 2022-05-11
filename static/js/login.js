function sign_in() {
    let user_mail = $("#input-user_mail").val()
    let user_pw = $("#input-password").val()

    if (user_mail == "") {
        $("#help-mail-login").text("이메일을 입력해주세요.")
        $("#input-user_mail").focus()
        return;
    } else {
        $("#help-mail-login").text("")
    }

    if (user_pw == "") {
        $("#help-password-login").text("비밀번호를 입력해주세요.")
        $("#input-password").focus()
        return;
    } else {
        $("#help-password-login").text("")
    }
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            user_mail_give: user_mail,
            user_pw_give: user_pw
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}
