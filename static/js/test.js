function post() {
    let comment = $("#textarea-post").val()
    let date_time = datetime.now()
    let today = date_time.strftime("%Y-%m-%d-%H-%M-%S")
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
        url: `/get_posts`,
        data: {},
        success: function (response) {

            if (response["result"] == "success") {
                let posts = response["posts"]
                let post_date = posts["date"]
                console.log(posts)
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    //let time_post = new Date(post["date"])
                    // let time_before = time2str(time_post)
                    let date_time = datetime.now()
                    let today = date_time.strftime("%Y-%m-%d-%H-%M-%S")
                                            // 삼항             true 값              False 값
                    let class_like = post['like_by_me'] ? "fa-thumbs-up" : "fa-thumbs-o-up"
                    let class_unlike = post['like_by_me'] ? "fa-thumbs-down" : "fa-thumbs-o-down"

                    let html_temp = `<div class="box" id="${post["_id"]}">
                                        <article class="media">
                                            <div class="media-left">
                                                <a class="image is-64x64" href="/user/${post['user_name']}">
                                                    <img class="is-rounded"
                                                        <img class="is-rounded" src="/static/${post['user_real_pic']}"
                                                         alt="Image">
                                                </a>
                                            </div>
                                            <div class="media-content">
                                                     <p class="community-delete">
                                                    <button class="btn btn-white btn-animate">수정
                                                    </button>&nbsp&nbsp&nbsp<button class="btn btn-white btn-animate" onclick="delete_date('${today}')">삭제</button>
                                                    
                                                    </p>
                                                <div class="content">
                                                    <p>
                                                        <strong>${post['user_name']}</strong> <small>${today}</small>
                                                        <br>
                                                        ${post['comment']}
                                                    </p>
                                                   
                                                </div>
                                                <nav class="level is-mobile">
                                                    <div class="level-left">
                                                        <a class="level-item is-sparta" aria-label="like" onclick="toggle_like('${post['_id']}', 'like')">
                                                            <span class="icon is-small"><i class="fa ${class_like}"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span class="like-num">${num2str(post["count_like"])}</span>
                                                        </a>
                                                        <a class="level-item is-sparta" aria-label="unlike" onclick="toggle_like('${post['_id']}', 'unlike')">
                                                            <span class="icon is-small"><i class="fa ${class_unlike}"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span class="like-num">${num2str(post["count_unlike"])}</span>
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

// function time2str(date) {
//     let today = new Date()
//     let time = (today - date) / 1000 / 60  // 분
//
//     if (time < 60) {
//         return parseInt(time) + "분 전"
//     }
//     time = time / 60  // 시간
//     if (time < 24) {
//         return parseInt(time) + "시간 전"
//     }
//     time = time / 24
//     if (time < 7) {
//         return parseInt(time) + "일 전"
//     }
//     return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
// }

function toggle_like(post_id, type) {
    console.log(post_id, type)
    let $a_like = $(`#${post_id} a[aria-label='${type}']`)
    let $i_like = $a_like.find("i")
    let class_s = {"like": "fa-thumbs-up", "unlike": "fa-thumbs-down"}
    let class_o = {"like": "fa-thumbs-o-up", "unlike": "fa-thumbs-o-down"}
    if ($i_like.hasClass(class_s[type])) {
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
                $i_like.addClass(class_o[type]).removeClass(class_s[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
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
                $i_like.addClass(class_s[type]).removeClass(class_o[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })

    }
}


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