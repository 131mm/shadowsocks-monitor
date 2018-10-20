#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random
import getopt
import sys
import json
import base64


class Address():
    ssr_folder='/Users/sanji/hexo/shadowsocksr'
    config_user_mudb_file=ssr_folder+'/mudb.json'


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
        import socket
        import struct
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

    def ssrlink(self, user, encode, muid=None):
        protocol = user.get('protocol', '')
        obfs = user.get('obfs', '')
        protocol = protocol.replace("_compatible", "")
        obfs = obfs.replace("_compatible", "")
        passwd64=base64.b64encode(user['passwd'])
        link = ("%s:%s:%s:%s:%s:%s" % (self.server_addr, user['port'], protocol, user['method'], obfs, passwd64.replace("=", "")))
        return "ssr://"+base64.b64encode(link.encode('utf-8'))

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
            'method': "aes-128-ctr",
            'protocol': "auth_aes128_md5",
            'obfs': "tls1.2_ticket_auth_compatible",
            'transfer_enable': 9007199254740992
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
                print("user [%s] port [%s] already exist" % (row['user'], row['port']))
                return
        self.data.json.append(up)
        print("### add user info %s" % self.userinfo(up))
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
                print("### new user info %s" % self.userinfo(row))
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
                print("delete user [%s]" % row['user'])
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


def print_server_help():
    print('''usage: python mujson_manage.py -a|-d|-e|-c|-l [OPTION]...

Actions:
  -a                   add/edit a user
  -d                   delete a user
  -e                   edit a user
  -c                   set u&d to zero
  -l                   display a user infomation or all users infomation

Options:
  -u USER              the user name
  -p PORT              server port (only this option must be set if add a user)
  -k PASSWORD          password
  -m METHOD            encryption method, default: aes-128-ctr
  -O PROTOCOL          protocol plugin, default: auth_aes128_md5
  -o OBFS              obfs plugin, default: tls1.2_ticket_auth_compatible
  -G PROTOCOL_PARAM    protocol plugin param
  -g OBFS_PARAM        obfs plugin param
  -t TRANSFER          max transfer for G bytes, default: 8388608 (8 PB or 8192 TB)
  -f FORBID            set forbidden ports. Example (ban 1~79 and 81~100): -f "1-79,81-100"
  -i MUID              set sub id to display (only work with -l)
  -s SPEED             set speed_limit_per_con
  -S SPEED             set speed_limit_per_user

General options:
  -h, --help           show this help message and exit
''')


def main():
    shortopts = 'adeclu:i:p:k:O:o:G:g:m:t:f:hs:S:'
    longopts = ['help']
    action = None
    user = {}
    fast_set_obfs = {'0': 'plain',
            '+1': 'http_simple_compatible',
            '1': 'http_simple',
            '+2': 'tls1.2_ticket_auth_compatible',
            '2': 'tls1.2_ticket_auth'}
    fast_set_protocol = {'0': 'origin',
            's4': 'auth_sha1_v4',
            '+s4': 'auth_sha1_v4_compatible',
            'am': 'auth_aes128_md5',
            'as': 'auth_aes128_sha1',
            'ca': 'auth_chain_a',
            }
    fast_set_method = {'0': 'none',
            'a1c': 'aes-128-cfb',
            'a2c': 'aes-192-cfb',
            'a3c': 'aes-256-cfb',
            'r': 'rc4-md5',
            'r6': 'rc4-md5-6',
            'c': 'chacha20',
            'ci': 'chacha20-ietf',
            's': 'salsa20',
            'a1': 'aes-128-ctr',
            'a2': 'aes-192-ctr',
            'a3': 'aes-256-ctr'}
    try:
        optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        for key, value in optlist:
            if key == '-a':
                action = 1
            elif key == '-d':
                action = 2
            elif key == '-e':
                action = 3
            elif key == '-l':
                action = 4
            elif key == '-c':
                action = 0
            elif key == '-u':
                user['user'] = value
            elif key == '-i':
                user['muid'] = int(value)
            elif key == '-p':
                user['port'] = int(value)
            elif key == '-k':
                user['passwd'] = value
            elif key == '-o':
                if value in fast_set_obfs:
                    user['obfs'] = fast_set_obfs[value]
                else:
                    user['obfs'] = value
            elif key == '-O':
                if value in fast_set_protocol:
                    user['protocol'] = fast_set_protocol[value]
                else:
                    user['protocol'] = value
            elif key == '-g':
                user['obfs_param'] = value
            elif key == '-G':
                user['protocol_param'] = value
            elif key == '-s':
                user['speed_limit_per_con'] = int(value)
            elif key == '-S':
                user['speed_limit_per_user'] = int(value)
            elif key == '-m':
                if value in fast_set_method:
                    user['method'] = fast_set_method[value]
                else:
                    user['method'] = value
            elif key == '-f':
                user['forbidden_port'] = value
            elif key == '-t':
                val = float(value)
                try:
                    val = int(value)
                except:
                    pass
                user['transfer_enable'] = int(val * 1024) * (1024 ** 2)
            elif key in ('-h', '--help'):
                print_server_help()
                sys.exit(0)
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    manage = MuMgr()
    if action == 0:
        manage.clear_ud(user)
    elif action == 1:
        if 'user' not in user and 'port' in user:
            user['user'] = str(user['port'])
        if 'user' in user and 'port' in user:
            manage.add(user)
        else:
            print("You have to set the port with -p")
    elif action == 2:
        if 'user' in user or 'port' in user:
            manage.delete(user)
        else:
            print("You have to set the user name or port with -u/-p")
    elif action == 3:
        if 'user' in user or 'port' in user:
            manage.edit(user)
        else:
            print("You have to set the user name or port with -u/-p")
    elif action == 4:
        manage.list_user(user)
    elif action is None:
        print_server_help()

if __name__ == '__main__':
    app=MuMgr()
    user={
        'user':'mtest',
        'port':6088
    }
    app.add(user)
    app.list_user(user)
