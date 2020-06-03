## DADASHOP  测试配置文档  Ubuntu18.04

以下文档以python教学环境为准

### 1.  安装nginx

```shell
# 安装nginx
tarena@aid:~$ sudo apt-get install nginx

# 检查nginx版本
tarena@aid:~$ nginx -v
nginx version: nginx/1.14.0 (Ubuntu)

# 查看nginx启动状况
tarena@aid:~$ sudo service nginx status

# 启动/重启/停止等服务  两种方式如下
tarena@aid:~$ sudo service nginx [start|restart|stop]
tarena@aid:~$ sudo sudo /etc/init.d/nginx [start|restart|stop]


在浏览器中可以输入本地的回环地址查看
http://127.0.0.1
```

ubuntu版本中的nginx HTML 页面的路径为 　**/var/www/html**



### 2. nginx 配置 - 前端页面

sudo vim /etc/nginx/conf.d/dadashop.conf　　(每次修改配置文件后要重启nginx服务)

```nginx
server {
        
        listen 7000 default_server;
        listen [::]:7000 default_server;
        server_name __;

        root /var/www/html;
        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }
        

}
    
```



配置完毕后可在终端中 直接输入 nginx -t   查看配置文件是否有语法错误

```shell
tarena@tedu:~$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
#此例为配置文件 检查通过
```

配置通过后终端中 直接输入 nginx -s reload   平滑重启nginx【访问用户无感知】

```python
nginx -s reload 平滑重启，用户无感知

sudo /etc/init.d/nginx restart 强行重启，这是先kill进程再重启
```



### 3. 创建目录 /var/www/html/dadashop/

```shell
tarena@aid:~$ sudo mkdir /var/www/html/dadashop/
```

将client目录下的static和templates目录放到/var/www/html/dadashop目录下

```shell
#假设clietn文件夹已在ubuntu主目录下，则执行如下命令即可
sudo cp -fr client/. /var/www/html/dadashop/
```

查看

```shell
执行超级用户权限：sudo su
			   cd /var/www/html/dadashop
```



### 4. 验证

浏览器输入 http://127.0.0.1:7000/dadashop/templates/index.html  即可



测试跨域请求

```shell
sudo su
cd /var/www/html/dadashop/templates
vim login.html
103行的url改成：url:'http://127.0.0.1:8000/test_cors,

效果是：用火狐浏览器打开http://127.0.0.1:7000/dadashop/templates/login.html
设置登录名和密码，点击登录后。F12调试器里面网络显示两个200请求，预检跨域和post提交请求，post提交请求的响应是views.py中HttpResponse的‘hahahaha'。如果post请求403响应，应该是django里面settings.py启用了csrf中间件，可以暂时禁掉。
```






