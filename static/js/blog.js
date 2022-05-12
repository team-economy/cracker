let i = 0;

$(document).ready(function () {
    get_blog()
    get_blog_middle()
})

function get_blog() {
    $.ajax({
        type: "GET",
        url: '/blog',
        data: {},
        success: function (response) {
            let blogs = response["blog_list"]
            console.log(blogs)
            const next = document.querySelector(".next")
            next.addEventListener("click", temp_html (blogs)); {
                $('#blog-box').empty();
                // temp_html(blog)
                console.log("clicked", i)
            }
            }
    })

function temp_html(blog) {
    i++;
    let html_temp = `<div class="card" style="width: 18rem;">
                          <img src="${blog['img']}" class="card-img-top" alt="...">
                          <div class="card-body">
                            <a href="${blog['link']}" target="_blank" id="place_name">&nbsp&nbsp&nbsp&nbsp<b>${blog['title']}                                  </div>
                        </div>`
    $('#blog-box').append(html_temp)
}


function get_blog_middle() {
    $('#blog-box-middle').empty();
    $.ajax({
        type: "GET",
        url: '/blogmiddle',
        data: {},
        success: function (response) {
            let blogsmiddle = response["blog_list_middle"]
            console.log(blogsmiddle)
            for (let i = 0; i < blogsmiddle.length; i++) {
                let blogmiddle = blogsmiddle[i]
                let temp_html = `<div>
                                <div><img src="static/cookie.png" width="50" height="50">
                                <a href="${blogmiddle['link']}" target="_blank" id="place_name">&nbsp&nbsp&nbsp&nbsp<b>${blogmiddle['title']}</b></a>
                                   </label>
                            </div>`
                $("#blog-box-middle").append(temp_html);
            }
        }
    })
}
}