# Shadowsocks web powered by django

## Functions:

- [x] 1、add user

- [x] 2、delete user

- [x] 3、change settings

## How to use? 

this web is working with another ssr shell, ssrmu.sh [https://github.com/ToyoDAdoubi/doubi](https://github.com/ToyoDAdoubi/doubi), download that shell and run it before you start this web.

To start this web is nothing different from starting a normal django web.

You need edit the  ssr_folder in line 13 of ss/views.py ,if you use the shell mentioned before ,the folder is '/usr/local/shadowsocksr'

If you use nginx+uwsgi to start this web, conf files could be as follow:

> * nginx server conf
```
server {
	listen 80;
	server_name yourdomain.com;
	location / {
		include uwsgi_params;
		uwsgi_pass 127.0.0.1:8008;
		uwsgi_read_timeout 5;
		auth_basic "server";
		auth_basic_user_file /etc/nginx/passwd.db; 
	}
}
```
> * uwsgi.ini 
```
[uwsgi]
socket = :8008
chdir           = /yourfolder/ssweb
module          = ssweb.wsgi
master          = true
processes       = 1
vacuum          = true
```

Maybe you need to google how to start a django web with nginx and uwsgi

For security concern, authorization in nginx or other web server is recommanded.

![example_pic](https://i.loli.net/2018/10/20/5bcaf4623ed13.png)

![example_pic](https://i.loli.net/2018/10/20/5bcb2aae44e13.png)
![example_pic](https://i.loli.net/2018/10/20/5bcb28ef16453.png)
![example_pic](https://i.loli.net/2018/10/20/5bcb28ef17590.png)
