/**
 * Created by wyf on 2017/7/31.
 */

//点击“X”退出创建资产窗口
$("#cancel").click(function () {
    $(this).parent().addClass("hide");
    $(this).parent().prev().addClass("hide");
});

//点击“X”退出更新资产窗口
$("#cancel-1,#cancel-2").click(function () {
    $(".update").addClass("hide");
    $(".shade").addClass("hide");
    // $(this).parent().addClass("hide");
    // $(this).parent().prevAll(".shade").addClass("hide");
});


//点击“创建”新增加一条资产信息事件
$("#create-btn").click(function () {
    var value_list = [];
    var $new_tr=$(".odd").first().clone();
    $new_tr.removeClass("hide"); //删除模板tr的hide
    $(".model .input-info input").each(function () {
        // console.log($(this).val());
        value_list.push($(this).val());
    });
    // console.log(value_list);
    $($new_tr.children(".var")).each(function (i) {
        $(this).text(value_list[i]);
    });

    $(".table").append($new_tr);
    $(".shade").addClass("hide");
    $(".model").addClass("hide");
});


$login_user=$(".left-menu-header").children().text().slice(8,-1);
$update_target="";
$eles = $(".update .input-info input,.update .input-info select");
// console.log($eles);

$(".table").on("click",".btn_asset_update",function (event){
    $('.input-box .error').remove();
    $update_target=$(event.target);
    // var id=$(event.target).parent().siblings(".hide").eq(0).text();
    $eles.each(function (k) {
        $(this).val($(event.target).parent().siblings(".var").eq(k).text());
    });
    // $.ajax({
    //     url:"/bms/mod_asset/"+id+"/",
    //     type:"GET",
    //     data:"",
    //     datatype:"JSON",
    //     success:function (arg) {
    //         console.log(arg)
    //     }
    // });
    
    $(".update").removeClass("hide");
    $(".shade").removeClass("hide");
    // var id=$update_target.parent().siblings(".hide").eq(0).text();
    // console.log(id);
    // $("form").prop("action","/bms/mod_asset/"+id+"/");
    // console.log($("form"));
});
$("#create-btn-1").click(function () {
    // console.log($update_target);
    var id=$update_target.parent().siblings(".hide").eq(0).text();
    // console.log(id);
    var hostname=$eles.eq(0).val();
    var ip=$eles.eq(1).val();
    var port=$eles.eq(2).val();
    var model=$eles.eq(3).val();
    var env=$eles.eq(4).val();
    var hardware=$eles.eq(5).val();
    var admin=$eles.eq(6).val();
    if ($login_user=='admin'){    //如果当前登录用户为admin，前端显示更改后的admin字段
        admin=$eles.eq(6).val();
    }else{                        //若是其他用户，前端显示当前的admin字段
        admin=$update_target.parent().siblings(".var").eq(6).text();
    }
    console.log(admin);
    var $asset_info=[hostname,ip,port,model,env,hardware,admin];
    // console.log(hostname,ip,port,model,env,hardware,admin);
    // $update_target.parent().siblings(".var").each(function (k) {
    //     $(this).text($asset_info[k]);   //在前端页面上显示更改的数据
    // });
    $('.input-box .error').remove();
    $.ajax({
        url:"/bms/mod_asset/"+id+"/",
        type:"POST",
        headers:{"X-CSRFToken": $.cookie('csrftoken')},
        data:$(".input-box").serialize(),
        dataType:'JSON',
        success:function (arg) {
            // console.log(arg);
            if(arg.status){
                $(".update").addClass("hide");
                $(".shade").addClass("hide");
                $update_target.parent().siblings(".var").each(function (k) {
                    $(this).text($asset_info[k]);   //在前端页面上显示更改的数据
                });
                // location.href = "/bms/index/";
            }else{
                console.log(arg.msg);
            /*
            arg.msg = {
                email: ['xxxxx',]
                password: ['xxxxx',]
                user: ['xxxxx',]
            }
             */
            $.each(arg.msg,function (k,v) {

                var tag = document.createElement('span');
                tag.innerHTML = v[0];
                tag.className = "error";
                tag.style = "color:deepskyblue;position:absolute;left:25%;top:35px";
                // console.log(tag);
                // <span class='error'>v[0]</span>
                //$('#login_btn').before(tag);
                $('.input-info input[name="'+k+'"],.input-info select[name="'+k+'"]').after(tag);
            })
        }
            
        }
    });
    // $(".update").addClass("hide");
    // $(".shade").addClass("hide");

    // $update_target.parent().siblings(".var").each(function (k) {
    //     // console.log($eles.eq(k).val());
    //     $(this).text($eles.eq(k).val())
    // })

});

// “删除”按钮触发事件
$(".table").on("click",".btn_asset_delete",function () {
    // $(".del-box").removeClass("hide");
    // $(".shade").removeClass("hide");
    // console.log($(this).parent().parent().find(".itpt_check"));
    // var flag = false;
    $del_target = $(this);
    asstid = $(this).attr("assetid");
    checked_var= $(this).parent().parent().find(".ipt_check").prop("checked");
    if(checked_var){
        $(".del-box").removeClass("hide");
        $(".shade").removeClass("hide");
        // $(this).parent().parent().remove(); //仅限前端删除
        // //利用ajax以get方式提交到后端，实现异步删除
        // $.ajax({
        //     url:"/bms/del_asset/",
        //     type:"GET",
        //     headers:{"X-CSRFToken": $.cookie('csrftoken')}, //请求头中携带csrftoken,实现防跨站
        //     data:{id:asstid,checked:checked_var}
        // });

        // flag = true;
        // $(this).prop("href","/bms/del_asset/?id="+asstid+"&checked="+checked_var);
        //加入判断，如果checked=true，才修改href属性，才会刷新页面，否则没有href点击<a>不会导致页面刷新
    }
    // alert(flag);
    // alert(checked_var);
    // $(this).prop("href","/bms/del_asset/?id="+asstid+"&checked="+checked_var);
     // $.get("/bms/del_asset/?id="+asstid+"&checked="+checked_var, function(result){
     //  });  // 利用ajax传递get
});

$(".del-box .btn-default").click(function () {
    $(".del-box").addClass("hide");
    $(".shade").addClass("hide");
});

$(".del-box .btn-danger").click(function () {
    $del_target.parent().parent().remove();
    $.ajax({
        url:"/bms/del_asset/",
        type:"GET",
        headers:{"X-CSRFToken": $.cookie('csrftoken')}, //请求头中携带csrftoken,实现防跨站
        data:{id:asstid,checked:checked_var}
    });
    $(".del-box").addClass("hide");
    $(".shade").addClass("hide");
});




//"批量删除"按钮绑定事件
$("#del").click(function () {
    var $del_list=[];

    $(".ipt_check:checked").parents(".odd").children(".asset_id").each(function (k) {
        $del_list.push($(this).text())
    });
    // console.log($del_list);
    $(".ipt_check:checked").parents(".odd").remove();
    $.ajax({
        url:"/bms/batch_del/",
        type:"POST",
        data:{del_list:JSON.stringify($del_list)},
        headers:{"X-CSRFToken": $.cookie('csrftoken')},
        success:function (data) {
            alert(data)
        }
    })
});

//checkbox正反选绑定事件
$(".top_tr .ipt_check").click(function () {
    // console.log($(".top_tr .ipt_check").prop("checked"));
    if($(".top_tr .ipt_check").prop("checked")){
        $("[class='odd'] .ipt_check").prop("checked",true)
    }
    else{
        $("[class='odd'] .ipt_check").prop("checked",false)
    }
});

//
// $(".pagination li a").click(function () {
//     $page_num=$(this).text();
//     console.log($page_num);
//     $.ajax({
//         url:'/bms/index/',
//         type:'GET',
//         data:{page_num:$page_num},
//         success:function (data) {
//             console.log(JSON.parse(data))
//         }
//     })
//
// });

// $("#search_icon").click(function () {
//     $.ajaxSetup({
//         data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
//     });
//     var $search_str=$(this).parent().siblings("input").val();
//     console.log($search_str);
//     $.ajax({
//         url:"/bms/index/",
//         type:"POST",
//         data:{search_str:$search_str}
//     })
// });

$(".ajax_test").click(function () {
    $.ajax({
        url:"/bms/ajax/",
        type:"POST",
        data:{test:"test"},
        headers:{"X-CSRFToken": $.cookie('csrftoken')},
        success:function (data) {
            alert(data)
        }
    })
});

$(".table").on("click","#terminal_event",function () {
    $.ajax({
        url:"/bms/applications/terminal/",
        type:"POST",
        data:{hostip:$(this).text(),hostuser:"root",hostpwd:"teamsun"},
        headers:{"X-CSRFToken": $.cookie('csrftoken')},
        success:function (data) {
            
        }
    })
});