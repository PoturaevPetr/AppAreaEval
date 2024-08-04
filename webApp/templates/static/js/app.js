
function loadFile(input) {
    var preview_div = $(input).data("preview")

    $('#' + preview_div).empty();
    if ($(input)[0].files[0]) {
        for(i=0;i<$(input)[0].files.length;i++)
        {
            if (($(input)[0].files[i].type.includes('image')))
            {
                div = document.createElement('div');
                div.setAttribute('class', 'col-12 p-1 m-0');
                img = document.createElement('img');
                img.setAttribute('class', 'preview_img w-100');
                img.setAttribute('id', $(input)[0].files[i].name.split('.')[0]);
                previewIMG($(input)[0].files[i], $(img));
                div.appendChild(img);
                $("#" + preview_div).append(div);
            }
        }
    }
}

function previewIMG(input, preview) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $(preview).attr('src', e.target.result);
    }
    reader.readAsDataURL(input);
}

function upload(input) {
    var fileList = $(input).prop("files");
    for(i=0; i<fileList.length; i++) {
        var formData = new FormData();
        if (fileList[i].type.includes('image')) {
            formData.append("files", fileList[i]);
            $.ajax({
                type:'POST',
                data: formData,
                url: '/upload_image?type=' + $(input).data('type'),
                async: false,
                processData: false,  // tell jQuery not to process the data
                contentType: false,  // tell jQuery not to set contentType
                success: (data) => {
                    
                },
                error:function (jqXHR, exception) {
                    $('#' + fileList[i].name.split('.')[0]).css('opacity', '70%');
                    $('#' + fileList[i].name.split('.')[0]).parent().css('background-color', 'red');
                }
            });
        }
    }
}

function loadImagesList() {
    $.ajax({
        type: "GET",
        url: "/list_image_type",
        async: false,
        contentType: false,
        processData: false,
        success: (data) => {
            var src = data['src']
            $("#list_imgs").empty()
            for (var i = 0; i < src.length; i++) {
                $("#list_imgs").append(
                    "<div class='col-2'>\
                        <img class='w-100 image_process' data-type='" + src[i] + "' src='/proccess_pic?type=" + src[i] +"&part=src&q=" + make_rnd(8) +"'>\
                    </div>"
                )
            }
        }
    })
}

function imageReturner(type, part) {
    $("#image_edit").attr("src", "/proccess_pic?type=" + type + "&part=" + part + "&q=" + make_rnd(8))
}

function imageReturnerResult(type, part) {
    $("#calc_result").append(
        "<div class='col-6 mt-1'>\
            <p class='p-0 m-0'>Тип изображения: " + type + "</p>\
            <img class='w-100' src='/proccess_pic?type=" + type + "&part=" + part + "&q=" + make_rnd(8) +"'>\
        </div>"
    )
}


function make_rnd(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}


$(document).ready(function() {
    $("#preview_top_input").on("change", function() {
        loadFile(this)
        upload(this)
        loadImagesList()
    })

    $("#preview_side_input").on("change", function() {
        loadFile(this)
        upload(this)
        loadImagesList()
    })

    $(document).on("click", ".image_process", function() {
        var type = $(this).data('type')
        $("#image_edit").attr('data-type', type)
        imageReturner(type, 'src')
    }) 

    $(document).on("input", ".slice", function() {
        var type = $('#image_edit').attr("data-type")
        var props = {
            y: [$("#x0").val(), $("#x1").val()],
            x: [$("#y0").val(), $("#y1").val()],
            type: type
        }
        $.ajax({
            type: "POST",
            url: "/crop_img",
            contentType: false,
            processData: false,
            data: JSON.stringify(props),
            success: (data) => {
                imageReturner(type + "_rect", "edited")
            }
        })
    }) 

    $("#start_eval").on("click", function() {
        var props = {
            real: {
                x: $("#real_x").val(),
                y: $("#real_y").val(),
                z: $("#real_z").val()
            },
            sep: $("#sep").val(),
            tresh: $("#tresh").val(),
            mode: $("#mode").find(":selected").attr('value'),
            type: $('#image_edit').attr("data-type")

        }
        $.ajax({
            type: "POST",
            url: "/eval",
            contentType: false,
            processData: false,
            data: JSON.stringify(props),
            success: (data) => {
                var type = data['type']
                $("#calc_result").empty()
                imageReturnerResult(type + "_gray", 'edited')
                imageReturnerResult(type + "_mask", 'edited')
                imageReturnerResult(type + "_cnts", 'edited')
                $("#calc_result").append(
                    "<div class='col-12 mt-2'>\
                        <p>\
                            Площадь поверхности: " + data['result']['all_area'] + "\
                        </p>\
                    </div>"
                )
            }
        })
    })
})