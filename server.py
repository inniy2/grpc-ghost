from concurrent import futures
import grpc
import ghost_pb2
import ghost_pb2_grpc
import time
import threading
import os
import mysql.connector
from mysql.connector import errorcode
import subprocess
from subprocess import Popen, PIPE

class Listener(ghost_pb2_grpc.ghostServicer):
    def __init__(self, *args, **kwargs):
        self.name = ''

    def diskcheck(self, request, context):
        rdir = request.dir
        statvfs = os.statvfs(rdir)
        space = str(int(statvfs.f_frsize * statvfs.f_bfree / 1024 / 1024 / 1024))+"G"
        print("dir : %s, free size : %s" % (rdir, space))
        return ghost_pb2.APIResponse(responsemessage=space,
                                        responsecode=0)

    def checkdefinition(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        print("schema name : %s , table name: %s" % (schemaname, tablename))
        try:
            cnx = mysql.connector.connect(user='root', password='12345678',
                                  host='127.0.0.1',
                                  database=schemaname)
            cursor = cnx.cursor()
            cursor.execute(
                "SHOW CREATE TABLE {}".format(tablename))
            for (table, create_table) in cursor:
                print("{} OF SYNTAX IS {}".format(table, create_table))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Please check user & password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exits")
            else:
                print(err)
        cursor.close()
        cnx.close()
        return ghost_pb2.APIResponse(responsemessage=create_table,
                                        responsecode=0)

    def dryrun(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        statement  = request.statement
        binary      = "/Users/baesangsun/bin/gh-ost"
        conf       = "/Users/baesangsun/.my.cnf"
        print("schema name : %s , table name: %s, statement %s" % (schemaname, tablename, statement))
        print("ghost: %s , conf: %s" % (binary, conf))
        args = [
        binary,                                              # 0
				"--max-load=Threads_running=50",             # 1
				"--critical-load=Threads_running=1500",      # 2
				"--chunk-size=500",                          # 3
				"--max-lag-millis=1500",                     # 4
				"--conf="+conf,                              # 5
				"--host=127.0.0.1",                          # 6
				"--allow-on-master",                         # 7  *
				"--database="+schemaname,                    # 8
				"--table="+tablename,                        # 9
				"--alter="+statement,                        # 10
				"--switch-to-rbr",                           # 11
				"--cut-over=default",                        # 12
				"--exact-rowcount",                          # 13
				"--concurrent-rowcount",                     # 14
				"--default-retries=120",                     # 15
				"--timestamp-old-table",                     # 16
                "--panic-flag-file=/tmp/ghost.panic.flag",   # 17
                "--postpone-cut-over-flag-file=/tmp/ghost.postpone.flag", # 18
				"--verbose"                                  # 19
        ]
        ghost = subprocess.run(args,stdout=PIPE,stderr=PIPE, universal_newlines=True)
        _ghost_stdout = ghost.stdout
        _ghost_stderr = ghost.stderr
        print("ghost.stdout is %s " % (_ghost_stdout))
        print("ghost.stderr is %s " % (_ghost_stderr))
        return ghost_pb2.APIResponse(responsemessage=_ghost_stdout+'\n'+_ghost_stderr,
                                        responsecode=0)

    def execute(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        statement  = request.statement
        binary      = "/Users/baesangsun/bin/gh-ost"
        conf       = "/Users/baesangsun/.my.cnf"
        print("schema name : %s , table name: %s, statement %s" % (schemaname, tablename, statement))
        print("ghost: %s , conf: %s" % (binary, conf))
        args = [
        binary,                                              # 0
				"--max-load=Threads_running=50",             # 1
				"--critical-load=Threads_running=1500",      # 2
				"--chunk-size=500",                          # 3
				"--max-lag-millis=1500",                     # 4
				"--conf="+conf,                              # 5
				"--host=127.0.0.1",                          # 6
				"--allow-on-master",                         # 7  *
				"--database="+schemaname,                    # 8
				"--table="+tablename,                        # 9
				"--alter="+statement,                        # 10
				"--switch-to-rbr",                           # 11
				"--cut-over=default",                        # 12
				"--exact-rowcount",                          # 13
				"--concurrent-rowcount",                     # 14
				"--default-retries=120",                     # 15
				"--timestamp-old-table",                     # 16
                "--panic-flag-file=/tmp/ghost.panic.flag",   # 17
                "--postpone-cut-over-flag-file=/tmp/ghost.postpone.flag", # 19
				"--verbose",                                 # 20
				"--execute"                                  # 21
        ]
        with subprocess.Popen(args, bufsize=-1, stdout=PIPE, stderr=PIPE, universal_newlines=True) as ghost:
            while True:
                _ghost_stderr = ghost.stderr.readline()
                _ghost_stdout = ghost.stdout.readline()
                if ghost.poll() is not None:
                    print("server alter is completed.")
                    break
                print("ghost.stdout is %s " % (_ghost_stdout))
                print("ghost.stderr is %s " % (_ghost_stderr))
                yield ghost_pb2.APIResponse(responsemessage=_ghost_stdout+'\n'+_ghost_stderr,
                                                responsecode=0)

    def executeNohup(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        statement  = request.statement
        binary     = "/Users/baesangsun/bin/gh-ost"
        conf       = "/Users/baesangsun/.my.cnf"
        print("schema name : %s , table name: %s, statement %s" % (schemaname, tablename, statement))
        print("ghost: %s , conf: %s" % (binary, conf))
        args = [
        "nohup",
        binary,                                              # 0
				"--max-load=Threads_running=50",             # 1
				"--critical-load=Threads_running=1500",      # 2
				"--chunk-size=500",                          # 3
				"--max-lag-millis=1500",                     # 4
				"--conf="+conf,                              # 5
				"--host=127.0.0.1",                          # 6
				"--allow-on-master",                         # 7  *
				"--database="+schemaname,                    # 8
				"--table="+tablename,                        # 9
				"--alter="+statement,                        # 10
				"--switch-to-rbr",                           # 11
				"--cut-over=default",                        # 12
				"--exact-rowcount",                          # 13
				"--concurrent-rowcount",                     # 14
				"--default-retries=120",                     # 15
				"--timestamp-old-table",                     # 16
                "--panic-flag-file=/tmp/ghost.panic.flag",   # 17
                "--postpone-cut-over-flag-file=/tmp/ghost.postpone.flag", # 19
				"--verbose",                                 # 20
				"--execute"                                  # 21
        ]
        subprocess.Popen(args)
        return ghost_pb2.APIResponse(responsemessage="Executing",
                                        responsecode=0)

    def cutover(self, request, context):
        args = ["rm","-rf",
                "/tmp/ghost.postpone.flag"
        ]
        ghost = subprocess.run(args,stdout=PIPE,stderr=PIPE, universal_newlines=True)
        _ghost_stdout = ghost.stdout
        _ghost_stderr = ghost.stderr
        print("ghost.stdout is %s " % (_ghost_stdout))
        print("ghost.stderr is %s " % (_ghost_stderr))
        return ghost_pb2.APIResponse(responsemessage=_ghost_stdout+'\n'+_ghost_stderr,
                                        responsecode=0)

    def interactive(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        ghostcmd   = request.ghostcommand
        arg1 = ["echo", ghostcmd] 
        arg2 = ["nc","-U", "/tmp/gh-ost."+schemaname+"."+tablename+".sock"] 
        echo = subprocess.Popen(arg1, stdout=PIPE)
        ghost = subprocess.Popen(arg2, stdin=echo.stdout, stdout=PIPE, universal_newlines=True)
        echo.stdout.close() 
        message = ""
        while True:
            _ghost_stdout = ghost.stdout.readline()
            if _ghost_stdout == '' and ghost.poll() is not None:
                break
            if _ghost_stdout:
                print(_ghost_stdout.strip())
                message += (_ghost_stdout.strip() + "\n")

        return ghost_pb2.APIResponse(responsemessage=message,
                                        responsecode=0)

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    ghost_pb2_grpc.add_ghostServicer_to_server(Listener(),server)
    server.add_insecure_port("[::]:"+port)
    server.start()
    print("port : %s" % (port))

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("KeyboardInterupt")
        server.stop(0)

if __name__ == "__main__":
    serve("9090")