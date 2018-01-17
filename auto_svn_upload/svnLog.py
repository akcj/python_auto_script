#coding:utf-8
import os
import re

#日志分析，M为更改，A为添加，D为删除
inquire_arr = ['M','A','D'] 

# 分析最近num（默认为5）次的日志，将有变动的代码文件路径去重后以列表返回
def ansSvnLog(local_path, svn_path, num=5):
    svn_command = 'svn log ' + local_path + ' -l '+ str(num) + ' -v'
    com_log = os.popen(svn_command).read()
    arr = []
    for line in com_log.splitlines():
        line = line.strip()
        if line[0:1] in inquire_arr:
            if svn_path in line[2:] and '(' not in line[2:]:
                line = line[2:].replace(svn_path,local_path).replace('/','\\')
                if line not in arr:
                    arr.append(line)
    return arr

# 拉取最新代码到本地
def updateSvn(local_path):
    svn_command = 'svn update '+ local_path
    os.popen(svn_command).read()