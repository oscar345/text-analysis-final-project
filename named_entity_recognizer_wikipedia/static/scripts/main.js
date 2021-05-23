function switchInputMethod() {
    $("#switch-input-method").click(function () {
        $("#file-input-div").toggleClass("d-none");
        $("#text-area-input-div").toggleClass("d-none");

        if ($(this).hasClass("file")) {
            $(this).text("Use file upload");
            $('#file-input').prop('required', false);
            $('#text-area-input').prop('required', true);
        } else {
            $(this).text("Type text");
            $('#file-input').prop('required', true);
            $('#text-area-input').prop('required', false);
        }
        $(this).toggleClass("file")
    });
}


function showUploadedFilename() {
    document.querySelector('.custom-file-input').addEventListener('change', function (e) {
        var fileName = document.getElementById("file-input").files[0].name;
        var nextSibling = e.target.nextElementSibling;
        var fileFeedbackDiv = nextSibling.nextElementSibling;
        nextSibling.innerText = fileName;
        fileFeedbackDiv.classList.replace("invalid-feedback", "valid-feedback");
        fileFeedbackDiv.innerText = "The file has been uploaded succesfully to the website";
        fileFeedbackDiv.style.display = "block";
    })
}


$(function () {
    switchInputMethod();
    showUploadedFilename();
})

