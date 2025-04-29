import telebot
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ضع هنا توكن البوت
TOKEN = "7876243780:AAF5Dxt5V4iIbSo2_-CheWX0WhzNNJtqyy4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا بك")

@bot.message_handler(commands=['editor'])
def open_editor(message):
    bot.reply_to(message, "افتح المحرر باستخدام الأمر:\n\n nano bot.py")

@bot.message_handler(commands=['run'])
def run_bot(message):
    bot.reply_to(message, "لتشغيل البوت، استخدم:\n\n python bot.py")

print("البوت يعمل...")
bot.polling()


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "🚀 مرحبا بيك في بوت مولد أكواد الشخصيات!\n\n"
        "ابعت اسم الشخصية عشان ابعتلك الكود جاهز (مثل: akita)"
    )

def generate_code(update: Update, context: CallbackContext) -> None:
    char_name = update.message.text.lower().strip()
    
    if not char_name.replace("_", "").isalnum():
        update.message.reply_text("⚠ اسم الشخصية مش صحيح (استخدم حروف وانجليزي فقط)")
        return
    
    code = {
        "version": 3,
        "data": json.dumps({
            "lastSaved": "2022-08-08T09:50:09.992174Z",
            "patchVersion": 2,
            "selected": {
                "character": char_name,
                "outfit": "default"
            },
            "lastPermanentSelectedCharacter": {
                "character": None,
                "outfit": None
            },
            "owned": {
                char_name: {
                    "value": {
                        "id": char_name,
                        "ownedOutfits": [
                            {"value": "default", "expirationType": 0},
                            {"value": "red", "expirationType": 0},
                            {"value": "premium", "expirationType": 0}
                        ],
                        "lastOutfit": "default"
                    },
                    "expirationType": 0
                }
            }
        }, ensure_ascii=False)
    }
    
    update.message.reply_text(f"🎮 كود {char_name} جاهز:\n\n"
                            f"```json\n{json.dumps(code, indent=2, ensure_ascii=False)}\n```",
                            parse_mode='Markdown')

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_code))
    
    print("البوت شغال.. انتظر الرسائل!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()