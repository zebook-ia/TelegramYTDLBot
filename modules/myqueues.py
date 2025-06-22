import logging
from queue import Queue
from modules.ytdownloader import download
# Import specific exceptions if ytdownloader or its dependencies raise them and you want to catch them explicitly
# For example: from pytube.exceptions import VideoUnavailable
# from requests.exceptions import RequestException
# import subprocess

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

download_queue = Queue()

def download_worker(bot, download_queue_instance): # Renamed download_queue to download_queue_instance to avoid conflict
    while True:
        message, video_url, selected_quality = download_queue_instance.get()
        item_description = f"Video URL: {video_url}, Quality: {selected_quality}, Chat ID: {message.chat.id}"
        logging.info(f"Processing download: {item_description}")

        try:
            # The 'download' function in ytdownloader handles its own specific error reporting to user for now.
            # We are primarily concerned with errors that stop the worker or are not caught by 'download'.
            download(bot=bot, message=message, userInput=selected_quality, videoURL=video_url)
            logging.info(f"Successfully processed: {item_description}")

        # Specific anticipated errors (examples, adapt based on actual errors from ytdownloader)
        # except VideoUnavailable as e:
        #     logging.error(f"Video unavailable for {item_description}: {e}")
        #     bot.send_message(message.chat.id, f"Sorry, the video at {video_url} is unavailable.")
        # except RequestException as e:
        #     logging.error(f"Network error during download for {item_description}: {e}")
        #     bot.send_message(message.chat.id, "A network error occurred. Please try again later.")
        # except subprocess.CalledProcessError as e:
        #     logging.error(f"FFmpeg compression error for {item_description}: {e}")
        #     bot.send_message(message.chat.id, "There was an error processing the video (compression stage).")
        # except FileNotFoundError as e:
        #     logging.error(f"File not found during processing for {item_description}: {e}")
        #     bot.send_message(message.chat.id, "An internal error occurred (file not found).")

        except Exception as e: # Catch-all for unexpected errors
            logging.exception(f"An unexpected error occurred while processing {item_description}: {e}")
            # Notify user about a generic error if not handled by the download function itself
            try:
                bot.send_message(message.chat.id, "An unexpected error occurred while processing your download. The developers have been notified.")
            except Exception as send_e:
                logging.error(f"Failed to send error message to user {message.chat.id}: {send_e}")

        finally:
            download_queue_instance.task_done()
            logging.info(f"Task done for: {item_description}")
            if download_queue_instance.empty():
                logging.info("All downloads have been completed. Queue is empty now.\n")


