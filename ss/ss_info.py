#!bin/python3
import json,base64
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
        return '127.0.0.1'

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
                        'transfer_enable':self.triffic(i['transfer_enable']),
                        'used':self.triffic(i['d'] + i['u']),
                        'sslink':self.ss_link(ss)
                    }
                    user.update(i)
                    return user

    def Get_all_user           (self,q):
        with open(self.config_user_mudb_file, 'r') as user_file:
            mudb = json.load(user_file)
            users=[]
            for i in mudb:
                user={
                    'user':i['user'],
                    'port':i['port'],
                    'triffic':self.triffic(i['transfer_enable']),
                    'used':self.triffic(i['d'] + i['u'])
                }
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

if __name__ == '__main__':

    app=ssr()
    while 1:
        print("请输入要查看账号信息的用户 端口")
        port = input("(默认: 取消):")
        if not port:
            print("已取消...")
            break
        else:
            port = int(port)
        user =  app.Get_User_info(port)
        if not user:
            print("请输入正确 端口")
        else:
            print(user)
