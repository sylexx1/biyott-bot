from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7675521559:AAFJBWZRYn3BCthpymcCjOLB_aAvDoVu4ho"


def main_menu():
    keyboard = [
        ["🪐 Account Manage", "🪐 Subset"],
        ["💰 Deposit", "💸 Withdraw"]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def cancel_menu():
    keyboard = [
        ["❌ Cancel"]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! 👋\n\nPlease choose an option:",
        reply_markup=main_menu()
    )


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🪐 Account Manage":
        await update.message.reply_text(
            """💼 Account Management

💲 Balance: 150
👥 Referrals: 0

🔥 Claim Your Reward Today!
Exclusive rewards are waiting for active accounts.

👉 Tap Deposit below to start earning immediately! 📈""",
            reply_markup=cancel_menu()
        )

    elif text == "🪐 Subset":
        await update.message.reply_text(
            """🪐 Referral Program

Earn $25 for Every Qualified Referral!

Invite your friends to join and earn rewards.

🔗 Bot Link:
https://t.me/Biyott_bot?start=start""",
            reply_markup=cancel_menu()
        )

    elif text == "💰 Deposit":
        await update.message.reply_text(
            """💰 Deposit

🔥 Limited Time Offer!

Deposit a minimum of $150 today.

💳 Deposit Limits:
• Minimum: $150
• Maximum: $600

💵 USDT Address (ERC20):
YOUR_ADDRESS_HERE

💎 ETH Address:
YOUR_ADDRESS_HERE

📌 After completing the deposit, send TXID or screenshot for verification.""",
            reply_markup=cancel_menu()
        )

    elif text == "💸 Withdraw":
        await update.message.reply_text(
            """💸 Withdraw

❌ No Balance Available

Your current balance is $0.""",
            reply_markup=cancel_menu()
        )

    elif text == "❌ Cancel":
        await update.message.reply_text(
            "Main Menu 👇",
            reply_markup=main_menu()
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, messages))

print("Bot is running...")

app.run_polling()
