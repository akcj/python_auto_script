#coding:utf-8
import sys
import os
from conf import local_path,svn_path,servers
from svnLog import ansSvnLog,updateSvn
from linux import Linux


def uploadFile(num):
    try:
        updateSvn(local_path)
        logs = ansSvnLog(local_path,svn_path,num)
        for server in servers:
            host = Linux(server['ip'],server['port'], server['username'], server['password'])
            host.connect()
            for i in logs:
                server_path = i.replace(local_path,server['path']).replace('\\','/')
                # 文件存在，则进行上传/更新
                if os.path.exists(i):
                    if os.path.isdir(i):
                        host.exec_commands('mkdir -p '+server_path)
                        print i +'...OK'
                    if os.path.isfile(i):
                        host.exec_commands('mkdir -p '+os.path.dirname(server_path))
                        host.upload(i,server_path)
                        print i +'...OK'
                # 文件不存在，则代表svn的删除操作，直接删除服务端代码文件
                else:
                    host.exec_commands('rm -rf '+server_path)
                    print i +'...OK'
            host.close()
            print '------------------------------------------------------------------'
    except Exception, e:
        print e

if __name__ == '__main__':
    # 接收脚本传参，默认为5
    num = 5 if len(sys.argv) == 1 else sys.argv[1]
    uploadFile(num)