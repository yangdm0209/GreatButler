$(function () {
    $('.input-daterange').datepicker({
        language: "zh-CN",
        autoclose: true,//选中之后自动隐藏日期选择框
        todayBtn: true,//今日按钮
        format: "yyyy-mm-dd"//日期格式，详见 http://bootstrap-datepicker.readthedocs.org/en/release/options.html#format
    });
    $('.input-group.date').datepicker({
        language: "zh-CN",
        autoclose: true,//选中之后自动隐藏日期选择框
        todayBtn: true,//今日按钮
        format: "yyyy-mm-dd"//日期格式，详见 http://bootstrap-datepicker.readthedocs.org/en/release/options.html#format
    });
});

$(function() {
    $('#toggle-event').change(function() {
    if($(this).prop('checked')){
        $(this).parent.removeAttr("disabled");
    }
    else{
        $(this).parent.attr("disabled","disabled");
    }
        $('#console-event').html('Toggle: ' + $(this).prop('checked'))
    })
})

// item selection
$('img').click(function () {
  $(this).toggleClass('selected');
});