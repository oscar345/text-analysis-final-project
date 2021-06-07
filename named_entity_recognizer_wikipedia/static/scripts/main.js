function switchInputMethod() {
    $("#switch-input-method").click(function () {
        $("#file-input-div").toggleClass("d-none");
        $("#text-area-input-div").toggleClass("d-none");

        if ($(this).hasClass("file")) {
            $(this).text("Use .pos file");
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


function showUploadedFilename(fileInputId) {
    document.querySelector(`#${fileInputId}`).addEventListener('change', function (e) {
        var fileName = document.getElementById(fileInputId).files[0].name;
        var nextSibling = e.target.nextElementSibling;
        var fileFeedbackDiv = nextSibling.nextElementSibling;
        nextSibling.innerText = fileName;
        fileFeedbackDiv.classList.replace("invalid-feedback", "valid-feedback");
        fileFeedbackDiv.innerText = "Your file has been successfully uploaded to the website";
        fileFeedbackDiv.style.display = "block";
    })
}

function showHideElement(elementId) {
    $(`#${elementId}`).toggleClass("d-none");
}

function showHideOptions() {
    $("#add-test-file").click(function() {
        showHideElement("test-file-input-div")
    });
    $("#add-extra-tags").click(function() {
        showHideElement("extra-categories-input")
    });
}


function getProgress() {
    $("#submit-data").click(function() {
        $("#progress-text").html(`<div class="progress"><div id="progress-bar" class="progress-bar"></div></div>`)
        $("#universal-modal").modal("show");
        window.setInterval(() => {
            fetch("./progress", {
                method: "POST",
                type: "application/json"
            })
            .then(request => request.json())
            .then((request) => {
                let percentage = Math.round(request.progress / 7 * 100);
                $("#progress-bar").css("width", `${percentage}%`);
                $("#progress-bar").text(percentage);
            })
        }, 1000)
    })
}


$(document).ready(function () {
    switchInputMethod();
    showUploadedFilename("file-input");
    showUploadedFilename("test-file-input");
    getProgress();
    showHideOptions();
})

