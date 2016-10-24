<!doctype html>
<head>
<meta charset="utf-8" />
<title>$page_title</title>
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
<a href="/bug">返回bug列表</a>
</header>
<div id="main" role="main">
<div id="exhibit">
<h1>{{bug['id']}}-{{bug['title']}}</h1> <input type="button" value="编辑" id="editBug" /> <!-- input type="button" value="删除" id="deleteBug" / -->
<br />
程度: {{bug['priority']}}
<br />
状态: {{bug['status']}}
<br />
描述：
<br />
{{!bug['description'].replace('\n', '<br />')}}
<div>
%for i in image:
<img src="/img/{{i[2].encode('utf8')}}" width=200px height=200px />
%end
</div>
</div>
<div id="edit">
<h1 id="id">{{bug['id']}}</h1>
问题：<input type="text" value="{{bug['title']}}" id="title" />
<br />
程度：<input type="text" value="{{bug['priority']}}" id="priority"> </input>
<br />
状态：<input type="text" value="{{bug['status']}}" id="status"> </input>
<br />
<textarea id="description" rows="10" cols="60">{{bug['description']}}</textarea>
<br />
<input id="updateBug" type="button" value="保存"/> 
<input id="cancel" type="button" value="取消"/>
<br />
<form form method="post" action="" enctype="multipart/form-data">
<input type="file" name="file" id="newImage" />
<div id="accessory">
%for i in image:
<div>
<img src="/img/{{i[2].encode('utf8')}}" width=200px height=200px />'
<a href="/image/delete/{{str(i[0])}}">删除</a>
</div>'
<br />
%end
</div>
<script type="text/javascript">
$(document).ready(function() {
        $("#exhibit").show();
        $("#edit").hide();
        $("#editBug").click(function() {
            $("#exhibit").hide();
            $("#edit").show();
            });
        $("#deleteBug").click(function() {
            if (confirm("删除此项目?")) {
            }
            });
        $("#cancel").click(function() {
            $("#exhibit").show();
            $("#edit").hide();
            });
        $("#updateBug").click(function() {
            $("#edit").hide();
            var id = $("#id").html();
            var title = document.getElementById("title").value;
            var priority= document.getElementById("priority").value;
            var status = document.getElementById("status").value;
            var description = $("#description").val();
            $.post("/bug/update", {"id":id, "title":title, "priority":priority, "status":status, "description":description}, function() {
                window.location.reload();
                });
            });
        $("#newImage").AjaxFileUpload({
action: "/image/new",
bugid:{{bug['id']}},
onComplete: function(filename, response) {
var response = $.parseJSON(response);
$("#accessory").append(
    $("<img />").attr("src", response.filename).attr("width", 200).attr("height", 200)
    );
$("#accessory").append($("<br />"));
$("#accessory").append(
    $("<a />").attr("href", "/image/delete/".concat(response.id)).html("删除")
    );
}
});
});
var button = '<input type="button" value="Save" class="saveButton" /> <input type="button" value="Cancel" class="cancelButton"/>';
</script>
<footer>
</footer>
</div>
</body>
</html>
