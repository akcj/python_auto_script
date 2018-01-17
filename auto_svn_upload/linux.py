#coding:utf-8
import paramiko

class Linux(object):
    # 通过IP，端口， 用户名，密码 初始化一个远程Linux主机
    def __init__ (self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh = ''
        self.try_times = 3 # 链接失败的重试次数

    # 连接远程主机
    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while True:
            try:
                self.ssh.connect(self.ip, self.port, self.username, self.password, allow_agent=True)
                # 如果没有抛出异常说明连接成功，直接返回
                print u'连接%s成功' % self.ip
                return True
            except Exception, e:
                if self.try_times != 0:
                    print u'连接%s失败，进行重试' % self.ip
                    self.try_times -= 1
                else:
                    print u'重试3次失败，结束程序'
                    exit(1)

    # 断开连接
    def close(self):
        self.ssh.close()
        print u'断开%s成功' % self.ip

    # 发送要执行的命令
    def exec_commands(self, cmd):
        stdin,stdout,stderr = self.ssh.exec_command(cmd)

    # 上传文件
    def upload(self,locals_path,server_path):
        sftp = self.ssh.open_sftp()
        sftp.put(locals_path,server_path)
        sftp.close()


