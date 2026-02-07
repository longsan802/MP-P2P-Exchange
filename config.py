"""
USDT Exchange Bot Configuration
===============================
Edit this file to configure your bot settings.
"""

# ================= BOT TOKEN =================
# Get from @BotFather on Telegram
BOT_TOKEN = "8368520052:AAHpEb3gdIz8kLdlMIvlb9xIeezT3gdPpZU"

# ================= ADMIN ID =================
# Your Telegram user ID (find via @userinfobot)
ADMIN_ID = 7581084477

# ================= PLATFORM USDT WALLETS =================
# Platform wallets for receiving USDT
PLATFORM_USDT_WALLET = {
    "TRC20": "TPtKtKZH8oQiYkbwqgYxmeEBn5ZTTSKW8A",
    "BEP20": "0x3ceE1c1e10E775Ef36C007D2912B512CDAF61721",
    "ERC20": "0x3ceE1c1e10E775Ef36C007D2912B512CDAF61721"
}

# ================= KHQR PAYMENT =================
# KHQR code image - using local file
KHQR_IMAGE_PATH = "photo_2026-01-26_15-43-13.jpg"  # Your KHQR image file
KHQR_IMAGE_URL = None  # Disable URL, use local file

# KHQR Dynamic Payment Data
# These values are used for generating dynamic KHQR payments
KHQR_MERCHANT_ID = "222222"
KHQR_MERCHANT_NAME = "USDT Cambodia Exchange"
KHQR_ACQUIRING_BANK = "ABA"

# Dynamic KHQR payment data (Base64 encoded)
# This is the actual KHQR data string for payments
KHQR_PAYMENT_DATA = "qWY5B2SAUfIhLblxzOtfu5ckLzMHjaSki6Ru0bsOyNK+ylPBgZ0sHH6BeGUscKoEqcd2TgBIJ12h1yDmCnkCc/2yCqsQ4Udl70lCZRXiryWzaFe8EC+nZbQ6mlYR4KDy+oZR4whbKEcGyueyzaDrUsYlDxSEisshLfK8rRU/Xi+183WMs7JtMaFnfHKhjzlhoxABiaW96VA8kvDSYgWURzh5fkuS5+ht1m1gRPSF5TQ="
KHQR_KEY = "khqr"

# ================= GROUP & SUPPORT =================
# Your support username (without @)
SUPPORT_USERNAME = "m11122212"

# Your Telegram group link
GROUP_LINK = "https://t.me/iknowkhstore"

# ================= RULES =================
# English rules (Markdown safe)
RULES_TEXT = """
📜 *USDT Exchange Info*

USDT (Tether) គឺជាគ្រីបត្រូវដែលមានតម្លៃស្ថិតនៅជិត $1 ។ នៅកម្ពុជា អ្នកអាចទិញ/លក់ USDT តាមរយៈ:

🏠 *Online Platforms* (Coindisco, Binance P2P)
 ដោយប្រើប្រាក់កាត ធនាគារ ឬ e-wallet 📱

👥 *P2P Trading* ដោយប្រើប្រាក់ផ្ទាល់

🏪 *Physical Shops* នៅភ្នំពេញ

⚠️ *Safety & Risks*:
• មានហានិភ័យ scammers និងរបៀបធនាគារ
• សូមប្រុងប្រយ័ត្ន និងពិនិត្យលក្ខខណ្ឌ

💬 *Support*: @{SUPPORT_USERNAME}
"""


# ================= BUY USDT INFO (KHMER) =================
# Use this for /buy_usdt_info command
BUY_USDT_INFO = """
📌 របៀបទិញ USDT (Buy USDT)

1️⃣ ផ្ទេរប្រាក់
ផ្ទេរប្រាក់ទៅតាមចំនួន USDT ដែលចង់ទិញ បូកសេវា

ឧទាហរណ៍៖
• ទិញ 49 USDT
• Fee 1 USDT
👉 ផ្ញើ ABA = 50$

2️⃣ ផ្ញើវិក័យប័ត្រ (Transaction Slip)
សូមផ្ញើវិក័យប័ត្រផ្ទេរប្រាក់ឲ្យបានច្បាស់

3️⃣ ផ្ញើ Wallet Address
ទម្លាក់ Wallet Address របស់ Exchange ឬ Wallet App ដែលអ្នកប្រើប្រាស់

4️⃣ អត្រាប្រាក់រៀល (KHR)
💵 1 USD = 4,050₭
💵 10 USD = 40,500₭

⚠️ សេចក្តីជូនដំណឹងសំខាន់

⛔️ សូមពិនិត្យឈ្មោះគណនីអោយបានត្រឹមត្រូវ
(SHP2P BY L.LAY)

🚫 ក្នុងករណីផ្ញើខុស UID / ABA / Wallet Address
➡️ SH P2P មិនទទួលខុសត្រូវ ទេ

⏰ ម៉ោងសេវាកម្ម

🟢 អាចទិញ-លក់បាន
08:00 ព្រឹក – 12:00 យប់

🍽️ ពេលសម្រាក
01:00 PM – 01:59 PM (ផ្នែកដាក់ប្រាក់សម្រាកញ៉ាំបាយ)

🙏 សូមអរគុណ

សូមអរគុណចំពោះការជឿទុកចិត្ត និងប្រើប្រាស់សេវាកម្មរបស់យើង 💚
បើមានសំណួរ សូមចុច Support ក្នុង Bot 📞
"""

# ================= SELL USDT INFO (KHMER) =================
SELL_USDT_INFO = """
📌 របៀបលក់ USDT (Sell USDT)

1️⃣ ជ្រើសរើស Network
• TRC20 (Tron) - លឿន & ថោក)
• BEP20 (BSC) - លឿន)
• ERC20 (Ethereum) - ថ្លៃ)

2️⃣ បញ្ចូលចំនួន USDT
• ចំនួនតិចបំផុត: 10 USDT

3️⃣ ផ្ញើ USDT ទៅ Platform
• ចម្លង Address ខាងក្រោម
• ប្រាក់នឹងបញ្ចូល KHR តាម ABA

4️⃣ ផ្ញើ Transaction Hash
• ទុកជាភ័ស្តុតាង

⚠️ សេចក្តីជូនដំណឹង
• ពិនិត្យ Network ឲ្យបានត្រឹមត្រូវ
• ផ្ញើ USDT ប្រាក់នឹងបញ្ចូល 1-5 នាទី

⏰ ម៉ោងសេវាកម្ម
🟢 08:00 ព្រឹក – 12:00 យប់
🍽️ 01:00 PM – 01:59 PM សម្រាក

🙏 សូមអរគុណ
"""

# ================= EXCHANGE RATE =================
EXCHANGE_RATE = {
    "USD_TO_KHR": 4050,  # 1 USD = 4,050 KHR
    "MIN_AMOUNT": 10,     # Minimum USDT transaction
    "BUY_FEE_PERCENT": 2,  # 2% fee for buying
    "SELL_FEE_PERCENT": 1  # 1% fee for selling
}


# ================= WELCOME & THANK YOU MESSAGES =================
WELCOME_MESSAGE = """
👋 *Welcome to USDT Cambodia Exchange*

━━━━━━━━━━━━━━━━━━━━
✅ Fast & Secure Manual Trading
✅ Best Exchange Rates
✅ 24/7 Customer Support
━━━━━━━━━━━━━━━━━━━━

Choose an option below to get started 👇
"""

THANK_YOU_MESSAGE = """
🙏 *Thank You for Trading With Us!*

━━━━━━━━━━━━━━━━━━━━
✅ Your transaction has been processed
✅ Funds will be credited shortly
✅ We appreciate your trust 💚
━━━━━━━━━━━━━━━━━━━━

💡 *Tips*:
• Save your transaction ID
• Contact support if any issues
• Trade again anytime!

Have a wonderful day! 🌟
"""

ORDER_APPROVED_MESSAGE = """
🎉 *Order Approved!*

━━━━━━━━━━━━━━━━━━━━
✅ Transaction completed successfully
✅ {action} {amount} USDT via {network}
✅ Reference: #{reference}
━━━━━━━━━━━━━━━━━━━━

{thank_you_message}

Need help? Contact @YourSupport
"""

ORDER_REJECTED_MESSAGE = """
❌ *Order Rejected*

━━━━━━━━━━━━━━━━━━━━
Reason: {reason}
━━━━━━━━━━━━━━━━━━━━

📞 Please contact @YourSupport for clarification or assistance.

💡 You may try again with correct information.
"""

# ================= TIMEOUT SETTINGS =================
# Payment timeout in seconds (30 minutes)
PAYMENT_TIMEOUT_SECONDS = 1800

# ================= NETWORKS =================
NETWORKS = {
    "TRC20": {
        "name": "TRC20 (Tron)",
        "fee": "Fast & Low Fee",
        "confirmations": 1
    },
    "BEP20": {
        "name": "BEP20 (BSC)",
        "fee": "Medium Fee",
        "confirmations": 1
    },
    "ERC20": {
        "name": "ERC20 (Ethereum)",
        "fee": "Higher Fee",
        "confirmations": 1
    }
}

# ================= SCHEDULED RATE BROADCAST =================
# Channel/Group ID to send exchange rates (use negative ID for supergroups)
RATE_CHANNEL_ID = -1003785665811  # iknowkhstore group

# Schedule: "30min", "1hour", "1day"
RATE_BROADCAST_INTERVAL = "1hour"  # Send rates every hour

# Enable/disable scheduled broadcast
RATE_BROADCAST_ENABLED = True
