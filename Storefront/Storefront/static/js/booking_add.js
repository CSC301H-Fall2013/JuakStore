/**
 * Created by wyeung on 11/12/2013.
 */
//function showHideFrequency(show){
//    if (show){
//        document.getElementById("id_repeat_frequency").style.display = 'block'
//        document.getElementById("id_repeat_frequency_unit").style.display = 'block'
//        document.getElementById("id_repeat_end_year").style.display = 'block'
//        document.getElementById("id_repeat_end_month").style.display = 'block'
//        document.getElementById("id_repeat_end_day").style.display = 'block'
//    } else {
//        document.getElementById("id_repeat_frequency").style.display = 'none'
//        document.getElementById("id_repeat_frequency_unit").style.display = 'none'
//        document.getElementById("id_repeat_end_year").style.display = 'none'
//        document.getElementById("id_repeat_end_month").style.display = 'none'
//        document.getElementById("id_repeat_end_day").style.display = 'none'
//    }
//}

$(document).ready(function(){
    // initially hide all these elements
    $("label[for=id_repeat_frequency], #id_repeat_frequency").hide();
    $("label[for=id_repeat_frequency_unit], #id_repeat_frequency_unit").hide();
    $("label[for=id_repeat_end_year], #id_repeat_end_year").hide();
    $("label[for=id_repeat_end_month], #id_repeat_end_month").hide();
    $("label[for=id_repeat_end_day], #id_repeat_end_day").hide();

    $("#id_repeat").change(function(){
        console.log($("#id_repeat").val());
        if ($("#id_repeat").prop('checked')){
            $("label[for=id_repeat_frequency], #id_repeat_frequency").show();
            $("label[for=id_repeat_frequency_unit], #id_repeat_frequency_unit").show();
            $("label[for=id_repeat_end_year], #id_repeat_end_year").show();
            $("label[for=id_repeat_end_month], #id_repeat_end_month").show();
            $("label[for=id_repeat_end_day], #id_repeat_end_day").show();
        } else {
            $("label[for=id_repeat_frequency], #id_repeat_frequency").hide();
            $("label[for=id_repeat_frequency_unit], #id_repeat_frequency_unit").hide();
            $("label[for=id_repeat_end_year], #id_repeat_end_year").hide();
            $("label[for=id_repeat_end_month], #id_repeat_end_month").hide();
            $("label[for=id_repeat_end_day], #id_repeat_end_day").hide();
        }
    })
})