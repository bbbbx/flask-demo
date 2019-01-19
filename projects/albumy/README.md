# Albumy

一个图片分享社交网站，类似 Ins？

## 配置

在 `project` 目录下新建一个 `.env` 文件，填入：

```env
SECRET_KEY="随便加点随机字符"
MAIL_SERVER=""    # 邮件服务器，例如 "smtp.example.com"
MAIL_USERNAME=""  # 邮件服务器用户，例如 "user@example.com"
MAIL_PASSWORD=""  # 邮件服务器用户对应的密码
```

更多配置见 `albumy/settings.py` 文件。

## 运行

### 使用 pipenv

`pipenv shell` 激活 pipenv 虚拟环境后，在 `project` 目录下运行：

```bash
$ pipenv install  # 安装依赖
$ flask run       # 运行
```
