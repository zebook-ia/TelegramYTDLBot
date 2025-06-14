This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
modules/
  checker.py
  myqueues.py
  ytdownloader.py
.gitignore
bot.py
README.md
requirements.txt
```

# Files

## File: modules/myqueues.py
````python
import time
from queue import Queue
from modules.ytdownloader import download

download_queue = Queue()

def download_worker(bot, download_queue):
    while True:
        message, videoURL, receivedData = download_queue.get()
        try:
            download(bot=bot, message=message, userInput=receivedData, videoURL=videoURL)

        except Exception as e:
            print(f"Error downloading file: {e}")
        download_queue.task_done()

        # Check if the queue is empty
        if download_queue.empty():
            print("All downloads have been completed. Queue is empty now.\n\n")
````

## File: modules/ytdownloader.py
````python
import os
from y2mate_api import Handler
import requests
import pytube

# Download the YouTube Video
def download(bot, message, userInput, videoURL):

    api = Handler(videoURL)
    yt = pytube.YouTube(videoURL)

    mediaPath = f"{os.getcwd()}/vids"

    # Download the video using user's input
    for video_metadata in api.run(quality=userInput):
        # print(video_metadata)
        
        if not os.path.exists(mediaPath):
            os.makedirs(mediaPath)

        downloadMsg = bot.send_message(chat_id=message.chat.id, text="<b>Downloading...📥</b>")

        vidFileName = f"{ video_metadata['vid'] }_{ video_metadata['q'] }.{ video_metadata['ftype'] }"

        try:
            # Start Downloading the Video
            api.save(third_dict=video_metadata, dir="vids", naming_format=vidFileName, progress_bar=True)
        except Exception as e:
            bot.reply_to(message, f"Error downloading video: {e}")

        bot.edit_message_text(chat_id=downloadMsg.chat.id, message_id=downloadMsg.message_id, text="<b>Uploading...📤</b>")

        # Upload the video to Telegram
        try:
            print(vidFileName, "Uploading..")
            bot.send_video(
                message.chat.id, 
                open(f"vids/{vidFileName}", 'rb'), 
                thumb=requests.get(yt.thumbnail_url).content,
                width=1920, 
                height=1080,
                # caption= f" <i>Thanks for Using @{bot.get_me().username }.</i> ", 
                caption=f"""
                <b>Title:</b><i> { yt.title } </i>
<b>URL:</b><i> { videoURL } </i>
<b>Quality:</b><i> { video_metadata['q'] } </i>

<i><b>Thanks for Using @YoutubeDownloader4K0_bot.</b></i>""",
            )

            print("File was uploaded/sent to the User.")

        except Exception as e:
            bot.reply_to(message, f"Error uploading video: {e}")
            print(vidFileName, f": Error uploading video: {e}")

        bot.delete_message(downloadMsg.chat.id, downloadMsg.message_id)

        # Delete the Media files after download.
        os.remove(f"{mediaPath}/{vidFileName}")
        print(vidFileName, ": Done!")
        print("-------------------------------")
````

## File: modules/checker.py
````python
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from y2mate_api import Handler


def linkCheck(bot, message):

    linkFilter = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    userLinks = re.findall(linkFilter, message.text)

    yt_link = []
    for link in userLinks:
        if 'youtube.com' in link or 'youtu.be' in link:
            yt_link.append(link)

    if yt_link:
        # bot.reply_to(message, "YouTube links found.")

        # global videoURL
        # global ytApi

        videoURL = yt_link[0]
        

        qualityChecker(bot=bot, message=message, videoURL=videoURL)

    else:
        bot.reply_to(message, "No YouTube links found!")


def qualityChecker(bot, message, videoURL):

    qualityCheckerMsg = bot.reply_to(message, "Looking for Available Qualities..🔎")

    ytApi = Handler(videoURL)

    q_list = ['4k', '1080p', '720p', '480p', '360p', '240p']
    # q_list.reverse()

    urlList = []

    def getVidInfo(r):
        for video_metadata in ytApi.run(quality=r):
        
            q = video_metadata.get("q")
            dlink = video_metadata.get("dlink")
            size = video_metadata.get("size")
            
            if dlink == None:
                pass
            else:
                urlList.append([q, size, dlink])
                # print(r, " fetched")
                
    # Iterate over q_list to check if res quality exist on that video
    for r in q_list:
        getVidInfo(r)

    # print(urlList)

    # Create a new list to show
    global showList
    showList = {}
    for count, item in enumerate(urlList, 1):
        del item[2] # Remove dlink from list
        q = item[0]
        # print(i)
        size = item[1] 
        showList.update( { count: { "q":q, "size": size }} )
    
    # print(showList)


    # Add Inline Buttons to get user input

    def gen_markup():
        markup = InlineKeyboardMarkup() 
        for value in showList.values(): 
            callbackData = f"{ value["q"] }#{ videoURL }"
            button = InlineKeyboardButton(text=f"{value['q']} ({value['size']})", callback_data=callbackData)
            markup.add(button)
        return markup
    

    bot.delete_message(qualityCheckerMsg.chat.id, qualityCheckerMsg.message_id)

    bot.reply_to(message=message, text="Choose a stream:", reply_markup=gen_markup())
````

## File: requirements.txt
````
aiohttp==3.9.3
aiosignal==1.3.1
amqp==5.2.0
annotated-types==0.6.0
anyio==4.2.0
appdirs==1.4.4
async-timeout==4.0.3
attrs==23.2.0
beautifulsoup4==4.12.3
billiard==4.2.0
Brotli==1.1.0
cachetools==5.3.2
celery==5.3.6
certifi==2023.11.17
cffi==1.16.0
charset-normalizer==3.3.2
click==8.1.3
click-didyoumean==0.3.1
click-plugins==1.1.1
click-repl==0.3.0
colorama==0.4.6
decorator==4.4.2
decouple==0.0.7
docopt==0.6.2
emoji==2.10.0
ffmpeg-progress-yield==0.7.8
ffmpeg-python==0.2.0
ffpb==0.4.1
frozenlist==1.4.1
future==0.18.3
google-api-core==2.17.1
google-api-python-client==2.123.0
google-auth==2.28.0
google-auth-httplib2==0.2.0
googleapis-common-protos==1.62.0
h11==0.14.0
httpcore==1.0.2
httplib2==0.22.0
httpx==0.26.0
idna==3.6
imageio==2.33.1
imageio-ffmpeg==0.4.9
kombu==5.3.7
markdown-it-py==3.0.0
mdurl==0.1.2
moviepy==1.0.3
multidict==6.0.5
mutagen==1.47.0
numpy==1.26.4
outcome==1.3.0.post0
pillow==10.2.0
pipreqs==0.4.13
proglog==0.1.10
prompt-toolkit==3.0.43
protobuf==4.25.3
pyasn1==0.5.1
pyasn1-modules==0.3.0
pycparser==2.22
pycryptodomex==3.20.0
pydantic==2.6.0
pydantic_core==2.16.1
pyee==11.1.0
Pygments==2.17.2
pygramtic==0.2.0
pyparsing==3.1.1
PySocks==1.7.1
pyTelegramBotAPI==4.15.4
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
python-ffmpeg==2.0.10
python-telegram-bot==20.8
python-telegram-bot-api==0.0.7
pytube==15.0.0
redis==5.0.2
requests==2.28.2
rich==13.7.0
rq==1.16.1
rsa==4.9
selenium==4.19.0
setuptools==70.0.0
six==1.16.0
sniffio==1.3.0
sortedcontainers==2.4.0
soupsieve==2.5
tabulate==0.9.0
tqdm==4.65.0
trio==0.25.0
trio-websocket==0.11.1
typing_extensions==4.9.0
tzdata==2024.1
uritemplate==4.1.1
urllib3==1.26.18
vine==5.1.0
wcwidth==0.2.13
websockets==12.0
wsproto==1.2.0
y2mate==1.0.0
y2mate-api==1.0.4
yarg==0.1.9
yarl==1.9.4
````

## File: .gitignore
````
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

/vids
.mp4
/telegram-bot-api
````

## File: bot.py
````python
import os
import telebot
import threading

from modules import checker, myqueues 

from dotenv import load_dotenv 
load_dotenv()

TOKEN = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
                      
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, "Hello, I'm a <b>Simple Youtube Downloader!👋</b>\n\nTo get started, just type the /help command.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(
        message,
        """
        <b>Just send your youtube link and select the video quality.</b> 😉
  <i>
  Developer: @dev00111
  Source: <a href="https://github.com/hansanaD/TelegramYTDLBot">TelegramYTDLBot</a></i>
        """, disable_web_page_preview=True,)
        
    

@bot.message_handler(func=lambda m: True)
def link_check(message):
    checker.linkCheck(bot=bot, message=message)
    # print(checker.videoURL)

# Callback handler for # getVidInfo() 
@bot.callback_query_handler(func=lambda call: [call.data == item for item in checker.showList])
def callback_query(call):

    data = call.data.split("#")
    receivedData = data[0]
    videoURL = data[1]
    # print(receivedData)
    
    bot.answer_callback_query(call.id, f"Selected {receivedData} to download.")
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    myqueues.download_queue.put((call.message, videoURL, receivedData))
    queue_position = myqueues.download_queue.qsize()

    
    if queue_position == 0 & 1:
        bot.send_message(call.message.chat.id, f"Download has been added to the queue.")
    else:
        bot.send_message(call.message.chat.id, f"Download has been added to the queue at #{queue_position}.")


    # downloader.download(bot=bot, message=call.message, userInput=receivedData, videoURL=checker.videoURL)
    # bot.send_message(call.message.chat.id, f"{videoURL} \n{receivedData} : Download Triggered!")
            
# message, videoURL, receivedData
    
download_thread = threading.Thread(target=myqueues.download_worker, args=(bot, myqueues.download_queue))
download_thread.daemon = True
download_thread.start()

print("TelegramYTDLBot is running..\n")
bot.infinity_polling()
````

## File: README.md
````markdown
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
#

## Disclaimer
This repository is intended for educational and personal use only. The use of this repository for any commercial or illegal purposes is strictly prohibited. The repository owner does not endorse or encourage the downloading or sharing of copyrighted material without permission. The repository owner is not responsible for any misuse of the software or any legal consequences that may arise from such misuse

- **APIs : [y2mate-api](https://github.com/Simatwa/y2mate-api/) , [pytelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/)**
- **Contact for issues : [@dev00111](https://t.me/dev00111)**
#
_Sorry for my bad english and my messy documentation. 😶_
````
