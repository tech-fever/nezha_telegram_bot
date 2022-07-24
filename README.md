[English version](https://github.com/tech-fever/nezha_telegram_bot/tree/main/en)

# 哪吒面板API查询机器人
本项目是[哪吒面板](https://github.com/nezhahq)衍生项目，基于API实时查询哪吒面板的服务器信息。

## 项目特色
- [x] 支持中/英多语言切换
- [x] 支持分组统计(CPU磁盘内存上下行速度流量统计等)
- [x] 支持实时刷新单个服务器数据
- [x] 支持键盘互动查询
- [x] 支持命令直接查询
- [x] 增加群聊判断，限制群聊可发送命令
- [x] 增加群聊内5秒自动删除信息
- [x] 支持docker部署
- [ ] 增加websocket统计，无需API【】
- [ ] 增加排行榜功能(娱乐)【[fake-nezha-agent](https://github.com/dysf888/fake-nezha-agent)出来了大概率不会再做这个功能了】

## 命令列表
| 命令 | 功能 | 仅私聊 |
| --- | --- | --- |
| start | 开始使用键盘主菜单 | ✔️ |
| help | 帮助列表 | ❌ |
| add | 添加面板链接和token | ✔️ |
| url | 添加面板链接 | ✔️ |
| token | 添加面板token | ✔️ |
| info | 获取保存的面板链接和token | ✔️ |
| delete | 删除保存的面板链接和token | ✔️ |
| id | 命令后面添加整数id，来进行单个服务器信息查询（私聊带刷新按钮，群聊不带） | ❌ |
| all | 查询所有服务器的统计信息 | ❌ |
| search | 在服务器名字中搜索关键字（支持多个，用空格分开） | ❌ |

## 效果展示
![image](https://user-images.githubusercontent.com/105153585/175813727-bef77a8e-ff46-4fd4-b41b-43902abf6159.png#pic_left)
![image](https://user-images.githubusercontent.com/105153585/175813645-4df4f4c7-2591-4133-9645-21c7db2f62ab.png#pic_right)



## 项目部署
### 直接python运行
#### 环境要求
- 本项目使用 `python3` 。首先保证本地已经安装相应环境。
- 如部署在国内服务器，请参考 https://nezhahq.github.io/guide/q1.html 建立telegram bot api反代，
#### 安装步骤
首先将项目clone到本地，打开项目文件夹，执行
```bash
pip install -r requirements.txt
```
复制一份 `conf.ini` 。
```bash
cp conf.ini.example conf.ini
vim conf.ini
```
填入下列信息：
```ini
[TELEBOT]
# 机器人token
BOT_TOKEN = 
# 国内服务器需要telegram bot api反代，请参考https://nezhahq.github.io/guide/q1.html
# 国外服务器留空即可
BASE_URL =
BASE_FILE_URL =

[DEVELOPER]
# 填入开发者telegram userid
DEVELOPER_CHAT_ID = 
```

然后运行项目即可
```bash
python3 main.py
```

如果想要长期部署，请使用 `tmux` 或者 `screen` 运行。
例如 `tmux` 安装：
```bash
# Debian or Ubuntu
apt install tmux
# CentOS or RedHat
yum install tmux
```
`tmux` 使用：
```bash
tmux new -s telebot
cd nezha_telegram_bot
python3 main.py
```
然后键盘按下 `ctrl + b d` 即可 detach 当前窗口。

> 注：没有试过在windows进行部署，如果部署的话，应该需要注释掉main.py中的
> `os.environ['TZ'] = 'Asia/Shanghai'` 和 `time.tzset()`
### Docker 部署【推荐】
将配置文件下载至本地然后编辑
```bash
mkdir nezha && cd nezha
wget https://raw.githubusercontent.com/tech-fever/nezha_telegram_bot/main/conf.ini.example -O conf.ini
vim conf.ini
```
对配置文件 `conf.ini` 进行修改。
将 `docker-compose.yml` 下载至本地文件夹，然后运行
```bash
wget https://raw.githubusercontent.com/tech-fever/nezha_telegram_bot/main/docker-compose.yml
docker-compose up -d
```
#### 重启机器人
```bash
docker-compose down
docker-compose up -d
```
#### 版本升级
```bash
docker-compose pull # 拉取新版本
# 重启
docker-compose down
docker-compose up -d
```
注意此时如果有新版本的话，会有旧版本镜像残留，tag会是None。运行命令 `docker images` 类似于下面这样：
```
REPOSITORY                                          TAG         IMAGE ID       CREATED              SIZE
techfever/nezha_telegram_bot                        latest      b9f3543f80ef   About a minute ago   69.1MB
techfever/nezha_telegram_bot                        <none>      1d92ec28e0fb   7 hours ago          69.1MB
```
这个时候，下面这行就是旧版本镜像，可以将其删除。
```bash
docker images
docker rmi 需要删除的镜像ID # 在这个例子里就是1d92ec28e0fb
```

## 语言开发
本项目使用 `crowdin` 进行多语言翻译，如对语言有建议/想要贡献新的语言请至项目地址：
https://zh.crowdin.com/translate/telegram-bot-nezha/

成为翻译者：
https://crwd.in/telegram-bot-nezha

（作者也是第一次用 `crowdin` ，但是发现还蛮好上手的）

也可以下载项目中的 'myapplication.pot' 文件至本地进行编辑开发。

## 感谢
- [哪吒面板](https://github.com/naiba/nezha)
本项目受启发于
- [nezha_api_tgbot](https://github.com/spiritLHLS/nezha_api_tgbot)，作者[spiritLHLS](https://github.com/spiritLHLS)
- [NezhaBot](https://github.com/Erope/NezhaBot)，作者[Erope](https://github.com/Erope)
