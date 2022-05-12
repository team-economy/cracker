function post() {
    let comment = $("#textarea-post").val()
    let today = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/posting",
        data: {
            comment_give: comment,
            date_give: today
        },
        success: function (response) {
            window.location.reload()
        }
    })
}

function get_posts() {
    $("#post-box").empty()
    $.ajax({
        type: "GET",
        url: "/get_posts",
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    let time_post = new Date(post["date"])
                    let time_before = time2str(time_post)
                    let class_heart = post['heart_by_me'] ? "fa-heart" : "fa-heart-o"
                    let count_heart = post['count_heart']
                    let html_temp = `<div class="box" id="${post["_id"]}">
                                        <article class="media">
                                            <div class="media-left">
                                                <a class="image is-64x64" href="/user/${post['user_name']}">
                                                    <img class="is-rounded" src="/static/${post['user_pic_real']}"
                                                         alt="Image">
                                                </a>
                                            </div>
                                            <div class="media-content">
                                                <div class="content">
                                                    <p>
                                                        <strong>${post['user_name']}</strong> <small>${time_before}</small>
                                                        <br>
                                                        ${post['comment']}
                                                    </p>
                                                </div>
                                                <nav class="level is-mobile">
                                                    <div class="level-left">
                                                        <a class="level-item is-sparta" aria-label="heart" onclick="toggle_like('${post['_id']}', 'heart')">
                                                            <span class="icon is-small"><i class="fa ${class_heart}"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span class="like-num">${num2str(count_heart)}</span>
                                                        </a>
                                                    </div>

                                                </nav>
                                            </div>
                                        </article>
                                    </div>`
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
}

function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

function toggle_like(post_id, type) {
    console.log(post_id, type)
    let $a_like = $(`#${post_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass("fa-heart-o").removeClass("fa-heart")
                $a_like.find("span.like-num").text(response["count"])
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                $a_like.find("span.like-num").text(response["count"])
            }
        })

    }
}

// function toggle_like(post_id, type) {
//     console.log(post_id, type)
//     let $a_like = $(`#${post_id} a[aria-label='${type}']`)
//     let $i_like = $a_like.find("i")
//     let class_s = {"like": "fa-thumbs-up", "unlike": "fa-thumbs-down"}
//     let class_o = {"like": "fa-thumbs-o-up", "unlike": "fa-thumbs-o-down"}
//     if ($i_like.hasClass(class_s[type])) {
//         $.ajax({
//             type: "POST",
//             url: "/update_like",
//             data: {
//                 post_id_give: post_id,
//                 type_give: type,
//                 action_give: "unlike"
//             },
//             success: function (response) {
//                 console.log("unlike")
//                 $i_like.addClass(class_o[type]).removeClass(class_s[type])
//                 $a_like.find("span.like-num").text(num2str(response["count"]))
//             }
//         })
//     } else {
//         $.ajax({
//             type: "POST",
//             url: "/update_like",
//             data: {
//                 post_id_give: post_id,
//                 type_give: type,
//                 action_give: "like"
//             },
//             success: function (response) {
//                 console.log("like")
//                 $i_like.addClass(class_s[type]).removeClass(class_o[type])
//                 $a_like.find("span.like-num").text(num2str(response["count"]))
//             }
//         })
//
//     }
// }


function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"
    }
    if (count == 0) {
        return ""
    }
    return count
}

function delete_date(date) {
    $.ajax({
        type: "DELETE",
        url: `/delete`,
        data: {
            commu_give: date
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

$(document).ready(function () {
    get_posts()
})