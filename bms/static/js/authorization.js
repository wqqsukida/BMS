/**
 * Created by wyf on 2017/9/13.
 */
/**
 * Created by wyf on 2017/7/31.
 */

//点击“X”退出更新用户产窗口
$("#b-cancel-1,#b-cancel-2").click(function () {
    $(".mod_bussiness").addClass("hide");
    $(".shade").addClass("hide");
});
// 得到当前登录用户名
$login_user=$(".left-menu-header").children().text().slice(8,-1);
// 定义当前操作按钮
$update_target="";
// 修改用户权限模态对话框下的所有input,select标签
$eles = $(".mod_bussiness .input-info input,.mod_bussiness .input-info textarea");
// console.log($eles);

//点击每条记录的"管理"按钮触发事件
$(".table").on("click",".btn_bussiness_update",function (event){
    $('.input-box .error').remove();
    $update_target=$(event.target);
    // var id=$(event.target).parent().siblings(".hide").eq(0).text();
    $eles.each(function (k) {
        $(this).val($(event.target).parent().siblings(".var").eq(k).text());
    });
    $(".mod_bussiness").removeClass("hide");
    $(".shade").removeClass("hide");
    // var id=$update_target.parent().siblings(".hide").eq(0).text();
    // console.log(id);
    // $("form").prop("action","/bms/mod_asset/"+id+"/");
    // console.log($("form"));

});

//点击模态对话框的更新按钮触发事件
$("#mod_bussiness_btn").click(function () {
    // console.log($update_target);
    var id=$update_target.parent().siblings(".hide").eq(0).text();
    // console.log(id);
    var name=$eles.eq(0).val();
    var decription=$eles.eq(1).val();
    if ($login_user=='admin'){    //如果当前登录用户为admin，前端显示更改后的业务线字段
        name=$eles.eq(0).val();
    }else{                        //若是其他用户，前端显示当前的业务线字段
        name=$update_target.parent().siblings(".var").eq(0).text();
    }
    console.log(name);
    var $asset_info=[name,decription];
    $('.input-box .error').remove();
    $.ajax({
        url:"/bms/authorization/"+id+"/",
        type:"POST",
        headers:{"X-CSRFToken": $.cookie('csrftoken')},
        data:$(".input-box").serialize(), //form表单post的所有数据
        dataType:'JSON', //自动序列化为JSON
        success:function (arg) {
            // console.log(arg);
            if(arg.status){  //后端接收后处理判定是有效数据
                $(".mod_bussiness").addClass("hide");
                $(".shade").addClass("hide");
                $update_target.parent().siblings(".var").each(function (k) {
                    $(this).text($asset_info[k]);   //在前端页面上显示更改的数据
                });
                // location.href = "/bms/index/";
            }else{ //判定不是有效数据,返回false和error
                console.log(arg.msg);
            /*
            arg.msg = {
                email: ['xxxxx',]
                password: ['xxxxx',]
                user: ['xxxxx',]
            }
             */
            $.each(arg.msg,function (k,v) {
                //在每个input后生成错误信息标签
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
});

// “删除”按钮触发事件
$(".table").on("click",".btn_bussiness_delete",function () {
    // console.log($(this).parent().parent().find(".itpt_check"));
    // var flag = false;
    $del_bussiness_target = $(this);
    bid = $(this).attr("bid");
    checked_var= $(this).parent().parent().find(".ipt_check").prop("checked");
    if(checked_var){
        $(".del-bussiness").removeClass("hide");
        $(".shade").removeClass("hide");
    //     $(this).parent().parent().remove(); //仅限前端删除
    //     //利用ajax以get方式提交到后端，实现异步删除
    //     $.ajax({
    //         url:"/bms/del_user/",
    //         type:"GET",
    //         headers:{"X-CSRFToken": $.cookie('csrftoken')}, //请求头中携带csrftoken,实现防跨站
    //         data:{id:asstid,checked:checked_var}
    //     });
    }
});

$(".del-bussiness .btn-default").click(function () {
    $(".del-bussiness").addClass("hide");
    $(".shade").addClass("hide");
});

$(".del-bussiness .btn-danger").click(function () {

    $.ajax({
        url:"/bms/del_bussiness/",
        type:"POST",
        headers:{"X-CSRFToken": $.cookie('csrftoken')}, //请求头中携带csrftoken,实现防跨站
        data:{id:bid,checked:checked_var},
        dataType:'JSON',
        success:function (arg) {
            // console.log(arg);
            if (arg.status){
                $del_bussiness_target.parent().parent().remove();
                alert(arg.msg)
            }else{
                alert(arg.msg)
            }
        }
    });
    $(".del-bussiness").addClass("hide");
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
        url:"/bms/del_users/",
        type:"POST",
        data:{del_list:JSON.stringify($del_list)},
        headers:{"X-CSRFToken": $.cookie('csrftoken')},
        success:function (data) {
            alert(data)
        }
    })
});


