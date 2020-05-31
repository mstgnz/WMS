$(document).ready(function(){

    var path = window.location.pathname;
    $(`.accordion h6 a[href="${path}"]`).parent('h6').addClass('active');
    $(`.accordion h6 a[href="${path}"]`).parent('h6').next('p').css('display','block');
    // Accordion menu
    $(".accordion h6").on("click", function(e){
        $(".accordion h6").removeClass('active');
        $(this).addClass("active");
        $(".accordion li p").stop().slideUp();
        $(this).next("p").stop().slideToggle();
        span = $(this).find("span i").attr("class");
        if(span=="far fa-plus-square"){
            $(".accordion li span i").attr("class","far fa-plus-square");
            $(this).find("span i").attr("class","far fa-minus-square");
        }else{
            $(this).find("span i").attr("class","far fa-plus-square");
            $(".accordion h6").removeClass('active');
        }
    });

    // Worksite List
    $("#tab li:first").addClass("active");
    $(".tab_title:first").addClass("active");
    $(".tab_list:not(:first)").hide();
    $(".tab_content").hide();

    $("#tab li").click(function(){
        var windex = $(this).index();
        $("#tab li").removeClass("active");
        $(this).addClass("active");
        $(".tab_list").hide();
        $(".tab_list:eq("+ windex +")").show();
        $(".tab_list:eq("+ windex +") h6:first").addClass("active");
    });

    $(".tab_title").click(function(){
        $(".tab_title").removeClass("active");
        $(this).addClass("active");
        $(".tab_content").slideUp();
        $(this).find(".tab_content").stop().slideToggle();
    });


});
