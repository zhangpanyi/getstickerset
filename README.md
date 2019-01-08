# getstickerset
getstickerset 是一个可以下载 Telegram 贴纸集合的Bot。能够把聊天对话框中的 Sticker 集合整体打包，然后 Bot 会把打包后的压缩文件发送到当前聊天对话框。

你只需要对着 Sticker 消息回复一句 `/zip`，它就会知道该工作了。

在Telegram搜索用户 `@getsticker_bot` 或者打开链接 [http://telegram.me/getsticker_bot](http://telegram.me/getsticker_bot) 立即使用。

## 部署指南

**1. 安装 Docker**
* [Get Docker CE for CentOS](https://docs.docker.com/install/linux/docker-ce/centos/)
* [Get Docker CE for Debian](https://docs.docker.com/install/linux/docker-ce/debian/)
* [Get Docker CE for Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)
* [Get Docker CE for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

将当前用户添加到 `docker` 组：
```
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart
newgrp docker
```

**2. 安装 docker-compose**
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
参考文档：[https://docs.docker.com/compose/install/#install-compose](https://docs.docker.com/compose/install/#install-compose)

**3. 快速启动**
```
git clone git@github.com:zhangpanyi/getstickerset.git
cd getstickerset
```

打开 `docker-compose.yml` 文件，将字符串 `<Telegram bot token>` 修改为自己Bot的Token。

```
docker-compose build
docker-compose up -d
```