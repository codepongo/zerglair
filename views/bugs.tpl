<!doctype html>
<head>
<meta charset="utf-8" />
<title>问题列表</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<script src="/js/jquery-1.6.4.min.js"></script>
<script src="/js/jquery.ajaxfileupload.js"></script>
<style>
table{width:100%;table-layout:fixed;empty-cells:show;border-collapse:collapse;}code {white-space:pre-wrap; /* css3.0 <em>/ white-space:-moz-pre-wrap; /</em> Firefox <em>/ white-space:-pre-wrap; /</em> Opera 4-6 <em>/ white-space:-o-pre-wrap; /</em> Opera 7 <em>/ word-wrap:break-word; /</em> Internet Explorer 5.5+ */ }
th {
color:white;
	  background-color:gray;
}
td {
	border-color:gray;
}
body {background-color: #fff; border: 0px solid #ddd; padding: 15px; margin: 15px;}
pre {background-color: #eee; border: 0px solid #ddd; padding: 5px;}
</style>
</head>
<body>
<div id="container">
<header>
</header>
<div id="main" role="main">
<table border=1>
<tr><th width="70%">问题</th><th>程度</th><th>状态</th></tr>
%for bug in bugs:
	<tr><td><a href="/bug/{{bug[0]}}">{{bug[1]}}</a></td><td>{{bug[2]}}</td><td>{{bug[3]}}</td></tr>
%end
<tr id="save_bug_area"><td colspan="3"><input type="text" placeholder="Bug Title" id="BugTitle" /><input type="button" value="保存" id="saveBug"/><input type="button" value="取消" id="cancelBug"/></td></tr>
<tr id="new_bug_area"><td colspan="3"><input type="button" value="new bug" id="newBug" /></td></tr>
</table>
<script type="text/javascript">
$(document).ready(function(){
    $("#new_bug_area").show();
    $("#save_bug_area").hide();
    $("#newBug").click(function() {
        $("#new_bug_area").hide();
        $("#save_bug_area").show();
        $("#BugTitle").focus();
    })
    $("#saveBug").click(function() {
        var bug = document.getElementById("BugTitle").value
        if(bug != "") {
            $.post("/bug/new", bug, function() {
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
})
</script>
</div>
<footer>
</footer>
</div>
</body>
</html>

