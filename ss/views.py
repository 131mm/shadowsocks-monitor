from django.shortcuts import render
import json,base64
import socket
# Create your views here.
class Address():
    #ssr_folder='C://User/13395/ubun/shadowsocksr'
    ssr_folder='/Users/sanji/hexo/shadowsocksr'
    config_file=ssr_folder+'/config.json'
    config_user_file=ssr_folder+'/user-config.json'
    config_user_api_file=ssr_folder+'/userapiconfig.py'
    config_user_mudb_file=ssr_folder+'/mudb.json'
    ssr_log_file=ssr_folder+'/ssserver.log'
    Libsodiumr_file="/usr/local/lib/libsodium.so"
    Libsodiumr_ver_backup="1.0.15"
    Server_Speeder_file="/serverspeeder/bin/serverSpeeder.sh"
    LotServer_file="/appex/bin/serverSpeeder.sh"
    jq_file=ssr_folder+'/jq'

class ssr(Address):

    def triffic(self,big):
        flag = 0
        tr = 0
        units = {0: 'B', 1: 'K', 2: 'M', 3: 'G'}
        little = int(big / 1024)
        for i in range(4):
            if little:
                tr = little
                little = int(little / 1024)
                flag += 1
            else:
                return str(tr) + units[flag]


    def Get_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip

    def ss_link(self,ss):
        sslink = base64.b64encode(ss.encode('utf-8'))
        return 'ss://' + str(sslink, 'utf-8')

    def ssr_link(self):
        return 'ssraaaa'

    def Get_User_info(self,port):
        with open(self.config_user_mudb_file,'r') as user_file:
            mudb=json.load(user_file)
            for i in mudb:
                if i['port']==port:
                    ss = i['method'] + ':' + i['passwd'] + '@' + self.Get_ip() + ':' + str(port)
                    user={
                        'ip':self.Get_ip(),
                        'traffic':self.triffic(i['transfer_enable']),
                        'used':self.triffic(i['d'] + i['u']),
                        'sslink':self.ss_link(ss)
                    }
                    user.update(i)
                    return user

    def Get_all_user           (self):
        with open(self.config_user_mudb_file, 'r') as user_file:
            mudb = json.load(user_file)
            users=[]
            for i in mudb:
                ss = i['method'] + ':' + i['passwd'] + '@' + self.Get_ip() + ':' + str(i['port'])
                user={
                    'ip':self.Get_ip(),
                    'traffic':self.triffic(i['transfer_enable']),
                    'used':self.triffic(i['d'] + i['u']),
                    'sslink':self.ss_link(ss),
                }
                user.update(i)
                users.append(user)
            return users

    def View_User                (self):
        while 1:
            print("请输入要查看账号信息的用户 端口")
            port=input("(默认: 取消):")
            if not port:
                print("已取消...")
                return 0
            else:port= int(port)
            user=self.Get_User_info(port)
            if not user:
                print("请输入正确 端口")
            else: return user

app=ssr()
def home(request):
    if 'port' in request.GET:
        port = request.GET['port']
    else: port=6001
    users=app.Get_all_user()
    context={'users':users}

    obj = render(request, 'home.html', context=context)
    return obj

def user_info(request):
    if 'port' in request.GET:
        port = request.GET['port']
    else: port=6001
    user=app.Get_User_info(port)
    context=user
    obj = render(request, 'home.html', context=context)

