
# wrapper around sqlite's data base functionality

import sqlite3

def exec_cmd(dbname, cmd_string, qualifier=""):
    ''' execute the command on the database '''
    print("exec_cmd: "+cmd_string+" => "+str(qualifier))

    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        query_result = []

        if cmd_string != "":
            if qualifier == "": cur.execute(cmd_string)
            else: cur.execute(cmd_string, qualifier)

            conn.commit()
            query_result = cur.fetchall()
            cur.close()

            if query_result != None:
                return query_result
        else:
            print("exec_cmd: ", cmd_string,"!")
    except Exception as e:
            print("exec_cmd: "+str(e), cmd_string,"!")

