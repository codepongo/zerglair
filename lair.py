#encoding:utf8
import conf
from bottle import route, get, post, request, response, run, _stderr, hook, redirect, template
import json
import db
import datetime
import copy
import time
import sys
import os
import hashlib
import shutil


@hook('before_request')
def output_request():
    return
    output(request.path)
    output(request.method)
    output('=header=')
    for k,v in request.headers.items():
        output('%s: %s' % (k, v))
    output('=cookie=')
    for k,v in request.cookies.items():
        output('%s: %s' % (k, v))
    output('=body=')
    output(request.body.read())
    output(request.body.read().decode('utf8'))

def timestamp():
    timestamp = str(time.time())
    return timestamp.replace('.', '')

def output(x):
    if type(x) == unicode:
        x = x.encode('gbk')
    return _stderr(str(x)+'\n')

@get('/bug')
def query_bug():
    title = ''
    header = ''
    body_front = u'''
<table border=1>
<tr><th width="70%">问题</th><th>程度</th><th>状态</th></tr>
'''
    body_behind = u'''
<tr id="new_bug_area"><td colspan="3"><input type="button" value="new bug" id="newBug" /></td></tr>
<tr id="save_bug_area"><td colspan="3"><input type="text" placeholder="Bug Title" id="BugTitle" /><input type="button" value="保存" id="saveBug"/><input type="button" value="取消" id="cancelBug"/></td></tr>
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
'''
    bugs = db.exec_cmd(conf.def_dbname, 'select rowid, * from bug')
    idx = 0
    for bug in bugs:
        body_front += '<tr><td><a href="/bug/%s">%s</a></td><td>%s</td><td>%s</td></tr>' % bug[:4]
    template = open('template.html', 'rb').read()
    return template.replace('$page_title', title).replace('$page_header', header).replace('$page_body', body_front+body_behind)

@post('/bug/update')
def update_bug():
    output(request.body.read())
    bug = {}
    bug['title'] = unicode(request.forms.get('title'), 'utf8')
    bug['priority'] = unicode(request.forms.get('priority'), 'utf8')
    bug['status'] = unicode(request.forms.get('status'), 'utf8')
    bug['description'] = unicode(request.forms.get('description'), 'utf8')
    bug['rowid'] = unicode(request.forms.get('id'), 'utf8')
    db.exec_cmd(conf.def_dbname, 'update bug set name=?, priority=?, status=?, description=? where rowid=?', (bug['title'], bug['priority'], bug['status'], bug['description'], bug['rowid']))

@post('/bug/new')
def new_bug():
    title = unicode(request.body.read(), 'utf8')
    db.exec_cmd(conf.def_dbname, 'insert into bug values(?,?,?,?)', (title, '', u'新建', u"请加入问题的详细描述。 \n\n有效的问题描述包括三方面内容： \n\n* 产生步骤 \n\n* 期望结果 \n\n* 实际结果\n\n"))
    return ''

@get('/bug/:bugid')
def edit_bug(bugid = ""):
    bug = (0, u"", u"", u"", u"")
    if bugid != "":
        bug = db.exec_cmd(conf.def_dbname, 'select rowid, * from bug where rowid='+bugid)[0]
        image = db.exec_cmd(conf.def_dbname, 'select rowid, * from image where bugid='+bugid)


    b = {}
    b['id'] = bug[0]
    b['title'] = bug[1].encode('utf8')
    b['priority'] = bug[2].encode('utf8')
    b['status'] = bug[3].encode('utf8')
    b['description'] = bug[4].encode('utf8')
    return template('bug', bug=b, image=image)

    exhibit = '''
<div id="exhibit">
<h1>%d-%s</h1> <input type="button" value="编辑" id="editBug" /> <!-- input type="button" value="删除" id="deleteBug" / -->
<br />
程度:%s
<br />
状态:%s
<br />
%s''' % bug
    accessory = '<div>'
    for i in image:
        accessory += '<img src="/img/'+i[2].encode('utf8') +'" width=200px height=200px />'
    accessory += '</div>'
    exhibit = exhibit + accessory + '</div>'
    b = tuple(field.replace('<br />', '\n') if type(field) == str else field for field in bug)    
    edit = '''
<div id="edit">
<h1 id="id">%d</h1>
问题：<input type="text" value="%s" id="title" />
<br />
程度：<input type="text" value="%s" id="priority"> </input>
<br />
状态：<input type="text" value="%s" id="status"> </input>
<br />
<textarea id="description" rows="10" cols="60">%s</textarea>
<br />
<input id="updateBug" type="button" value="保存"/> 
<input id="cancel" type="button" value="取消"/>
<br />
<form form method="post" action="" enctype="multipart/form-data">
		<input type="file" name="file" id="newImage" />
		<div id="accessory">
''' % bug
    accessory = '<div>'
    for i in image:
        accessory += '<img src="/img/'+i[2].encode('utf8') +'" width=200px height=200px />'
        accessory += '<a href="/image/delete/'+str(i[0]) +'">删除</a>'
    accessory += '</div>'
    edit = edit + accessory + '''		</div>
	</form>
</div>'''
    script = '''
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
				bugid:%d,
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
''' % bug[0]
    xtemplate = open('template.html', 'rb').read()
    return xtemplate.replace('$page_title', 'edit bug').replace('$page_header', '').replace('$page_body', exhibit+edit+script)


@post('/image/new')
def new_image():
    upload = request.files.get('file')
    bugid = request.forms.get('bugid')
    upload.save('./', overwrite=True)
    with open(upload.filename, 'rb') as f:
        md5v = hashlib.md5(f.read()).hexdigest()
        name = os.path.join('img', md5v)
    shutil.move(upload.filename, name)
    if sys.platform == 'win32':
        name = name.replace('\\', '/')
    db.exec_cmd(conf.def_dbname, 'insert into image values(?,?)', (bugid, md5v))
    rowid = db.exec_cmd(conf.def_dbname, 'select rowid from image where md5="'+md5v+'"')[0][0]
    return json.dumps('{"filename":"/%s", "id":"%s"}' % (name, rowid))
    

@get('/image/delete/:id')
def delete_image(id = ""):
    if id != "":
        r = db.exec_cmd(conf.def_dbname, 'select bugid, md5 from image where rowid="'+id+'"')[0]
        output(r)
        filename = os.path.join('img', r[1])
        #os.remove(filename)
        db.exec_cmd(conf.def_dbname, 'delete from image where rowid="'+id+'"')
    return redirect('/bug/'+str(r[0]))
            
@get('/img/:filename')
def send_img(filename = ""):
    filename = os.path.join('img', filename)
    #os.path.splitpath(filename)[1]
    if os.path.exists(filename):
        #response.content_type = "image/x-png"
        return open(filename, "rb").read()
    return ''

@get('/js/:filename')
def send_js(filename = ""):
    ''' send any requested file'''
    if os.path.exists(filename):
        response.content_type = "text/javascript"
        return open(filename, "rb").read()
    return ''

db.exec_cmd(conf.def_dbname, conf.project_table)
db.exec_cmd(conf.def_dbname, conf.bug_table)
#db.exec_cmd(conf.def_dbname, conf.wiki_table)
db.exec_cmd(conf.def_dbname, conf.image_table)
if not os.path.isdir('img'):
    os.mkdir('img')
run(host='localhost', port=8080, debug=True,reload=True)

