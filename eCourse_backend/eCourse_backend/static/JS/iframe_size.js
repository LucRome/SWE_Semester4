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

$('.modal-button').on('click', function (e) {
    src = $(e.target).attr('data-src');
    modal_id = $($(e.target).attr('data-target'));
    iframe = $(modal_id).children('.modal-dialog').children('.modal-content').children(".modal-body").children("iframe");
    // if the iframe hasn't already been loaded once
    if ($(iframe).attr("src") == "") {
        $(iframe).attr("src", src);
    }
})