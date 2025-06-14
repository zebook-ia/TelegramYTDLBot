# <p align="center">YouTube Downloader Bot</p>
<p align="center">A Telegram Bot to Download YouTube Videos upto 4K under 2GB.</p>
<p align="center"><i>(Only for Educational Purposes)</i></p>

#
## Features 
- ✅ Fast Downloads
- ✅ Choose video quality before download.
- ✅ Downloading Queue for users.
- ✅ Max video upload size : 2GB
- ✅ Save server side resources.
- ✅ No Developer side limits.

## How to Deploy
### 1. Setup Environment Variables
- Get your [BOT_API_KEY](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) from here.
- Create .env file
- Paste this code into your file and replace with your own values.
```
BOT_API_KEY = "9999999999:AAHePL8-xSzjOlnF5dRGiwhNyxxZsS3u7f4" # Replace with your own token
# Optional: point to your local API server to enable 2GB uploads
BOT_API_URL = "http://localhost:8081"
```
- Save it!
  
#
### 2. Install Dependencies
```
git clone https://github.com/hansanaD/TelegramYTDLBot.git;
cd TelegramYTDLBot;
pip install -r requirements.txt;
```
#
### 3. Run api server locally (optional)
You can choose not to use this service.\
But then you won't be able  to **upload files up to 2000 MB** and get these [features](https://core.telegram.org/bots/api#using-a-local-bot-api-server).

- Generate your instructions from [here](https://tdlib.github.io/telegram-bot-api/build.html). _(This step might take upto 20 mins.)_
- Go to:
- ```
  cd telegram-bot-api/bin
  ```
- Get API ID & HASH from [here](https://core.telegram.org/api/obtaining_api_id). (Watch this [Tutorial](https://www.youtube.com/watch?v=8naENmP3rg4) to get help.)
- Start the server. (Remember to replace the values with your own values):
- ```
  ./telegram-bot-api --api-id=XXXXX --api-hash=XXXXXXXXXXXX --http-port=8081 --local
  ```

Read the instructions on [eternnoir/pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/#using-local-bot-api-sever) and [tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api) for more information.
#
### 4. Run your bot
- open a new "[screen](https://www.geeksforgeeks.org/screen-command-in-linux-with-examples/)" or tab on your terminal.
- run: ```python bot.py```

**both script & api server should run at the same time order to work.**

### 5. Deploy with Docker
1. Create a `.env` file containing your `BOT_API_KEY` and optional `BOT_API_URL`.
2. Build and start the container using docker-compose:
   ```bash
   docker-compose up -d --build
   ```
The compose file builds the image for `linux/amd64` so it runs on an x86 VPS
   even if you build from an Apple Silicon machine. Traefik is configured to
   expose the bot at **bot.sherlockramos.tech**.

## API

The bot exposes a small command based API over Telegram. Interact using the
standard Telegram Bot API by sending messages to your bot. Below are the
available endpoints and their behaviour.

### Endpoints

| Command/Action | Description |
|---------------|-------------|
| `/start` | Greet the user and provide a short introduction. |
| `/help` | Display instructions on how to download a video. |
| `YouTube link` | Send any message containing a valid YouTube URL. The bot will reply with a list of quality options as inline buttons. |
| `Quality button` | When a button is pressed the bot downloads the video and uploads it back. |

### Request and Response Format

All interactions occur via Telegram messages. Requests are regular text messages
or callback data from inline buttons. Responses are text messages or video
files. Example flows:

```text
User: /start
Bot: Hello, I'm a Simple Youtube Downloader!👋

User: /help
Bot: <b>Just send your youtube link and select the video quality.</b> …

User: https://youtu.be/dQw4w9WgXcQ
Bot: Choose a stream:
  [360p] [720p]

User presses 720p button
Bot: sends the video file (if under 2GB)
```

### Limitations

- Files larger than **2 GB** will not be uploaded; choose a lower quality if the
  selected stream exceeds this size.
- Only YouTube links are recognized.
- Without a local Bot API server (`BOT_API_URL`) uploads are limited to 50 MB by
  Telegram's default servers.
#

## Disclaimer
This repository is intended for educational and personal use only. The use of this repository for any commercial or illegal purposes is strictly prohibited. The repository owner does not endorse or encourage the downloading or sharing of copyrighted material without permission. The repository owner is not responsible for any misuse of the software or any legal consequences that may arise from such misuse

- **APIs : [y2mate-api](https://github.com/Simatwa/y2mate-api/) , [pytelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/)**
- **Contact for issues : [@dev00111](https://t.me/dev00111)**
#
_Sorry for my bad english and my messy documentation. 😶_


