import db
import conf
#print db.exec_cmd(conf.def_dbname, 'drop table project')
#print db.exec_cmd(conf.def_dbname, 'alter table bug add column project integer')
#print db.exec_cmd(conf.def_dbname, 'update bug set project=1')
#print db.exec_cmd(conf.def_dbname, 'select * from sqlite_master')
#print db.exec_cmd(conf.def_dbname, 'select * from bug')
#print db.exec_cmd(conf.def_dbname, 'alter table project rename to project_t')
#print db.exec_cmd(conf.def_dbname,  "create table project (name text unique, recovery integer);")
#print db.exec_cmd(conf.def_dbname, 'insert into project(name, recovery) selct name, remove from project_t')
#print db.exec_cmd(conf.def_dbname, 'alter table project_t rename to project')
#print db.exec_cmd(conf.def_dbname, 'update project set recovery=0')
#print db.exec_cmd(conf.def_dbname, 'select * from project')
#print db.exec_cmd(conf.def_dbname, 'alter table project add column datetime text')
#print db.exec_cmd(conf.def_dbname, 'select * from sqlite_master')
#print db.exec_cmd(conf.def_dbname, 'alter table bug rename to bug_t')
#print db.exec_cmd(conf.def_dbname, 'insert into bug select * from bug_t')
#print db.exec_cmd(conf.def_dbname, 'alter table bug add column projectid integer')
#print db.exec_cmd(conf.def_dbname, 'select rowid, * from project')
#print db.exec_cmd(conf.def_dbname, 'select rowid, * from bug')
#print db.exec_cmd(conf.def_dbname, 'update bug set projectid=1')
#print db.exec_cmd(conf.def_dbname, conf.project_table)
#print db.exec_cmd(conf.def_dbname, 'select name from sqlite_master where type="table"')
#print db.exec_cmd(conf.def_dbname, 'select * from sqlite_master where type="table"')
#print db.exec_cmd(conf.def_dbname, 'update bug set projectid=0 where rowid = 16')
#print db.exec_cmd(conf.def_dbname, 'update bug set projectid=2 where rowid = 17')
#print db.exec_cmd(conf.def_dbname, 'select * from bug where rowid=9')
#print db.exec_cmd(conf.def_dbname, 'select name, status, description, priority, projectid from bug where rowid=10')

### fix the bug table's field ###
#print db.exec_cmd(conf.def_dbname, 'alter table bug rename to bug_t')
#print db.exec_cmd(conf.def_dbname, conf.bug_table)
#print db.exec_cmd(conf.def_dbname, 'insert into bug select name, status, priority, description, projectid from bug_t')
#print db.exec_cmd(conf.def_dbname, 'drop table bug_t')
###


### delete test bug item ###
#print db.exec_cmd(conf.def_dbname, 'delete from bug where rowid=39')
print db.exec_cmd(conf.def_dbname, 'delete from project where name="abc"')
print db.exec_cmd(conf.def_dbname, 'delete from project where name="test"')
