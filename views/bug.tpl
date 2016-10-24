<!doctype html>
<head>
<meta charset="utf-8" />
<title>问题</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<script src="/js/jquery-1.6.4.min.js"></script>
<script src="/js/jquery.ajaxfileupload.js"></script>
<link rel="Stylesheet" type="text/css" href="/css/weui.min.css" />
<style>
body {font-family:-apple-system-font,Helvetica Neue,Helvetica,sans-serif; border: 0px solid #ddd; padding: 15px; margin: 15px;}
</style>
</head>
<body>
<input class="weui-btn weui-btn_mini weui-btn_default" type="button" value="返回问题列表" id="return" />
<input class="weui-btn weui-btn_mini weui-btn_primary" type="button" value="编辑" id="editBug" />
<div class="weui-cells" id="exhibit">
<div class="weui-cell">
<label class="weui-label">标题</label>
{{bug['title']}}
</div>
<div class="weui-cell">
<label class="weui-label">编号</label>
{{bug['id']}}
</div>
<div class="weui-cell">
<label class="weui-label">程度</label>
{{bug['priority']}}
</div>
<div class="weui-cell">
<label class="weui-label">状态</label>
{{bug['status']}}
</div>
<div class="weui-cell">
<label class="weui-label">描述</label>
{{!bug['description'].replace('\n', '<br />')}}
</div>
%for i in image:
<div class="weui-cell">
<img src="/img/{{i[2].encode('utf8')}}" width=200px height=200px />
</div>
%end
</div>
<div id="edit">
<div class="weui-cells">
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">编号</label></div><div class="weui-cell__bd" id="id">{{bug['id']}}</div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">问题</label></div>
<div class="weui-cell__bd"><input class="weui-input" type="text" value="{{bug['title']}}" id="title"></div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">程度</label></div>
<div class="weui-cell__bd"><input class="weui-input" type="text" value="{{bug['priority']}}" id="priority"></div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">状态</label></div>
<div class="weui-cell__bd"><input class="weui-input" type="text" value="{{bug['status']}}" id="status"></div>
</div>
<div class="weui-cell">
<div class="weui-cell__hd"><label class="weui-label">状态</label></div>
<textarea id="description" class="weui-textarea" rows="10">{{bug['description']}}</textarea>
</div>
<div class="weui-cell">
<input class="weui-btn weui-btn_primary" id="updateBug" type="button" value="保存"/> 
</div>
<div class="weui-cell">
<input class="weui-btn weui-btn_default" id="cancel" type="button" value="取消"/>
</div>
</div>

<div id="accessory">
<div class="weui-cells">
<div class="weui-cell"><div class="weui-uploader__input-box">
<input class="weui-uploader__input" type="file" name="file" id="newImage" />
</div></div>
<script type="text/javascript">
        function deleteImage(o) {
            if (confirm("删除此图片?")) {
            $.post("/image/delete/"+o.id, null, function() {
                o.parentNode.parentNode.parentNode.removeChild(o.parentNode.parentNode);
                $("#editBug").click();
            });
            
            }
        };
</script>
%for i in image:
<div class="weui-cell">
<div class="weui-cell__bd"><img src="/img/{{i[2].encode('utf8')}}"/></div>
<div class="weui-cell__ft"><input class="weui-btn weui-btn_warn" type="button" id="{{str(i[0])}}" value="删除图片" onClick="deleteImage(this)"/></div>
</div>
%end
</div>
</div>
<script type="text/javascript">
$(document).ready(function() {
        $("#exhibit").show();
        $("#edit").hide();
        $("#return").click(function() {
            window.location.href="/bug";
            });
        $("#editBug").click(function() {
            $("#exhibit").hide();
            $("#edit").show();
            });
        $("#deleteBug").click(function() {
            if (confirm("删除此项目?")) {
            }
            });
        $("#cancel").click(function() {
            window.location.reload();
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
var node = $("<div />").attr("class", "weui-cell").html("<div class=\"weui-cell__bd\"><img src=\""+response.filename+"\" /></div><div class=\"weui-cell__ft\"><input class=\"weui-btn weui-btn_warn\" type=\"button\" id="+response.id+" value=\"删除图片\" onClick=\"deleteImage(this)\"/></div>");
$("#accessory").append(node);
}
});
});
var button = '<input type="button" value="Save" class="saveButton" /> <input type="button" value="Cancel" class="cancelButton"/>';
</script>
<footer>
</footer>
</body>
</html>
