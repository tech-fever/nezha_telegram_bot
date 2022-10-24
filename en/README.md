[English version](https://github.com/tech-fever/nezha_telegram_bot/tree/main/en)

# Nezha Monitoring API query telegram robot

This project is a derivative project of the [Nezha Monitoring](https://github.com/nezhahq) , based on the API to query the server information of the Nezha panel in real time.

## Program features

- [x] Support Chinese/English multi-language switch
- [x] Support tag statistics (CPU, disk, memory, upstream and downstream speed, traffic statistics, etc.)
- [x] Support real-time refresh of single server data
- [x] Support keyboard interactive query
- [x] Support query by command
- [x] Support adding bot to group, privacy protection of bot replies in group chat
- [x] Support bot messages automatic deletion in group chat within 20 seconds
- [x] Support docker deployment
- [ ] Support websocket statistics, no API required
- [ ] Added the function of ranking list (entertainment) [ with [fake-nezha-agent](https://github.com/dysf888/fake-nezha-agent), this function will be temporarily put on hold]

## Commands list

Command | Description | Private chat only
--- | --- | ---
start | Getting started with the keyboard main menu | ✔️
help | help message | ❌
add | Add Nezha monitoring url link and token | ✔️
url | Add Nezha monitoring url link | ✔️
token | Add Nezha monitoring token | ✔️
info | Get saved Nezha monitoring url link and token | ✔️
delete | Delete saved Nezha monitoring url link and token | ✔️
id | Add an integer id after the command to query the information of a single server (refresh button only available in private chat) | ❌
all | Query statistics for all servers | ❌
search | Search for keywords in server names (multiple keywords supported, split by spaces) | ❌

## Show results

![image](https://user-images.githubusercontent.com/105153585/175813727-bef77a8e-ff46-4fd4-b41b-43902abf6159.png#pic_left) ![image](https://user-images.githubusercontent.com/105153585/175813645-4df4f4c7-2591-4133-9645-21c7db2f62ab.png#pic_right)

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
mkdir nezha && cd nezha
wget https://raw.githubusercontent.com/tech-fever/nezha_telegram_bot/main/conf.ini.example -O conf.ini
vim conf.ini
```

Modify the configuration file `conf.ini` . Download `docker-compose.yml` to a local folder and run

```bash
wget https://raw.githubusercontent.com/tech-fever/nezha_telegram_bot/main/docker-compose.yml
docker-compose up -d
```

#### Restart the robot

```bash
docker-compose down
docker-compose up -d
```

#### version upgrade

```bash
docker-compose pull # pull the new version
# restart
docker-compose down
docker-compose up -d
```

Note that if there is a newer version when you pulling, there will be leftover images of the old version, and the tag will be None. Running the command `docker images` looks like this:

```
REPOSITORY                                          TAG         IMAGE ID       CREATED              SIZE
techfever/nezha_telegram_bot                        latest      b9f3543f80ef   About a minute ago   69.1MB
techfever/nezha_telegram_bot                        <none>      1d92ec28e0fb   7 hours ago          69.1MB
```

Then, the following line is the old version image, which can be deleted.

```bash
docker images
docker rmi image_ID_to_delete # in this case it is 1d92ec28e0fb
```

## Language development

This project uses `crowdin` for multilingual translation. If you have suggestions on languages, or you would like to contribute new languages, please go to the project address: https://zh.crowdin.com/translate/telegram-bot-nezha/

(It is the first time for the author to use `crowdin` .But I found that it is quite easy to use)

You can also download the `myapplication.pot` file in the project to local for editing and development.

## Inspiration

- [Nezha Panel](https://github.com/naiba/nezha)
- [nezha_api_tgbot](https://github.com/spiritLHLS/nezha_api_tgbot) by [spiritLHLS](https://github.com/spiritLHLS)
- [NezhaBot](https://github.com/Erope/NezhaBot) by [Erope](https://github.com/Erope)
