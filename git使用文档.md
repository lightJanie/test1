![git结构](img/git.jpeg)

1. 从远程仓库clone到本地

   ```python
   git支持https和git两种传输协议，git分享链接时会有两种可选。
   
   两种方法的区别：
   git使用https协议，每次pull, push都会提示要输入密码。
   使用git协议，配置好ssh密钥，这样免去每次都输密码的麻烦。
   
   一.使用https协议clone
   git clone https://github.com/TheAlgorithms/Python.git

   
    
   二.使用git传输协议
1.本地生成秘钥对
   tarena@tedu:~$ ssh-keygen -t rsa -C syuying07@163.com #生成公钥的命令
Generating public/private rsa key pair.
   Enter file in which to save the key (/home/tarena/.ssh/id_rsa):#此处直接enter 
Enter passphrase (empty for no passphrase): #输入密码123456
   Enter same passphrase again: 
   Your identification has been saved in /home/tarena/.ssh/id_rsa.
   Your public key has been saved in /home/tarena/.ssh/id_rsa.pub.
   The key fingerprint is:
   SHA256:UccV5bF7R2k2mNRGSJt6s+sywNSK+mzm5foJt8qG/hs syuying07@163.com
   The key's randomart image is:
   +---[RSA 2048]----+
   |          ..o+*=.|
   |         . .o.=++|
   |        . .  =.*o|
   |         o .. o.o|
   |        S .. o .o|
   |       . +  . o o|
   |      oE o.  .   |
   |     oo+* oo  .  |
   |    ..BX==  +o   |
   +----[SHA256]-----+
   tarena@tedu:~$ pwd
   /home/tarena
   tarena@tedu:~$ cd .ssh
   tarena@tedu:~/.ssh$ ls
   id_rsa  id_rsa.pub  #.pub后缀的就是公钥
   2.设置远程仓库上的公钥
   登陆你的github帐户。点击你的头像，然后 Settings -> 左栏点击 SSH and GPG keys -> 点击 New SSH key
   add key之后验证是否能正常工作
   tarena@tedu:~/.ssh$ ssh -T git@github.com
   Hi lightJanie! You've successfully authenticated, but GitHub does not provide shell access. #这样就表示公钥配对设置成功，可以用git协议clone了。
   ```
   
   如何创建分支
   
   如何打补丁，1.0是发行版，将修改上传到1.1未发行版。
   
   
   
   1.本地使用
   
   ```python
   git init
   git status
   git add <filename>
   git add .
   git rm --cached 文件名   # index/repository->workspace
   git commit -m '备注信息'
   git reset <commitID> --hard
   git tag v1.0 <commitID> -m '备注信息'
   git reset --hard v1.0 #取代commitID,实现重要节点的跳转
   git log
   git reflog
   ```
   
   2.分支
   
   ```python
   git branch
   git checkout -b <branch name>   新切出来分支
   git checkout master
   ```
   
   3.合并
   
   ```python
   git merge <branch name> 挨个合并分支,出现冲突，手动处理
   ```
   
   4.远程仓库
   
   ```python
   A:切出新分支并上传至远程仓库:
   git clone git协议
   git checkout -b <branch name>
   git push --set-upstream origin <branch name> 第一次上传先要创建远端上游分支
   git push
   
   B:获取远端的新分支并更新数据至本地
   git clone git协议
   git fetch 查看远程仓库信息
   git checkout <branch name>
   git pull
   ```
   
   