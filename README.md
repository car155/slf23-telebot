# SLF Telegram Bot

This is the official Telegram Bot for NUS SLF 2022.

## Deployed Bot

[link to be added]()

## Installation

### 1. Create a Telegram Bot using Bot Father

1. Go to Telegram and find [Bot Father](https://t.me/botfather)
2. Use `/newbot` to create your telegram bot
3. Copy down the `token` (a string along the lines of `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`) and store it safely and privately for later
heroku git:remote -a <app-name>
Reference: [Creating a Telegram bot](https://core.telegram.org/bots#6-botfather)

### 2. Installing Heroku CLI (if haven't done so)

1. Create a Heroku account [here](https://signup.heroku.com/)
2. Download Heroku CLI using this [guide](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
3. Sign in to your account

### 3. Downloading dependencies

1. `git clone git@github.com:yyj-02/slf-telegram-bot.git`
2. Enter the main repository: `cd slf23-telebot` (if haven't done so)
3. **(Optional but recommended)** Create a virtual environment
    - `pip install virtualenv`
    - `python -m venv venv`
    - (Windows) `venv\Scripts\activate`  
    (MacOS/Linux) `source venv/bin/activate`
4. `pip install -r requirements.txt`

### 4. Creating a Heroku app

1. Type this command, replace the app-name with your app name (without bracket) `heroku create -a <app-name>`
2. Add to remote `heroku git:remote -a <app-name>`
3. Check the remote has been set for your app: `git remote -v`

Reference: [Creating a Heroku app](https://devcenter.heroku.com/articles/creating-apps)

### 5. Creating a Google Service Account

1. Create a Google Service Account with access to the official spreadsheet using this [guide](https://docs.gspread.org/en/latest/oauth2.html#service-account)
2. Enable the APIs and create credentials
3. Goto “Manage service accounts”
4. Press on ⋮ near recently created service account and select “Manage keys” and then click on “ADD KEY > Create new key”
5. Select JSON key type and press “Create”
6. You will receive something similar to the content below, store it privately for later
```
{
    "type": "service_account",
    "project_id": "api-project-XXX",
    "private_key_id": "2cd … ba4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
    "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
    "client_id": "473 … hd.apps.googleusercontent.com",
    ...
}
```
7. Go to the official spreadsheet and share it with the `client_email`

### 6. Creating an environment variables file

1. `touch .env`
2. Key in the relevant details in the `.env` file, e.g.
```
BOT_TOKEN=110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
PROJECT_ID=xxx
PRIVATE_KEY_ID=92e705df3bec7e5a6f7f3b928bdf8b870d916280
PRIVATE_KEY=... # without -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY-----\n, put them in '' as well
CLIENT_EMAIL=xxx@xxxx.iam.gserviceaccount.com
CLIENT_ID=114923329371738492284
CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/xxx.iam.gserviceaccount.com
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/1M82bxY_kgvPSRi7290nv82m-11IrrJ0QmoL73bncRLQkk/edit#gid=0
```
3. Setting up the environment variables in Heroku using this [guide](https://devcenter.heroku.com/articles/config-vars):
   `heroku config:set TELEGRAM_TOKEN=110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`
   ``
### 7. Pushing to Heroku

1. `git add . && git commit -m "<your-message>"` (if haven't done so)
2. `git push heroku main`

## Features

* Schedule of performance
* ... and more

## Todo

- [ ] Update picture and year
- [ ] Update [spreadsheet](https://docs.google.com/spreadsheets/d/1M5wxKY_kgvPSRix4uRBvpE-11IrrJ0QmoLzVysRLQkk/edit#gid=0)
- [ ] Deploy to heroku and bot father