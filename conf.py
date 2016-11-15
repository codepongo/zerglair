def_dbname = "lair.db"
#def_shortchars = 50 # number of characters to display
project_table = "create table project (name text unique, recovery integer);"
bug_table = "create table bug (name text, priority text, status text, description text);" 
#bug_table = "create table bug (projectid integer, name text, description text, priority text, status text, foreign key(projectid) references project(rowid));" 
image_table = "create table image (bugid integer, md5 text, foreign key(bugid) references bug(rowid));" 
#wiki_table = "create table wiki (projectid integer, shortname text, content text, foreign key(projectid) references project(rowid));"
