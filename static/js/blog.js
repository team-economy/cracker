$(document).ready(function () {
    get_blog()
    get_blog_middle()
})

function get_blog() {
    $('#blog-box').empty();
    $.ajax({
        type: "GET",
        url: '/blog',
        data: {},
        success: function (response) {
            let blogs = response["blog_list"]
            console.log(blogs)
            for (let i = 0; i < blogs.length; i++) {
                let blog = blogs[i]
                let html_temp = `<div>
                                   <a href="${blog['link']}" target="_blank" id="place_name">&nbsp&nbsp&nbsp&nbsp<b>${blog['title']}</b></a>
                                       <p> </p>
                                       </label>
                                </div>`
                $("#blog-box").append(html_temp);
            }
        }
    })
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
                                    <a href="${blogmiddle['link']}" target="_blank" id="place_name">&nbsp&nbsp&nbsp&nbsp<b>${blogmiddle['title']}</b></a>
                                       <p>&nbsp;</p>
                                       </label>
                                </div>`
                $("#blog-box-middle").append(temp_html);
            }
        }
    })
}