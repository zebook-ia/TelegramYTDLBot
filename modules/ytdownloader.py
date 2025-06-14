import os
import subprocess
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
            continue

        file_path = os.path.join(mediaPath, vidFileName)
        file_size = os.path.getsize(file_path)
        max_size = 2 * 1024 * 1024 * 1024
        if file_size > max_size:
            bot.edit_message_text(
                chat_id=downloadMsg.chat.id,
                message_id=downloadMsg.message_id,
                text="<b>Arquivo grande, comprimindo...</b>",
            )
            compressed_name = f"compressed_{vidFileName}"
            compressed_path = os.path.join(mediaPath, compressed_name)
            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        file_path,
                        "-vf",
                        "scale='min(1280,iw)':-2",
                        "-c:v",
                        "libx264",
                        "-preset",
                        "fast",
                        "-crf",
                        "28",
                        "-c:a",
                        "copy",
                        "-fs",
                        str(max_size - 10 * 1024 * 1024),
                        compressed_path,
                    ],
                    check=True,
                )
            except Exception as e:
                bot.reply_to(message, f"Erro ao comprimir vídeo: {e}")
                os.remove(file_path)
                continue

            os.remove(file_path)
            file_path = compressed_path
            vidFileName = compressed_name

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
        
