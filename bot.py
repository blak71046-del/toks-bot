from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8987230310:AAE2YnnvHCAbMiFQkRWuIhSzB2PeGuoUB0k"
CHANNEL_USERNAME = "@sssvbvc"
OWNER_USERNAME = "@besos_e"

WELCOME_MESSAGE = """📌 ⁞ مرحباً بكم في البوت التعليمي الخاص بتوكس

يرجى الاشتراك في قناتنا أولاً للمتابعة 👇"""

SERVICES_MESSAGE = "🛠️ اختر الخدمة التي تريدها:"

SERVICES_BUTTONS = [
    [InlineKeyboardButton("📦 الخدمة الأولى", callback_data="service_1"),
     InlineKeyboardButton("📦 الخدمة الثانية", callback_data="service_2")],
    [InlineKeyboardButton("📦 الخدمة الثالثة", callback_data="service_3"),
     InlineKeyboardButton("📦 الخدمة الرابعة", callback_data="service_4")],
    [InlineKeyboardButton("📦 الخدمة الخامسة", callback_data="service_5"),
     InlineKeyboardButton("📦 الخدمة السادسة", callback_data="service_6")],
]

async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subscribed = await is_subscribed(user_id, context)
    if not subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
            [InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data="check_sub")]
        ]
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(SERVICES_MESSAGE, reply_markup=InlineKeyboardMarkup(SERVICES_BUTTONS))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "check_sub":
        subscribed = await is_subscribed(user_id, context)
        if subscribed:
            await query.edit_message_text(SERVICES_MESSAGE, reply_markup=InlineKeyboardMarkup(SERVICES_BUTTONS))
        else:
            keyboard = [
                [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
                [InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data="check_sub")]
            ]
            await query.edit_message_text("❌ لم تشترك بعد!\nاشترك ثم اضغط تحققت.", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith("service_"):
        service_num = query.data.split("_")[1]
        names = {"1":"الخدمة الأولى","2":"الخدمة الثانية","3":"الخدمة الثالثة","4":"الخدمة الرابعة","5":"الخدمة الخامسة","6":"الخدمة السادسة"}
        keyboard = [
            [InlineKeyboardButton("💬 تواصل مع توكس", url="https://t.me/besos_e")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
        ]
        await query.edit_message_text(f"✅ اخترت: {names[service_num]}\n\nاضغط للتواصل مع توكس 👇", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "back":
        await query.edit_message_text(SERVICES_MESSAGE, reply_markup=InlineKeyboardMarkup(SERVICES_BUTTONS))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
print("✅ البوت يعمل!")
app.run_polling()
