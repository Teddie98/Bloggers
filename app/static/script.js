function clicked() {
    console.log("clickes");
}

// use classes to hide and show the requred forms, create a general class for hidden and a unique class to represent the current showing macro// also remember thatone function will contain all the required classes and it will take arguments of current class and classes to be hidden and it will be called by oother functions on click events in their respective buttons.......find a way to make sure that no two classes are open at the same time

// i has got to fucking sleep at this point now

$(document).ready(function () {
    $(".posts-options").click(function (e) {
        e.preventDefault();
        $('.new-blog').addClass('d-none');
        $('.all-blogs').removeClass('d-none');
    });
    $(".new-blog-btn").click(function (e) {
        e.preventDefault();
        $('.new-blog').removeClass('d-none');
        $('.all-blogs').addClass('d-none');
    });
});