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
print db.exec_cmd(conf.def_dbname, 'select * from sqlite_master')
print db.exec_cmd(conf.def_dbname, 'update project set recovery=0')
print db.exec_cmd(conf.def_dbname, 'select * from project')
