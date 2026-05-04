from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# === TOKEN ===
TOKEN = "8666909072:AAEtxO8JGXZvMUZCQnRJ19tIt2RPXb7LbF0"

# Holatlar
A, B, C = range(3)

# Foydalanuvchi ma'lumotlarini saqlash
user_data = {}


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men uchburchak yuzini hisoblayman 📐\n"
        "/hisob — Hisoblashni boshlash\n"
        "/help  — Yordam"
    )


# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Qanday ishlaydi:\n"
        "1. /hisob buyrug'ini yuboring\n"
        "2. Uchburchakning 3 tomonini kiriting\n"
        "3. Bot Geron formulasi bilan yuzni hisoblaydi!\n\n"
        "📐 Formula: S = √(p(p-a)(p-b)(p-c))\n"
        "Bu yerda p = (a+b+c)/2"
    )


# /hisob — 1-tomon
async def hisob_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📏 1-tomonni kiriting (a):")
    return A


# 2-tomon
async def get_a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        a = float(update.message.text)
        if a <= 0:
            await update.message.reply_text("❌ Tomon musbat son bo'lishi kerak! Qayta kiriting:")
            return A
        context.user_data["a"] = a
        await update.message.reply_text("📏 2-tomonni kiriting (b):")
        return B
    except ValueError:
        await update.message.reply_text("❌ Iltimos, son kiriting! Masalan: 5 yoki 3.5")
        return A


# 3-tomon
async def get_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        b = float(update.message.text)
        if b <= 0:
            await update.message.reply_text("❌ Tomon musbat son bo'lishi kerak! Qayta kiriting:")
            return B
        context.user_data["b"] = b
        await update.message.reply_text("📏 3-tomonni kiriting (c):")
        return C
    except ValueError:
        await update.message.reply_text("❌ Iltimos, son kiriting! Masalan: 5 yoki 3.5")
        return B


# Natija
async def get_c(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        c = float(update.message.text)
        if c <= 0:
            await update.message.reply_text("❌ Tomon musbat son bo'lishi kerak! Qayta kiriting:")
            return C

        a = context.user_data["a"]
        b = context.user_data["b"]

        # Uchburchak sharti tekshirish
        if a + b <= c or a + c <= b or b + c <= a:
            await update.message.reply_text(
                "❌ Bu tomonlar bilan uchburchak hosil bo'lmaydi!\n"
                "Qaytadan boshlash uchun /hisob yuboring."
            )
            return ConversationHandler.END

        # Geron formulasi
        p = (a + b + c) / 2
        yuza = (p * (p - a) * (p - b) * (p - c)) ** 0.5

        await update.message.reply_text(
            f"✅ Natija:\n\n"
            f"📐 Tomonlar: a={a}, b={b}, c={c}\n"
            f"📊 Perimetr: {a + b + c}\n"
            f"🔢 Yarim perimetr (p): {p}\n"
            f"📏 Yuza: {yuza:.2f} kv.birlik\n\n"
            f"Yana hisoblash uchun /hisob yuboring!"
        )
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("❌ Iltimos, son kiriting! Masalan: 5 yoki 3.5")
        return C


# /bekor
async def cancel(update: Update):
    await update.message.reply_text("❌ Bekor qilindi. /hisob — qayta boshlash.")
    return ConversationHandler.END


# === MAIN ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("hisob", hisob_start)],
        states={
            A: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_a)],
            B: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_b)],
            C: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_c)],
        },
        fallbacks=[CommandHandler("bekor", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)

    print("Bot ishga tushdi ✅")
    app.run_polling()