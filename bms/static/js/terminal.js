/**
 * Created by wyf on 2017/9/8.
 */
$("#input_icon").click(function () {
    var $ele=$("<p>");
    $ele.text($("input").val());
    $(".body_right").append($ele)
});