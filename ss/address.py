import os,json,base64,sys

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
def triffic(big):
    flag=0
    tr=0
    units={0:'B',1:'K',2:'M',3:'G'}
    little=int(big/1024)
    for i in range(4):
        if little:
            tr=little
            little = int(little / 1024)
            flag+=1
        else:
            return str(tr)+units[flag]



# ip='12.0.0.1'
# port='6001'
# passwd='6001'
# method='aes-256-cfb'
# ss=method+':'+passwd+'@'+ip+':'+port
# sslink=base64.b64encode(ss.encode('utf-8'))
# ss_link='ss://'+str(sslink,'utf-8')
# print(ss_link)
# with open(adr.config_user_mudb_file, 'r') as user_file:
#     mudb = json.load(user_file)
#
#     for i in mudb:
#         #print(i)
#         print('user:', i['user'], 'port:', i['port'], 'triffic:', triffic(i['transfer_enable']), 'used:', triffic(i['d'] + i['u']))
#
