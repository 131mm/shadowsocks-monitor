#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random,os,json,base64,socket,struct
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

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


class MuJsonLoader(object):
    def __init__(self):
        self.json = None

    def load(self, path):
        l = "[]"
        try:
            with open(path, 'rb+') as f:
                l = f.read().decode('utf8')
        except:
            pass
        self.json = json.loads(l)

    def save(self, path):
        if self.json is not None:
            output = json.dumps(self.json, sort_keys=True, indent=4, separators=(',', ': '))
            with open(path, 'a'):
                pass
            with open(path, 'rb+') as f:
                f.write(output.encode('utf8'))
                f.truncate()


class MuMgr(object):
    def __init__(self):
        self.adr=Address()
        self.config_path = self.adr.config_user_mudb_file
        self.data = MuJsonLoader()
        self.server_addr = self.getipaddr()

    def getipaddr(self, ifname='eth0'):
        ret = '127.0.0.1'
        try:
            ret = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        except:pass
        if ret == '127.0.0.1':
            try:
                import fcntl
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ret = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
            except:
                pass
        return ret

    def ssrlink(self, user):
        protocol = user.get('protocol', '')
        obfs = user.get('obfs', '')
        protocol = protocol.replace("_compatible", "")
        obfs = obfs.replace("_compatible", "")
        passwd64=base64.b64encode(user['passwd'].encode('utf-8'))
        passwd64=str(passwd64, 'utf-8')
        link = ("%s:%s:%s:%s:%s:%s" % (self.getipaddr(), user['port'], protocol, user['method'], obfs, (passwd64.replace("=", "")).encode('utf-8')))
        return "ssr://"+str(base64.b64encode(link.encode('utf-8')),'utf-8')

    def userinfo(self, user, muid = None):
        ret = ""
        key_list = ['user', 'port', 'method', 'passwd', 'protocol', 'protocol_param', 'obfs', 'obfs_param', 'transfer_enable', 'u', 'd']
        for key in sorted(user):
            if key not in key_list:
                key_list.append(key)
        for key in key_list:
            if key in ['enable'] or key not in user:
                continue
            ret += '\n'
            if (muid is not None) and (key in ['protocol_param']):
                for row in self.data.json:
                    if int(row['port']) == muid:
                        ret += "    %s : %s" % (key, str(muid) + ':' + row['passwd'])
                        break
            elif key in ['transfer_enable', 'u', 'd']:
                if muid is not None:
                    for row in self.data.json:
                        if int(row['port']) == muid:
                            val = row[key]
                            break
                else:
                    val = user[key]
                if val / 1024 < 4:
                    ret += "    %s : %s" % (key, val)
                elif val / 1024 ** 2 < 4:
                    val /= float(1024)
                    ret += "    %s : %s  K Bytes" % (key, val)
                elif val / 1024 ** 3 < 4:
                    val /= float(1024 ** 2)
                    ret += "    %s : %s  M Bytes" % (key, val)
                else:
                    val /= float(1024 ** 3)
                    ret += "    %s : %s  G Bytes" % (key, val)
            else:
                ret += "    %s : %s" % (key, user[key])
        # ret += "\n    " + self.ssrlink(user, False, muid)
        # ret += "\n    " + self.ssrlink(user, True, muid)
        return ret

    def rand_pass(self):
        return ''.join([random.choice('''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~-_=+(){}[]^&%$@''') for i in range(8)])

    def add(self, user):
        up = {
            'enable': 1,
            'u': 0,
            'd': 0,
            'method': "aes-256-cfb",
            'protocol': "origin",
            'obfs': "plain",
            'transfer_enable': 53687091200
        }
        up['passwd'] = self.rand_pass()
        up.update(user)

        self.data.load(self.config_path)
        for row in self.data.json:
            match = False
            if 'user' in user and row['user'] == user['user']:
                match = True
            if 'port' in user and row['port'] == user['port']:
                match = True
            if match:
                return
        self.data.json.append(up)
        self.data.save(self.config_path)

    def edit(self, user):
        self.data.load(self.config_path)
        for row in self.data.json:
            match = True
            if 'user' in user and row['user'] != user['user']:
                match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                print("edit user [%s]" % (row['user'],))
                row.update(user)
                break
        self.data.save(self.config_path)

    def delete(self, user):
        self.data.load(self.config_path)
        index = 0
        for row in self.data.json:
            match = True
            if 'user' in user and row['user'] != user['user']:
                match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                del self.data.json[index]
                break
            index += 1
        self.data.save(self.config_path)

    def clear_ud(self, user):
        up = {'u': 0, 'd': 0}
        self.data.load(self.config_path)
        for row in self.data.json:
            match = True
            if 'user' in user and row['user'] != user['user']:
                match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                row.update(up)
                print("clear user [%s]" % row['user'])
        self.data.save(self.config_path)

    def list_user(self, user):
        self.data.load(self.config_path)
        if not user:
            for row in self.data.json:
                print("user [%s] port %s" % (row['user'], row['port']))
            return
        for row in self.data.json:
            match = True
            if 'user' in user and row['user'] != user['user']:
                match = False
            if 'port' in user and row['port'] != user['port']:
                match = False
            if match:
                muid = None
                if 'muid' in user:
                    muid = user['muid']
                print("### user [%s] info %s" % (row['user'], self.userinfo(row, muid)))
    def Print_User_info(self,user):
        i=user
        print('用户',i['user'],'的配置信息：')
        print('IP:    ',)
        print('端口：  ',i['port'])
        print('密码：  ',i['passwd'])
        print('加密：  ',i['method'])
        print('协议：  ',i['protocol'])
        print('混淆：  ',i['obfs'])
        print('流量：  ',i['traffic'])
        print('已用：  ',i['used'])
        print('ss链接：',i['sslink'])
        print('ssr链接:',i['ssrlink'])


class Iptables():
    def add_rule(self,port):
        commands=[]
        commands.append('iptables -I INPUT -m state --state NEW -m udp -p udp --dport {} -j ACCEPT'.format(port))
        commands.append('iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport {} -j ACCEPT'.format(port))
        for c in commands:
            try:
                os.popen(c)
            except: pass

    def del_rule(self,port):
        commands=[]
        commands.append('iptables -D INPUT -m state --state NEW -m udp -p udp --dport {} -j ACCEPT'.format(port))
        commands.append('iptables -D INPUT -m state --state NEW -m tcp -p tcp --dport {} -j ACCEPT'.format(port))
        for c in commands:
            try:
                os.popen(c)
            except: pass

    def save_table(self):
        try:
            os.popen('iptables-save > /etc/iptables.up.rules')
        except: pass

class ssr(Address,MuMgr,Iptables):
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


    def ss_link(self,ss):
        sslink = base64.b64encode(ss.encode('utf-8'))
        return 'ss://' + str(sslink, 'utf-8')

    def ssrlink(self, user):
        protocol = user.get('protocol', '')
        obfs = user.get('obfs', '')
        protocol = protocol.replace("_compatible", "")
        obfs = obfs.replace("_compatible", "")
        passwd64=base64.b64encode(user['passwd'].encode('utf-8'))
        passwd64=str(passwd64, 'utf-8')
        link = ("%s:%s:%s:%s:%s:%s" % (self.getipaddr(), user['port'], protocol, user['method'], obfs, (passwd64.replace("=", "")).encode('utf-8')))
        return "ssr://"+str(base64.b64encode(link.encode('utf-8')),'utf-8')

    def Get_User_info(self,port):
        with open(self.config_user_mudb_file,'r') as user_file:
            mudb=json.load(user_file)
            for i in mudb:
                if i['port']==port:
                    ss = i['method'] + ':' + i['passwd'] + '@' + self.getipaddr() + ':' + str(port)
                    ssr = self.ssrlink(i)
                    user={
                        'ip':self.getipaddr(),
                        'traffic':self.triffic(i['transfer_enable']),
                        'used':self.triffic(i['d'] + i['u']),
                        'sslink':self.ss_link(ss),
                        'ssrlink':ssr
                    }
                    user.update(i)
                    return user

    def Get_all_user           (self):
        with open(self.config_user_mudb_file, 'r') as user_file:
            mudb = json.load(user_file)
            users=[]
            for i in mudb:
                ssr = self.ssrlink(i)
                ss = i['method'] + ':' + i['passwd'] + '@' + self.getipaddr() + ':' + str(i['port'])
                user={
                    'ip':self.getipaddr(),
                    'traffic':self.triffic(i['transfer_enable']),
                    'used':self.triffic(i['d'] + i['u']),
                    'sslink':self.ss_link(ss),
                    'ssrlink':ssr,
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


app = ssr()


def home(request):
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
    return obj


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        name=request.POST.get('name','')
        port=request.POST.get('port','')
        passwd=request.POST.get('passwd','')
        method=request.POST.get('method','')
        protocol=request.POST.get('protocol','')
        obfs=request.POST.get('obfs','')
        if name and port:
            port=int(port)
            if port<65534:
                user={
                        'user':name,
                        'port':port,
                    }
            else:return HttpResponse('error')
            if passwd:
                user.update({'passwd':passwd})
            if method:
                user.update({'method':method})
            if protocol:
                user.update({'protocol':protocol})
            if obfs:
                user.update({'obfs':obfs})

            app.add(user)
            app.del_rule(port)
            app.add_rule(port)
            app.save_table()
        return HttpResponse('test')
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def edit_user(request):
    if request.method == 'POST':
        name=request.POST.get('name','')
        port=request.POST.get('port','')
        passwd=request.POST.get('passwd','')
        method=request.POST.get('method','')
        protocol=request.POST.get('protocol','')
        obfs=request.POST.get('obfs','')
        if port:
            port=int(port)
            if port<65534:
                user={
                        'port':port,
                    }
            else:return HttpResponse('error')
            if name:
                user.update({'user':name})
            if passwd:
                user.update({'passwd':passwd})
            if method:
                user.update({'method':method})
            if protocol:
                user.update({'protocol':protocol})
            if obfs:
                user.update({'obfs':obfs})
            app.edit(user)
        return HttpResponse('test')
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        port=request.POST.get('port','')
        if port:
            port=int(port)
            user={
                    'port':port,
                }
            app1=ssr()
            app1.delete(user)
            app1.del_rule(port)
            app1.save_table()
            return HttpResponse('ok')

    else:return HttpResponseRedirect('/')

