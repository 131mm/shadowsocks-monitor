#!bin/python3
import os,json,base64
class Address():
    #ssr_folder='C://User/13395/ubun/shadowsocksr'
    ssr_folder='E://a/shadowsocksr'
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
adr=Address()
class ss():
    def check_sys                (self): pass
    def Clear_transfer_all       (self): pass
    def crontab_monitor_ssr      (self): pass
    def menu_status              (self): pass
    def Install_SSR              (self,num): print(num)
    def Update_SSR               (self,num): print(num)
    def Uninstall_SSR            (self,num): print(num)
    def Install_Libsodium        (self,num): print(num)
    def SSR_installation_status  (self): pass
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

    def List_port_user           (self):
        with open(adr.config_user_mudb_file, 'r') as user_file:
            mudb = json.load(user_file)
            for i in mudb:
                print('user:', i['user'], 'port:', i['port'], 'triffic:', self.triffic(i['transfer_enable']), 'used:',
                      self.triffic(i['d'] + i['u']))
    def Get_ip(self):
        return '127.0.0.1'

    def ss_link(self,ss):
        sslink = base64.b64encode(ss.encode('utf-8'))
        return 'ss://' + str(sslink, 'utf-8')

    def ssr_link(self):
        return 'ssraaaa'

    def Get_User_info(self,port):
        with open(adr.config_user_mudb_file,'r') as user_file:
            mudb=json.load(user_file)
            for i in mudb:
                if i['port']==port:
                    print('用户',i['user'],'的配置信息：')
                    print('IP:    ',self.Get_ip())
                    print('端口：  ',port)
                    print('密码：  ',i['passwd'])
                    print('加密：  ',i['method'])
                    print('协议：  ',i['protocol'])
                    print('混淆：  ',i['obfs'])
                    print('流量：  ',self.triffic(i['transfer_enable']))
                    print('已用：  ',self.triffic(i['d'] + i['u']))
                    ss = i['method'] + ':' + i['passwd'] + '@' + self.Get_ip() + ':' + str(port)
                    print('ss链接：',self.ss_link(ss))
                    print('ssr链接:',self.ssr_link())
                    return 1

    def View_User                (self,num):
        self.SSR_installation_status()
        self.List_port_user()
        while 1:
            print("请输入要查看账号信息的用户 端口")
            port=input("(默认: 取消):")
            if not port:
                print("已取消...")
                return 0
            else:port= int(port)
            if not self.Get_User_info(port):
                print("请输入正确 端口")
            else: break


    def View_user_connection_info(self,num): print(num)
    def Set_config_user                (self): pass
    def Set_config_port                (self): pass
    def Set_config_password            (self): pass
    def Set_config_method              (self): pass
    def Set_config_protocol            (self): pass
    def Set_config_obfs                (self): pass
    def Set_config_protocol_param      (self): pass
    def Set_config_speed_limit_per_con (self): pass
    def Set_config_speed_limit_per_user(self): pass
    def Set_config_transfer            (self): pass
    def Set_config_forbid              (self): pass
    def Add_port_user(self):
        print('Add_port_user')
        self.Set_config_user                ()
        self.Set_config_port                ()
        self.Set_config_password            ()
        self.Set_config_method              ()
        self.Set_config_protocol            ()
        self.Set_config_obfs                ()
        self.Set_config_protocol_param      ()
        self.Set_config_speed_limit_per_con ()
        self.Set_config_speed_limit_per_user()
        self.Set_config_transfer            ()
        self.Set_config_forbid              ()
    def Del_port_user(self): print('Del_port_user')
    def Modify_Config_menu(self,num):
        cases = {
            1: self.Add_port_user,
            2: self.Del_port_user,
            3: self.Uninstall_SSR,
            4: self.Install_Libsodium,
            5: self.View_User,
            6: self.View_user_connection_info,
            7: self.Modify_Config,
            8: self.Manually_Modify_Config,
            9: self.Clear_transfer,
            10: self.Start_SSR,
            11: self.Stop_SSR,
            12: self.Restart_SSR,
            13: self.View_Log,
        }
        case = cases.get(num)
        if case:
            return case()

    def Modify_Config(self,num):
        self.SSR_installation_status()
        info = '''你要做什么？
     1.  添加 用户配置
     2.  删除 用户配置
    ————— 修改 用户配置 —————
     3.  修改 用户密码
     4.  修改 加密方式
     5.  修改 协议插件
     6.  修改 混淆插件
     7.  修改 设备数限制
     8.  修改 单线程限速
     9.  修改 用户总限速
     10. 修改 用户总流量
     11. 修改 用户禁用端口
     12. 修改 全部配置
    ————— 其他 —————
     13. 修改 用户配置中显示的IP或域名

      用户的用户名和端口是无法修改，如果需要修改请使用脚本的 手动修改功能 !
    '''
        print(info)
        case=input("(默认: 取消):")
        if not case: return 0
        else: case=int(case)
        self.Modify_Config_menu(case)


    def Manually_Modify_Config   (self,num): print(num)
    def Clear_transfer           (self,num): print(num)
    def Start_SSR                (self,num): print(num)
    def Stop_SSR                 (self,num): print(num)
    def Restart_SSR              (self,num): print(num)
    def View_Log                 (self,num): print(num)
    def Other_functions          (self,num): print(num)
    def Update_Shell             (self,num): print(num)
    def menu(self,num):
        cases = {
            1: self.Install_SSR,
            2: self.Update_SSR,
            3: self.Uninstall_SSR,
            4: self.Install_Libsodium,
            5: self.View_User,
            6: self.View_user_connection_info,
            7: self.Modify_Config,
            8: self.Manually_Modify_Config,
            9: self.Clear_transfer,
            10: self.Start_SSR,
            11: self.Stop_SSR,
            12: self.Restart_SSR,
            13: self.View_Log,
            14: self.Other_functions,
            15: self.Update_Shell
        }
        case = cases.get(num)
        if case:
            return case(num)

    def main(self):
        self.check_sys()
        action=1
        if action == "clearall":
            self.Clear_transfer_all()
        elif action == "monitor":
            self.crontab_monitor_ssr()
        else:
            print(self.view)
            self.menu_status()
            num = int(input("请输入数字 [1-15]："))
            self.menu(num)




    view='''  ShadowsocksR MuJSON一键管理脚本 
---- Toyo | doub.io/ss-jc60 ----

  1. 安装 ShadowsocksR
  2. 更新 ShadowsocksR
  3. 卸载 ShadowsocksR
  4. 安装 libsodium(chacha20)
——
  5. 查看 账号信息
  6. 显示 连接信息
  7. 设置 用户配置
  8. 手动 修改配置
  9. 配置 流量清零
————
 10. 启动 ShadowsocksR
 11. 停止 ShadowsocksR
 12. 重启 ShadowsocksR
 13. 查看 ShadowsocksR 日志
————
 14. 其他功能
 15. 升级脚本
    '''

app=ss()
app.main()