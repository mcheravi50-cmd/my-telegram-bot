from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

TOKEN = "8350375941:AAEucPHi0FwZRmQ0h1Ia-nlVbJop1H_IB6c"
ADMIN_ID = 569504594  # آیدی تلگرام خودت

CATEGORY, ITEM, QUANTITY, CONFIRM = range(4)

categories = {
    "☕ قهوه": [
        "روبوستا ۸۰ در ۲۰",
        "روبوستا ۷۰ در ۳۰",
        "دمی"
    ],

    "🍪 خوراکی": [
        "شیر پرچرب",
        "شیر کم‌چرب",
        "چای ایرانی",
        "چای خارجی",
        "بیسکوییت دایجستیو",
        "کیک",
        "بایکیت تلخ",
        "بایکیت فندقی",
        "بیسکوییت مادر",
        "کراکس شور",
        "کروسان",
        "قند",
        "شکر",
        "نبات",
        "چای کیسه‌ای"
    ],

    "🧼 شوینده و بهداشتی": [
        "شیشه پاک‌کن",
        "چندمنظوره",
        "دامستوس سرکج",
        "اسپری دامستوس",
        "اسپری گاز پاک‌کن",
        "وایتکس",
        "جرم‌گیر",
        "دستکش ظرف‌شویی",
        "دستکش لاتکس",
        "دستکش یکبارمصرف",
        "اسکاج گرد",
        "اسکاج مربعی",
        "دستمال سطوح",
        "دستمال شیشه",
        "کیسه زباله ۱۰۰×۱۲۰",
        "کیسه زباله ۱۲۰×۱۴۰",
        "کیسه زباله ۹۰×۱۱۰",
        "کیسه زباله زرد",
        "کیسه دسته‌دار ۵۰×۶۰",
        "مایع دستشویی",
        "مایع ظرفشویی",
        "طی حوله‌ای",
        "طی نخی",
        "دسته طی",
        "اسپری خوشبوکننده",
        "دستمال جعبه‌ای",
        "دستمال اقتصادی",
        "دستمال رولی",
        "دستمال مخزنی"
    ],

    "✏️ لوازم تحریر": [
        "خودکار آبی",
        "خودکار مشکی",
        "خودکار قرمز",
        "خودکار سبز",
        "ماژیک آبی",
        "ماژیک مشکی",
        "ماژیک قرمز",
        "ماژیک سبز",
        "تخته پاک‌کن",
        "چسب نواری",
        "مداد",
        "استیک نوت",
        "پاک‌کن",
        "تراش",
        "باطری قلم",
        "باطری نیم‌قلم"
    ],

    "🥤 یکبار مصرف": [
        "لیوان آب‌خوری",
        "لیوان کاغذی کوچک",
        "لیوان کاغذی بزرگ",
        "پیش‌دستی",
        "قاشق",
        "چنگال",
        "چاقو",
        "قاشق کوچک"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["choices"] = []
    keyboard = [[key] for key in categories.keys()]
    await update.message.reply_text(
        "دسته مورد نظر رو انتخاب کن 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CATEGORY

async def choose_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text

    if category == "🔙 برگشت":
        return await start(update, context)

    context.user_data["category"] = category
    items = categories.get(category, [])
    keyboard = [[i] for i in items] + [[KeyboardButton("🔙 برگشت")]]
    await update.message.reply_text(
        f"دسته «{category}» انتخاب شد. حالا آیتم مورد نظرت رو انتخاب کن 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return ITEM

async def ask_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update.message.text

    if item == "🔙 برگشت":
        keyboard = [[key] for key in categories.keys()]
        await update.message.reply_text(
            "دوباره دسته مورد نظر رو انتخاب کن 👇",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return CATEGORY

    context.user_data["item"] = item
    await update.message.reply_text(
        f"مقدار مورد نظرت برای «{item}» رو بنویس (مثلاً ۲ عدد یا ۱ کارتن):",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 برگشت")]], resize_keyboard=True)
    )
    return QUANTITY

async def save_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qty = update.message.text.strip()
    if qty == "🔙 برگشت":
        category = context.user_data.get("category")
        items = categories.get(category, [])
        keyboard = [[i] for i in items] + [[KeyboardButton("🔙 برگشت")]]
        await update.message.reply_text(
            "برگشتی! حالا دوباره آیتم مورد نظرت رو انتخاب کن 👇",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return ITEM

    cat = context.user_data.get("category")
    item = context.user_data.get("item")
    context.user_data["choices"].append(f"{cat} → {item} ({qty})")

    keyboard = [
        [KeyboardButton("➕ افزودن کالای جدید")],
        [KeyboardButton("✅ ثبت نهایی"), KeyboardButton("❌ انصراف")]
    ]
    await update.message.reply_text(
        f"✅ مورد اضافه شد: {cat} → {item} ({qty})\n\nمیخوای ادامه بدی یا ثبت نهایی؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "➕ افزودن کالای جدید":
        keyboard = [[key] for key in categories.keys()]
        await update.message.reply_text(
            "دسته مورد نظر رو انتخاب کن 👇",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return CATEGORY

    elif text == "✅ ثبت نهایی":
        user = update.message.from_user.username or update.message.from_user.first_name
        summary = "\n".join(context.user_data["choices"])
        message = f"📦 درخواست جدید از {user}:\n\n{summary}"

        await update.message.reply_text(f"✅ درخواستت ثبت شد:\n\n{summary}")
        await context.bot.send_message(chat_id=ADMIN_ID, text=message)

    else:
        await update.message.reply_text("❌ درخواست لغو شد.")

    keyboard = [[key] for key in categories.keys()]
    await update.message.reply_text(
        "برای شروع دوباره یکی از دسته‌ها رو انتخاب کن 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    context.user_data["choices"] = []
    return CATEGORY

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات تموم شد. برای شروع دوباره /start رو بزن.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_item)],
            ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_quantity)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_choice)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("done", done)]
    )

    app.add_handler(conv_handler)
    print("✅ ربات فعاله...")
    app.run_polling()

if __name__ == "__main__":
    main()
