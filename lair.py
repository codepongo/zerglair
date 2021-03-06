#encoding:utf8
import conf
import bottle
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
import datetime
import xlwt


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

@get('/')
@get('/project')
def query_prj():
    projects = db.exec_cmd(conf.def_dbname, 'select rowid, * from project where recovery=0 order by datetime')
    return template('projects', projects=projects)

@post('/project/new')
def new_project():
    title = unicode(request.body.read(), 'utf8')
    prj = db.exec_cmd(conf.def_dbname, 'select rowid, * from project where name="%s"' % (title))
    output(prj)
    
    if prj != None and len(prj) != 0:
        db.exec_cmd(conf.def_dbname, 'update project set recovery=0, datetime=? where name=?', (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), title))
    else:
        db.exec_cmd(conf.def_dbname, 'insert into project values(?,?,?)', (title, 0, datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    return ''

@get('/bug')
def query_bug():
    sql = 'select rowid, * from bug'
    prjid = request.GET.get('prjid', '')
    project = (None, '')
    if prjid != '':
        sql += ' where projectid=%s' % (prjid)
        project = db.exec_cmd(conf.def_dbname, 'select rowid, name from project where rowid = %s' % (prjid))[0]
    bugs = db.exec_cmd(conf.def_dbname, sql)
    return template('bugs', project=project, bugs=bugs)

@get('/project/:prjid/bug')
def query_bug(prjid):
    project = db.exec_cmd(conf.def_dbname, 'select rowid, name from project where rowid = %s' % (prjid))
    bugs = db.exec_cmd(conf.def_dbname, 'select rowid, * from bug where project = %s' % (prjid))
    return template('bugs', project=project[0], bugs=bugs)

@post('/project/:projectid/delete')
def delete_project(projectid):
    db.exec_cmd(conf.def_dbname, 'update project set recovery=1 where rowid=?', (projectid, ))

@get('/project/:projectid/export')
def save_as_excel(projectid):
    project = db.exec_cmd(conf.def_dbname, 'select rowid, name from project where rowid = %s' % (projectid))
    bugs = db.exec_cmd(conf.def_dbname, 'select rowid, * from bug where projectid = %s' % (projectid))    
    date_style = xlwt.easyxf(num_format_str='YYYY-MM-DD')
    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'问题列表')
    ws.write(0, 0, u'编码');
    ws.write(0, 1, u'标题');
    ws.write(0, 2, u'程度');
    ws.write(0, 3, u'状态');
    ws.write(0, 4, u'描述');
    for j in range(0, len(bugs)):
        for i in range(0, len(bugs[j])-1):
            ws.write(j+1, i, bugs[j][i])
    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    wb.save('export/%s.xls' % (name))
    return bottle.static_file(name+'.xls', root='export')

@post('/bug/update')
def update_bug():
    output(request.body.read())
    bug = {}
    bug['title'] = unicode(request.forms.get('title'), 'utf8')
    bug['priority'] = unicode(request.forms.get('priority'), 'utf8')
    bug['status'] = unicode(request.forms.get('status'), 'utf8')
    bug['description'] = unicode(request.forms.get('description'), 'utf8')
    bug['rowid'] = unicode(request.forms.get('id'), 'utf8')
    output(bug)
    db.exec_cmd(conf.def_dbname, 'update bug set name=?, priority=?, status=?, description=? where rowid=?', (bug['title'], bug['priority'], bug['status'], bug['description'], bug['rowid']))

@post('/bug/new')
def new_bug():
    title = unicode(request.forms.get('bug'), 'utf8')
    project = unicode(request.forms.get('project'), 'utf8')
    db.exec_cmd(conf.def_dbname, 'insert into bug values(?,?,?,?,?)', (title, u"请加入问题的详细描述。 \n\n有效的问题描述包括三方面内容： \n\n* 产生步骤 \n\n* 期望结果 \n\n* 实际结果\n\n", '', u'新建', project))
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
    b['description'] = bug[2].encode('utf8')
    b['priority'] = bug[3].encode('utf8')
    b['status'] = bug[4].encode('utf8')
    b['project'] = bug[5]
    return template('bug', bug=b, image=image)



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
    

@post('/image/delete/:id')
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

@get('/css/:filename')
def send_css(filename = ""):
    ''' send any requested file'''
    if os.path.exists(filename):
        response.content_type = "text/css"
        return open(filename, "rb").read()
    return ''

@get('/js/:filename')
def send_js(filename = ""):
    ''' send any requested file'''
    if os.path.exists(filename):
        response.content_type = "text/javascript"
        return open(filename, "rb").read()
    return ''

if not os.path.isdir('export'):
    os.mkdir('export')
db.exec_cmd(conf.def_dbname, conf.project_table)
db.exec_cmd(conf.def_dbname, conf.bug_table)
#db.exec_cmd(conf.def_dbname, conf.wiki_table)
db.exec_cmd(conf.def_dbname, conf.image_table)
if not os.path.isdir('img'):
    os.mkdir('img')
run(host='', port=8080, debug=True,reload=True)

