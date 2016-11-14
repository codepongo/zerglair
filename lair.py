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

@get('/')
@get('/project')
def query_prj():
    projects = db.exec_cmd(conf.def_dbname, 'select rowid, * from project')
    return template('projects', projects=projects)

@get('/bug')
def query_bug():
    bugs = db.exec_cmd(conf.def_dbname, 'select rowid, * from bug')
    return template('bugs', bugs=bugs)

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

db.exec_cmd(conf.def_dbname, conf.project_table)
db.exec_cmd(conf.def_dbname, conf.bug_table)
#db.exec_cmd(conf.def_dbname, conf.wiki_table)
db.exec_cmd(conf.def_dbname, conf.image_table)
if not os.path.isdir('img'):
    os.mkdir('img')
run(host='', port=8080, debug=True,reload=True)

