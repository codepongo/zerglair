<!doctype html>
<head>
<meta charset="utf-8" />
<title>问题列表</title>
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
<input class="weui-btn weui-btn_mini weui-btn_default" type="button" value="返回项目列表" id="return" />
{{project[1]}}  问题列表
<input class="weui-btn weui-btn_mini weui-btn_primary" type="button" value="导出Excel" id="saveAsExcel">
<input class="weui-btn weui-btn_mini weui-btn_warn" type="button" value="删除" id="deleteProject">
</h1>
<div class="weui-cells">
<div class="weui-cell">
<div class="weui-cell__hd"><p>[状态]</p></div>
<div class="weui-cell__bd"><p>问题</p></div>
<div class="weui-cell__ft">程度</div>
</div>
</div>
%if bugs != None:
%   for bug in bugs:
<a class="weui-cell weui-cell_access" href="/bug/{{bug[0]}}">
%       if bug[4] != '':
%           priority = bug[4]
%       else:
%           priority = '未知'
%       end
<div class="weui-cell__hd"><p style="color:#999;margin-right:5px;">[{{!priority}}]</p></div>
<div class="weui-cell__bd"><p>{{bug[1]}}</p></div>
<div class="weui-cell__ft">{{bug[3]}}</div>
</a>
%   end
%end
<div id="save_bug_area">
<input id="new_bug_title" class="weui-input" type="text" placeholder="请输入问题名称">
<input style="margin-top:5px" class="weui-btn weui-btn_primary" type="button" value="保存" id="saveBug"/>
<a style="margin-top:5px" class="weui-btn weui-btn_default" id="cancelBug">取消</a>
</div>
<div id="new_bug_area">
<input class="weui-btn weui-btn_primary" type="button" value="新建问题" id="newBug" />
</div>
<script type="text/javascript">
$(document).ready(function(){
        $("#new_bug_area").show();
        $("#save_bug_area").hide();
        $("#newBug").click(function() {
            $("#new_bug_area").hide();
            $("#save_bug_area").show();
            $("#new_bug_title").focus();
            })
        $("#saveBug").click(function() {
            var bug = document.getElementById("new_bug_title").value
            if(bug != "") {
            $.post("/bug/new", {'project':{{project[0]}},'bug':bug}, function() {
                window.location.reload();
                });
            } else {
            $("#BugTitle").focus();
            $("#BugTitle").css('border','1px solid red');
            }
            });
        $("#cancelBug").click(function() {
            $("#new_bug_area").show();
            $("#save_bug_area").hide();
            });
        $("#deleteProject").click(function() {
            if (confirm("删除此项目?")) {
            $.post("/project/"+{{project[0]}}+"/delete", null, function() {
                window.location.href = "/";
            });
            }
            });
        $("#saveAsExcel").click(function() { 
            window.location.href = "/project/{{project[0]}}/export";
        });
        $("#return").click(function() {
            window.location.href="/project";
        });
})
</script>
<footer>
</footer>
</body>
</html>

