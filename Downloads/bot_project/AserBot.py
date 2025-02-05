
# سورس بوت "أسر"
# بوت حماية وتشغيل أغاني مخصص مع نظام أذونات.

from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess

# إعدادات البوت
API_ID = "your_api_id"  # ضع API_ID الخاص بك
API_HASH = "your_api_hash"  # ضع API_HASH الخاص بك
BOT_TOKEN = "your_bot_token"  # ضع توكن البوت الخاص بك
OWNER_USERNAME = "@FA_5_R"  # حساب الأونر
AUTHORIZED_USERS = [OWNER_USERNAME]  # قائمة المستخدمين المسموح لهم باستخدام السورس

# إنشاء تطبيق البوت
app = Client("AserBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# التحقق من الأذونات
@app.on_message(filters.private & ~filters.command("start"))
def check_authorization(client, message: Message):
    if message.from_user.username not in AUTHORIZED_USERS:
        message.reply("❌ ليس لديك الإذن لاستخدام هذا البوت.")
        return

# رسالة الترحيب عند بدء البوت
@app.on_message(filters.command("start") & filters.private)
def start_command(client, message: Message):
    message.reply(f"✨ مرحباً بك في بوت أسر!\n\nهذا البوت يدير الجروبات ويشغل الأغاني. فقط المصرح لهم يمكنهم استخدامه.\n\n👤 أونر البوت: {OWNER_USERNAME}")

# فلترة الروابط داخل الجروبات
@app.on_message(filters.text & filters.group)
def filter_links(client, message):
    if "http" in message.text:
        message.delete()
        message.reply("❌ الروابط ممنوعة في هذا الجروب!")

# تشغيل الأغاني
@app.on_message(filters.command("play") & filters.private)
def play_song(client, message: Message):
    if len(message.command) < 2:
        message.reply("❌ يرجى إدخال رابط الأغنية أو اسمها.")
        return

    url = message.text.split(" ", 1)[1]
    message.reply("⏳ جاري تحميل وتشغيل الأغنية...")

    try:
        # تحميل الصوت باستخدام youtube-dl
        subprocess.run(["youtube-dl", "-x", "--audio-format", "mp3", "-o", "song.%(ext)s", url])

        # إرسال الملف الصوتي
        audio_file = "song.mp3"
        if os.path.exists(audio_file):
            message.reply_audio(audio=audio_file, caption="🎶 استمتع بالموسيقى!")
            os.remove(audio_file)
        else:
            message.reply("❌ لم يتم العثور على ملف الصوت.")
    except Exception as e:
        message.reply(f"❌ حدث خطأ أثناء التشغيل: {e}")

# تشغيل البوت
if __name__ == "__main__":
    print("✅ Bot is running...")
    app.run()
