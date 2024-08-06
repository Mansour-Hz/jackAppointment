import requests
import pytz
from datetime import datetime
import time
import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext

# File to keep track of the last notification time
LAST_NOTIFICATION_FILE = 'last_notification_time.txt'
SAVED_PAGES_DIR = 'savedPages'

# Configuration for the Telegram bot
BOT_TOKEN = '7002542991:AAHAWKTKY1aJ_gCZS8sZ6PpUrGQO2Frtsxw'
CHAT_ID = '-4129556338'  # Updated chat ID

bot = Bot(token=BOT_TOKEN)

# Ensure savedPages directory exists
if not os.path.exists(SAVED_PAGES_DIR):
    os.makedirs(SAVED_PAGES_DIR)

def notify_user(message):
    url_button = InlineKeyboardButton(text="بریم تو سایت", url="https://appointment.bmeia.gv.at/?fromSpecificInfo=True")
    stop_button = InlineKeyboardButton(text="ساکت باش ربات", callback_data="stop_notifications")
    keyboard = [[url_button, stop_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, reply_markup=reply_markup)
        print("Notification sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

def save_html_page(html_content):
    tehran_tz = pytz.timezone('Asia/Tehran')
    current_time = datetime.now(tehran_tz)
    filename = current_time.strftime("%Y-%m-%d_%H-%M-%S.html")
    filepath = os.path.join(SAVED_PAGES_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Saved HTML page: {filename}")
    except Exception as e:
        print(f"Error saving HTML page: {str(e)}")

def check_appointments():
    url = "https://appointment.bmeia.gv.at/?fromSpecificInfo=True"
    payload = {
        "Language": "en",
        "Office": "TEHERAN",
        "CalendarId": "23134510",
        "PersonCount": "1",
        "Command": "Next"
    }
    error_message = '<p class="message-error">For your selection there are unfortunately no appointments available</p>'

    try:
        response = requests.post(url, data=payload)
        if error_message not in response.text:
            notify_user("سریع نوبت رو بگیر علی")
            save_html_page(response.text)
        # else:
        #     print("No appointments available.")
    except Exception as e:
        print(f"Error: {str(e)}")

def should_send_status_update():
    # Tehran timezone
    tehran_tz = pytz.timezone('Asia/Tehran')
    current_time = datetime.now(tehran_tz)
    current_hour = current_time.hour

    # Notify at 08:00, 16:00, or 00:00 Tehran time
    return current_hour in [0, 8, 16]

def get_last_notification_time():
    if os.path.exists(LAST_NOTIFICATION_FILE):
        with open(LAST_NOTIFICATION_FILE, 'r') as file:
            last_time_str = file.read().strip()
            return datetime.fromisoformat(last_time_str)
    return None

def update_last_notification_time():
    with open(LAST_NOTIFICATION_FILE, 'w') as file:
        file.write(datetime.now(pytz.timezone('Asia/Tehran')).isoformat())

def stop_notifications_for_one_minute(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="باشه داوش...")
    # Logic to stop notifications for 1 minute
    print("Stopping notifications for 1 minute.")
    time.sleep(60)
    print("Resuming notifications.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handler for stop notifications button
    dispatcher.add_handler(CallbackQueryHandler(stop_notifications_for_one_minute, pattern="stop_notifications"))

    updater.start_polling()

    while True:
        current_time = datetime.now(pytz.timezone('Asia/Tehran'))
        last_notification_time = get_last_notification_time()

        check_appointments()

        if should_send_status_update():
            if last_notification_time is None or (current_time - last_notification_time).total_seconds() >= 3600:
                notify_user("من هنوز دارم سایتو چک میکنم لاشی")
                update_last_notification_time()

        # Wait for one minute before running the check again
        time.sleep(300)

if __name__ == "__main__":
    main()
