$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    $('#addingredients li').each(function (i) {
        $(this).find('input').eq(0).attr("name", i++);
    });

    // Ingredients Add row
    // Append table with add row form on add new button click
    $("#add-newing").click(function () {
        var col = '<tr>' +
            '<td>' +
            '<ul>' + '<li><input type="text" class="form-control" name="ingredients" value=""></li>' + '</ul>' +
            '</td>' +
            '<td>' + actions + '</td>' +
            '</tr>';

        //add ingredients table row form for addrecipe.html
        $("#addingredients").append(col);
        $('[data-toggle="tooltip"]').tooltip();

        //add ingredients table row form for editrecipe.html
        $("#editIngredients").append(col);
        $('[data-toggle="tooltip"]').tooltip();

    });

    $('#addinstruction li').each(function (i) {
        $(this).find('input').eq(0).attr("name", i++);
    });

    // Instructions Add row
    // Append table with add row form on add new button click
    $("#add-newmethod").click(function () {

        var col = '<tr>' +
            '<td>' +
            '<ul>' + '<li><input type="text" class="form-control" name="instructions"></li>' + '</ul>' +
            '</td>' +
            '<td>' + actions + '</td>' +
            '</tr>';

        //add instructions table row form for addrecipe.html 
        $("#addinstruction").append(col);
        $('[data-toggle="tooltip"]').tooltip();

        //add instructions table row form for editrecipe.html
        $("#editInstruction").append(col);
        $('[data-toggle="tooltip"]').tooltip();
    });
    // delete row on add button click
    $(document).on("click", ".delete", function () {
        $(this).parents("tr").remove();
    });

});

// When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar
var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("mainNav").style.top = "0";
    } else {
        document.getElementById("mainNav").style.top = "-55px";
    }
    prevScrollpos = currentScrollPos;
}

// Float Back To Top Smooth Scrolling
$(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
        $('#scroll').fadeIn();
    } else {
        $('#scroll').fadeOut();
    }
});

// FLOAT TO TOP
$('#scroll').click(function () {
    $("html, body").animate({
        scrollTop: 0
    }, 600);
    return false;
});