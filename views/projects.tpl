<!doctype html>
<head>
<meta charset="utf-8" />
<title>项目</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="Stylesheet" type="text/css" href="/css/mobi.css" />
<link rel="Stylesheet" type="text/css" href="/css/weui.min.css" />
<script src="/js/jquery-1.6.4.min.js"></script>
<script src="/js/jquery.ajaxfileupload.js"></script>
</head>
<body>
<div class="flex-center">
<div class="container">
<h1 class="flex-center flex-middle">
项目列表
</h1>
<div class="weui-cell">
项目
</div>
%if projects != None:
%   for project in projects:
<a class="weui-cell weui-cell_access" href="/bug?prjid={{project[0]}}">
<div class="weui-cell__bd"><p>{{project[1]}}</p></div>
<div class="weui-cell__ft"></div>
</a>
%   end
%end
<div id="save_project_area">
<input id="new_project_title" class="weui-input" type="text" placeholder="请输入问题名称">
<input style="margin-top:5px" class="weui-btn weui-btn_primary" type="button" value="保存" id="saveBug"/>
<a style="margin-top:5px" class="weui-btn weui-btn_default" id="cancelBug">取消</a>
</div>
<div id="new_project_area">
<input class="weui-btn weui-btn_primary" type="button" value="新建项目" id="newBug" />
</div>
<script type="text/javascript">
$(document).ready(function(){
        $("#new_project_area").show();
        $("#save_project_area").hide();
        $("#newBug").click(function() {
            $("#new_project_area").hide();
            $("#save_project_area").show();
            $("#new_project_title").focus();
            })
        $("#saveBug").click(function() {
            var project = document.getElementById("new_project_title").value
            if(project != "") {
            $.post("/project/new", project, function() {
                window.location.reload();
                });
            } else {
            $("#BugTitle").focus();
            $("#BugTitle").css('border','1px solid red');
            }
            });
        $("#cancelBug").click(function() {
            $("#new_project_area").show();
            $("#save_project_area").hide();
            });
})
</script>
<footer>
</footer>
</div>
<aside class="hide-on-mobile" style="padding:0 28px">
<p>adv</p>
</aside>
</div>
</body>
</html>

