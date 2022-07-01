# Nezha Monitoring API query telegram robot

This project is a derivative project of the [Nezha Monitoring](https://github.com/nezhahq) , based on the API to query the server information of the Nezha panel in real time.

## Program features

- [x] Support Chinese/English multi-language switch
- [x] Support tag statistics (CPU, disk, memory, upstream and downstream speed, traffic statistics, etc.)
- [x] Support real-time refresh of single server data
- [ ] Add websocket (to query without API)
- [ ] Added leaderboard function (entertainment)
- [ ] Add group chat judgment, limit group commands available in chats
- [ ] Added automatic deletion of messages within 5 seconds of group chat

## Project deployment

### Directly run with python

#### Environmental requirements

- This project uses `python3` . First, ensure that the corresponding environment has been installed locally.
- If it is deployed on a server located in Mainland China, please refer to https://nezhahq.github.io/guide/q1.html to create a telegram bot api inversion,

#### Installation steps

First clone the project to the local, open the project folder, execute

```bash
pip install -r requirements.txt
```

Make a copy of `conf.ini` .

```bash
cp conf.ini.example conf.ini
vim conf.ini
```

Fill in the following information:

```ini
[TELEBOT]
# telegram bot token
BOT_TOKEN =
# For Mainland China servers only
# If you do not need reverse proxy for telegram bot api, JUST LEAVE it empty
BASE_URL =
BASE_FILE_URL =

[DEVELOPER]
# telegram userid of the developer (your telegram userid)
DEVELOPER_CHAT_ID =
```

Then run the project

```bash
python3 main.py
```

For long-term deployments, run with `tmux` or `screen` . For example `tmux` installation:

```bash
# Debian or Ubuntu
apt install tmux
# CentOS or RedHat
yum install tmux
```

Use `tmux`:

```bash
tmux new -s telebot
cd nezha_telegram_bot
python3 main.py
```

Then press `ctrl + b d` on the keyboard to detach the current window.

> Note: I haven't tried deploying on windows. If deploying, you should comment out `os.environ['TZ'] = 'Asia/Shanghai'` and `time.tzset()` in main.py

### Docker deployment [recommended]

Download the configuration file locally and edit it

```bash
mkdir nezha_telegram_bot && cd nezha_telegram_bot
wget https://raw.githubusercontent.com/tech-fever/nezha_telegram_bot/main/conf.ini.example -O conf.ini
vim conf.ini
```

Download `docker-compose.yml` to a local folder (same folder as `conf.ini` ) and run

```bash
wget https://raw.githubusercontent.com/tech-fever/nezha_telegram_bot/main/docker-compose.yml
docker-compose up -d
```

## Language development

This project uses `crowdin` for multilingual translation. If you have suggestions on languages, or you would like to contribute new languages, please go to the project address: https://zh.crowdin.com/translate/telegram-bot-nezha/

(It is the first time for the author to use `crowdin` .But I found that it is quite easy to use)

You can also download the `myapplication.pot` file in the project to local for editing and development.

## Grateful for

- [Nezha Monitoring](https://github.com/naiba/nezha)
- This project is inspired by [nezha_api_tgbot](https://github.com/spiritLHLS/nezha_api_tgbot) whose author is  [spiritLHLS](https://github.com/spiritLHLS)
