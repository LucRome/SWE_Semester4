$('.nav-tabs a').on('show.bs.tab', function (e) {
    paneID = $(e.target).attr('href');
    src = $(paneID).attr('data-src');
    // if the iframe hasn't already been loaded once
    if ($(paneID + " iframe").attr("src") == "") {
        $(paneID + " iframe").attr("src", src);
    }
});

$('iframe').on('load', function () {
    this.style.height = (this.contentDocument.body.scrollHeight + 20) + "px";
})
