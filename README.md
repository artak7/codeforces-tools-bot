# CodeForces Tools bot 

The code of this repository contains telegram bot on python using aiogram 3 framework that can be used to receive notifications from [Codeforces](https://codeforces.com) via API when new participants take part in the contest specified in the configs. Also bot contains functionality of 
[my previous work](https://github.com/artak7/CFAPI2JSON4unfreeze_standings) that convert information about contest to special JSON format [S4RIS](https://github.com/OStrekalovsky/S4RiS-StanD) or [neoSaris](https://github.com/equetzal/neoSaris) and then you can use it in these apps. These apps simulate what happens in the frozen time during a competitive programming competition.

## Motivation 

Recently I was the organizer of the сontest at codeforces.com platform in which it was possible to take part for several months. So I needed to periodically monitor the results table and I decided to make this bot. In addition, the participants in the table were anonymous and I decided to add function to set them names and create private results table.

## Navigate

- [How to Use](#how-to-use)
    - [Init project](#init-project)
    - [Configure environment variables](#configure-environment-variables)
        - [Bot config](#bot-config)
        - [Contest config](#contest-config)
        - [Private contest config](#private-contest-config)
    - [Application start (local)](#application-start-local)
- [Roadmap](#roadmap)

## How to Use

### Init project

```bash
$ git clone https://github.com/artak7/codeforces-tools-bot project_name
$ cd project_name
$ pip install -r requirements.txt
```

### Configure environment variables

> Copy variables from .env.example file to .env

```bash
$ cp .env.example .env
```

### Bot config

> Create `BOT_TOKEN` via [@BotFather](t.me/botfather)

`BOT_TOKEN` - your telegram bot token (required)

### Contest config

> Not required. You can add contest configs later via bot command [/set_configs]().
 If you need more about configs of contest you can read [here](https://codeforces.com/apiHelp)

`FROZEN_TIME` - int

`SHOW_UNOFFICIAL` - bool (true, false) 

`IS_PRIVATE_GROUP` - bool (true, false)

> **Note!** 
These configs you can find in the address link of your group

> Example: https://codeforces.com/group/GROUP_CODE/contest/CONTEST_ID

`GROUP_CODE` - hash

`CONTEST_ID` - int

### Private contest config

> Required if contest located in private group. 

> **Note!** You need to have manager rights and create `CF_API_KEY`, `CF_API_SECRET` [here](https://codeforces.com/settings/api)

`AS_MANAGER` - bool (true, false)

`CF_API_KEY` - hash

`CF_API_SECRET` - hash


## Application start (local)

```bash
$ python main.py
```

##### Note 
For launching [/unfreeze standings]() command's files you can use these apps https://neosaris.huronos.org or http://ostrekalovsky.github.io/S4RiS-StanD/

# Roadmap
- [ ] Deploy
- [ ] Create standings html page with setted names
- [ ] Add keyboards
- [ ] Add subscribe to update via pyscheduler
- [ ] add sessions and db with alembic
- [ ] add i18n
- [ ] fix problem with registering commands in command menu
