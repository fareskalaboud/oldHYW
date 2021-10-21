function submitBtnClicked() {
    console.log("yay")
    $("#youtube_url_form_container").addClass("animate__animated");
    $("#youtube_url_form_container").addClass("animate__fadeOut");
    // $("#youtube_url_form_container").addClass("hidden");

    $("#loading").removeClass("hidden");
    $("#loading").addClass("animate__fadeIn");

    $("#box-er").addClass("hidden");
    $("#box-sc").addClass("hidden");
    $("#box-wr").addClass("hidden");
}