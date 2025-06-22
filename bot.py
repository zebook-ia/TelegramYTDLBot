import os
import telebot
import threading
import time # For state cleanup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from modules import myqueues
from modules.checker import extract_youtube_links, get_video_qualities # Refactored imports

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_API_KEY")

# Configure custom API server if provided
custom_api_url = os.getenv("BOT_API_URL")
if custom_api_url:
    telebot.apihelper.API_URL = f"{custom_api_url.rstrip('/')}/bot{{0}}/{{1}}"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# In-memory store for video quality options associated with a message
# Key: chat_id:message_id (of the bot's message asking for quality)
# Value: {'qualities': list_of_qualities, 'timestamp': time.time()}
# A timestamp is added for potential cleanup of old entries
quality_options_store = {}
MAX_STATE_AGE_SECONDS = 3600 # 1 hour to keep state

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

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    yt_links = extract_youtube_links(message.text)

    if not yt_links:
        # Only reply if the message was likely intended as a command or link
        if message.text.startswith('/') or 'http' in message.text:
             bot.reply_to(message, "No YouTube links found in your message.")
        return

    video_url = yt_links[0] # Process the first link found
    
    # Inform user that we are fetching qualities
    quality_checker_msg = bot.reply_to(message, "Looking for Available Qualities..🔎")

    qualities = get_video_qualities(video_url)

    if not qualities:
        bot.edit_message_text("No video qualities found or an error occurred.", chat_id=quality_checker_msg.chat.id, message_id=quality_checker_msg.message_id)
        return

    markup = InlineKeyboardMarkup()
    # Store qualities with a unique key related to the message where options are presented
    # This key will be part of the callback_data to retrieve context
    options_key_base = f"{quality_checker_msg.chat.id}:{quality_checker_msg.message_id}"
    
    temp_qualities_for_key = []

    for quality_info in qualities:
        # callback_data format: "quality_key_base#quality_value#video_url"
        # No need to store dlink in callback, it's for the downloader
        callback_data = f"{options_key_base}#{quality_info['q']}#{video_url}"
        button_text = f"{quality_info['q']} ({quality_info['size']})"
        markup.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
        temp_qualities_for_key.append(quality_info) # Store full info temporarily

    # Store the fetched qualities for this specific interaction
    quality_options_store[options_key_base] = {'qualities': temp_qualities_for_key, 'timestamp': time.time()}

    bot.edit_message_text("Choose a stream:", chat_id=quality_checker_msg.chat.id, message_id=quality_checker_msg.message_id, reply_markup=markup)

# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        options_key_base, selected_quality_value, video_url = call.data.split("#", 2)
    except ValueError:
        bot.answer_callback_query(call.id, "Error: Invalid callback data.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id) # Clean up buttons
        return

    # Retrieve the stored qualities for this interaction (optional, if needed beyond URL and quality value)
    # stored_interaction_data = quality_options_store.get(options_key_base)
    # if not stored_interaction_data:
    #     bot.answer_callback_query(call.id, "Error: Options expired or invalid. Please try sending the link again.")
    #     bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    #     return

    bot.answer_callback_query(call.id, f"Selected {selected_quality_value} to download.")
    # Delete the message with quality options
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    # Clean up the stored state for this interaction
    if options_key_base in quality_options_store:
        del quality_options_store[options_key_base]

    myqueues.download_queue.put((call.message, video_url, selected_quality_value)) # Pass original message context
    queue_position = myqueues.download_queue.qsize()
    
    if queue_position == 1:
        bot.send_message(call.message.chat.id, "Download has been added to the queue.")
    else:
        bot.send_message(call.message.chat.id, f"Download has been added to the queue at #{queue_position}.")

# --- State Cleanup (Optional but good practice) ---
def cleanup_old_states():
    while True:
        now = time.time()
        keys_to_delete = [key for key, data in quality_options_store.items() if now - data['timestamp'] > MAX_STATE_AGE_SECONDS]
        for key in keys_to_delete:
            del quality_options_store[key]
            print(f"Cleaned up expired state for key: {key}")
        time.sleep(600) # Check every 10 minutes

# --- Main Bot Logic ---
if __name__ == "__main__":
    print("TelegramYTDLBot is running..\n")
    
    download_thread = threading.Thread(target=myqueues.download_worker, args=(bot, myqueues.download_queue))
    download_thread.daemon = True
    download_thread.start()

    # Start cleanup thread
    # cleanup_thread = threading.Thread(target=cleanup_old_states)
    # cleanup_thread.daemon = True
    # cleanup_thread.start() # Disabled for now, can be enabled if state grows too large

    bot.infinity_polling()
