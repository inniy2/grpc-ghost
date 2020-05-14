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
import configparser

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
    
    def ibdsize(self, request, context):
        rdir = request.dir
        schemaname = request.schemaname
        tablename  = request.tablename
        space = str(int(os.path.getsize(rdir+"/"+schemaname+"/"+tablename+".ibd")/ 1024 / 1024 / 1024))+"G"
        print("file : %s, file size : %s" % (rdir+"/"+schemaname+"/"+tablename+".ibd", space))
        return ghost_pb2.APIResponse(responsemessage=space,
                                        responsecode=0)

    def checkdefinition(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        print("schema name : %s , table name: %s" % (schemaname, tablename))
        config = configparser.ConfigParser()
        config.sections()
        config.read('/etc/grpc-ghost/config.ini')
        try:
            cnx = mysql.connector.connect(user=config['DEFAULT']['user'], password=config['DEFAULT']['password'],
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

    def rowcount(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        print("schema name : %s , table name: %s" % (schemaname, tablename))
        config = configparser.ConfigParser()
        config.sections()
        config.read('/etc/grpc-ghost/config.ini')
        try:
            cnx = mysql.connector.connect(user=config['DEFAULT']['user'], password=config['DEFAULT']['password'],
                                  host='127.0.0.1',
                                  database=schemaname)
            cursor = cnx.cursor()
            cursor.execute(
                "SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s", (schemaname,tablename))
            for (table_rows,) in cursor:
                print("{}".format(table_rows))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Please check user & password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exits")
            else:
                print(err)
        cursor.close()
        cnx.close()
        return ghost_pb2.APIResponse(responsemessage=str(int(table_rows)),
                                        responsecode=0)

    def dryrun(self, request, context):
        schemaname = request.schemaname
        tablename  = request.tablename
        statement  = request.statement
        binary      = "/usr/bin/gh-ost"
        conf       = "/etc/mysql/debian.cnf"
        if os.path.exists("/tmp/gh-ost.%s.%s.sock" % (schemaname, tablename)):
            return ghost_pb2.APIResponse(responsemessage="Ghost socket file already exists.",
                                        responsecode=1)
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
                "--approve-renamed-columns",                 # 8  *
				"--database="+schemaname,                    # 9
				"--table="+tablename,                        # 10
				"--alter="+statement,                        # 11
				"--switch-to-rbr",                           # 12
				"--cut-over=default",                        # 13
				"--exact-rowcount",                          # 14
				"--concurrent-rowcount",                     # 15
				"--default-retries=120",                     # 16
				"--timestamp-old-table",                     # 17
                "--panic-flag-file=/tmp/ghost.panic.flag",   # 18
                "--postpone-cut-over-flag-file=/tmp/ghost.postpone.flag", # 19
                "--initially-drop-ghost-table",              # 20 *
				"--verbose"                                  # 21
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
        binary      = "/usr/bin/gh-ost"
        conf       = "/etc/mysql/debian.cnf"
        if os.path.exists("/tmp/gh-ost.%s.%s.sock" % (schemaname, tablename)):
            return ghost_pb2.APIResponse(responsemessage="Ghost socket file already exists.",
                                        responsecode=1)
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
                "--approve-renamed-columns",                 # 8  *
				"--database="+schemaname,                    # 9
				"--table="+tablename,                        # 10
				"--alter="+statement,                        # 11
				"--switch-to-rbr",                           # 12
				"--cut-over=default",                        # 13
				"--exact-rowcount",                          # 14
				"--concurrent-rowcount",                     # 15
				"--default-retries=120",                     # 16
				"--timestamp-old-table",                     # 17
                "--panic-flag-file=/tmp/ghost.panic.flag",   # 18
                "--postpone-cut-over-flag-file=/tmp/ghost.postpone.flag", # 19
                "--initially-drop-ghost-table",              # 20 *
				"--verbose",                                 # 21
				"--execute"                                  # 22
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
        binary     = "/usr/bin/gh-ost"
        conf       = "/etc/mysql/debian.cnf"
        if os.path.exists("/tmp/gh-ost.%s.%s.sock" % (schemaname, tablename)):
            return ghost_pb2.APIResponse(responsemessage="Ghost socket file already exists.",
                                        responsecode=1)
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
                "--approve-renamed-columns",                 # 8  *
				"--database="+schemaname,                    # 9
				"--table="+tablename,                        # 10
				"--alter="+statement,                        # 11
				"--switch-to-rbr",                           # 12
				"--cut-over=default",                        # 13
				"--exact-rowcount",                          # 14
				"--concurrent-rowcount",                     # 15
				"--default-retries=120",                     # 16
				"--timestamp-old-table",                     # 17
                "--panic-flag-file=/tmp/ghost.panic.flag",   # 18
                "--postpone-cut-over-flag-file=/tmp/ghost.postpone.flag", # 19
                "--initially-drop-ghost-table",              # 20 *
				"--verbose",                                 # 21
				"--execute"                                  # 22
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
        print("Cut Over : rm -rf /tmp/ghost.postpone.flag")
        print("ghost.stdout is %s " % (_ghost_stdout))
        print("ghost.stderr is %s " % (_ghost_stderr))
        return ghost_pb2.APIResponse(responsemessage=_ghost_stdout+'\n'+_ghost_stderr,
                                        responsecode=0)

    def putpanicflag(self, request, context):
        args = ["touch",
                "/tmp/ghost.panic.flag"
        ]
        ghost = subprocess.run(args,stdout=PIPE,stderr=PIPE, universal_newlines=True)
        _ghost_stdout = ghost.stdout
        _ghost_stderr = ghost.stderr
        print("Put Panic Flag : touch /tmp/ghost.panic.flag")
        print("ghost.stdout is %s " % (_ghost_stdout))
        print("ghost.stderr is %s " % (_ghost_stderr))
        return ghost_pb2.APIResponse(responsemessage=_ghost_stdout+'\n'+_ghost_stderr,
                                        responsecode=0)

    def cleanup(self, request, context):
        args = 'rm -rf /tmp/ghost.panic.flag /tmp/gh-ost.*.*.sock /tmp/ghost.postpone.flag'
        ghost = subprocess.run(args,stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True)
        _ghost_stdout = ghost.stdout
        _ghost_stderr = ghost.stderr
        print("Clean up : %s" % (args))
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
    config = configparser.ConfigParser()
    config.sections()
    config.read('/etc/grpc-ghost/config.ini')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(config['DEFAULT']['max_workers'])))
    ghost_pb2_grpc.add_ghostServicer_to_server(Listener(),server)
    server.add_insecure_port("[::]:"+port)
    server.start()
    print("port : %s" % (port))
    print("max_workers : %s" % (config['DEFAULT']['max_workers']))

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("KeyboardInterupt")
        server.stop(0)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.sections()
    config.read('/etc/grpc-ghost/config.ini')
    serve(config['DEFAULT']['port'])