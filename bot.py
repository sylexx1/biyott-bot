import os
import threading

from flask import Flask

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
TOKEN = os.environ.get("BOT_TOKEN", "")

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is not set. "
        "Set it in your Render dashboard's Environment settings."
    )

# ─────────────────────────────────────────────
# Flask app (keeps Render web service alive)
# ─────────────────────────────────────────────
web = Flask(__name__)


@web.route("/")
def home():
    return "Bot is Running!"


def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


# ─────────────────────────────────────────────
# Keyboards
# ─────────────────────────────────────────────
def main_menu():
    keyboard = [
        ["🪐 Account Manage", "🪐 Subset"],
        ["💰 Deposit", "💸 Withdraw"],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def cancel_menu():
    keyboard = [["❌ Cancel"]]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ─────────────────────────────────────────────
# Handlers
# ─────────────────────────────────────────────
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

Invite your friends to join.

━━━━━━━━━━━━━━

📎 Bot Link:
https://t.me/Biyott_bot?start=start""",
            reply_markup=cancel_menu()
        )

    elif text == "💰 Deposit":
        await update.message.reply_text(
            """💰 Deposit

🔥 Limited-Time Offer!

Deposit a minimum of $150 today to activate your account.

💳 Deposit Limits:
• Minimum Deposit: $150
• Maximum Deposit: $600

💵 USDT Address (ERC20):
0xce4c0883c580de3af6737267e1af938b459127f6

💎 ETH Address:
0xce4c0883c580de3af6737267e1af938b459127f6

━━━━━━━━━━━━━━

📌 After completing the deposit,
send TXID or screenshot for verification.""",
            reply_markup=cancel_menu()
        )

    elif text == "💸 Withdraw":
        await update.message.reply_text(
            """💸 Withdraw

❌ No Balance Available

Your current balance is $0.

Please deposit and accumulate balance before requesting withdrawal.""",
            reply_markup=cancel_menu()
        )

    elif text == "❌ Cancel":
        await update.message.reply_text(
            "Welcome! 👋\n\nPlease choose an option:",
            reply_markup=main_menu()
        )

    else:
        await update.message.reply_text(
            "Please choose one of the options from the menu below. 👇",
            reply_markup=main_menu()
        )


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    main()
