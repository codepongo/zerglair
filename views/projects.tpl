<!doctype html>
<head>
<meta charset="utf-8" />
<title>项目</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="Stylesheet" type="text/css" href="/css/weui.min.css" />
<script src="/js/jquery-1.6.4.min.js"></script>
<script src="/js/jquery.ajaxfileupload.js"></script>
<style>
body {font-family:-apple-system-font,Helvetica Neue,Helvetica,sans-serif; border: 0px solid #ddd; padding: 15px; margin: 15px;}
</style>
</head>
<body>
<h1>
项目列表
</h1>
<div class="weui-cells">
<div class="weui-cell">
<div class="weui-cell__bd"><p>项目</p></div>
</div>
</div>
%if projects != None:
%   for project in projects:
<a class="weui-cell weui-cell_access" href="/bug?prjid={{project[0]}}">
<div class="weui-cell__bd"><p>{{project[1]}}</p></div>
<div class="weui-cell__ft"></div>
</a>
%   end
%end
<div id="save_project_area" class="weui-cell">
<div class="weui-cell__bd"><input id="new_project_title" class="weui-input" type="text" placeholder="请输入问题名称"></div>
<div class="weui-cell__ft">
<input class="weui-btn weui-btn_mini weui-btn_primary" type="button" value="保存" id="saveBug"/>
<input class="weui-btn weui-btn_mini weui-btn_default" type="button" value="取消" id="cancelBug"/>
</div>
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
</body>
</html>

