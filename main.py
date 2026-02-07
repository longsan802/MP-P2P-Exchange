"""USDT Cambodia Exchange Bot - Full Updated Version"""
import nest_asyncio
nest_asyncio.apply()

import asyncio
import logging
import os
import re
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ChatMemberUpdated
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters, ChatMemberHandler

import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

LANGUAGES = {
    "en": {"name": "🇺🇸 English", "code": "en"},
    "km": {"name": "🇰🇭 ភាសាខ្មែរ", "code": "km"},
    "zh": {"name": "🇨🇳 中文", "code": "zh"}
}

MESSAGES = {
    "en": {
        "welcome": "👋 *Welcome to USDT Cambodia Exchange* 🏦\n\nFast & Secure Trading | Best Rates | 24/7 Support\n\nChoose an option below 👇",
        "buy_usdt": "💵 *Buy USDT* 💵\n\n*Fee Schedule:*\n$10-$49 → $1.00\n$50-$99 → $1.50\n$100-$199 → $2.50\n$200-$399 → $4.00\n$400-$699 → $6.00\n$700-$1,199 → $8.00\n$1,200-$2,499 → $11.00\n$2,500-$4,999 → $17.00\n$5,000-$7,499 → $23.00\n$7,500-$10,000 → $26.00\n\n*Payment:* ABA, ACLEDA KHQR\n\n*Select Network:*",
        "sell_usdt": "💰 *Sell USDT* 💰\n\n*Min:* {min_amount} USDT\n*Fee:* {sell_fee}%\n\n*Networks:*\n🔷 TRC20 (Fast, Low Fee)\n🔶 BEP20 (Fast)\n💎 ERC20 (Higher Fee)\n\n*Select Network:*",
        "support": "📞 *Support Center* 📞\n\nWe are here to help you 24/7! 💚\n\n*How We Can Help:*\n💬 General questions\n🛠️ Technical support\n💱 Buy/Sell USDT guidance\n📩 Forward to admin\n\n*Contact us directly:*",
        "groups": "👥 *USDT Trading Groups* 👥\n\n*Why Join P2P Groups?*\n✅ Direct P2P trading\n✅ Better rates\n✅ Community support\n✅ Real-time updates\n\n*Join safely:* ⚠️ Beware of scammers",
        "rules": "📜 *Exchange Rules* 📜\n\n1️⃣ *Payment Methods* - Only ABA/KHQR, Bank Transfer\n2️⃣ *No Off-Platform Deals* - Never transfer outside\n3️⃣ *Confirm First* - Verify before releasing USDT\n4️⃣ *Timely Confirmation* - Upload proof promptly\n5️⃣ *Cancellation* - Frequent cancellations = penalties\n6️⃣ *Third-Party* - No using others' accounts\n7️⃣ *Disputes* - Open through system only\n8️⃣ *Safety* - Suspicious activity = suspension\n9️⃣ *Rates* - May vary by timing\n🔟 *Risk* - P2P involves risk",
        "rates": "📊 *Exchange Rates* 📊\n\n💵 *Base Rate:* 1 USD = {usd_to_khr:,} KHR\n\n💰 *Fees:*\n• Buy: {buy_fee}%\n• Sell: {sell_fee}%\n\n📦 *Min:* {min_amount} USDT\n\n*Note:* Rates may vary.",
        "enter_amount_buy": "💰 *Enter USDT amount to BUY:*\n\nMin: {min_amount} USDT",
        "enter_amount_sell": "💰 *\n\nMin: {min_amount} USDT",
        "enter_payment_detail": "🏦 *Enter your payment details* 🏦\n\nPlease enter your ABA account number or KHQR information where you want to receive KHR payment:\n\n💡 Example: ABA 123456789 or KHQR",
        "payment_detail_received": "✅ *Payment Details Received!*\n\n📋 We'll send payment to:\n{payment_detail}\n\nNow please send USDT to the platform wallet.",
        "enter_wallet": "🏦 *Enter your USDT wallet address:*\n\nWhere you receive USDT (TRC20/BEP20/ERC20)",
        "upload_invoice": "📷 *Upload Invoice*\n\nSend payment screenshot or invoice photo.\n\n💡 Max: 10MB | 📁 JPG, PNG",
        "invoice_uploaded": "✅ *Invoice Uploaded!*\n\n📋 *Order #{order_id}*\n🔹 Amount: {amount} USDT\n🔹 Status: ⏳ Awaiting Verification\n\n💚 Thank you! Team will verify shortly.",
        "order_timeout": "⏰ *Order #{order_id} Expired* ⏰\n\n⚠️ Payment timeout ({timeout} min).\n\n📞 New order: /start",
        "order_cancelled": "❌ *Order Cancelled*\n\nNew order: /start",
        "unknown_command": "❓ *Unknown Command*\n\nUse menu buttons or /start",
        "select_language": "🌐 *Select Language* 🌐\n\nChoose your language:",
        "no_history": "📭 *No Transaction History*\n\nYou haven't made any transactions yet.\n\nStart trading with /start",
        "group_welcome": "👋 *Welcome to USDT Cambodia Exchange Group* 🏦\n\n🎯 *What we offer:*\n✅ Best USDT rates in Cambodia\n✅ Fast & secure transactions\n✅ 24/7 customer support\n✅ Multiple payment methods\n\n💬 *Need help?* Click the button below to start chatting with our bot!",
        "group_welcome_km": "👋 *សូមស្វាគមន៍មកកាន់ក្រុម USDT Cambodia* 🏦\n\n🎯 *អ្វីដែលយើងផ្តល់:*\n✅ អត្រា USDT ល្អបំផុត\n✅ លឿន & មានសុវត្ថិ\n✅ គាំទ្រ 24/7\n✅ វិធីទូទាត់ច្រើន\n\n💬 *ត្រូវការជំនួយ?* ចុចប៊ុតខាងក្រោម!",
        "group_welcome_zh": "👋 *欢迎加入 USDT 柬埔寨交易所群* 🏦\n\n🎯 *我们提供:*\n✅ 柬埔寨最优 USDT 汇率\n✅ 快速安全交易\n✅ 24/7 客服支持\n✅ 多种支付方式\n\n💬 *需要帮助?* 点击下方按钮开始与我们的机器人交流！"
    },
    "km": {
        "welcome": "👋 *សូមស្វាគមន៍មកកាន់ USDT Cambodia Exchange* 🏦\n\n✅ ជេរភ្នាក់ងារលឿន & មានសុវត្ថិភាព\n✅ អត្រាល្អ\n✅ គាំទ្រ 24/7\n\n👇 ជ្រើសរើស:",
        "buy_usdt": "💵 *ទិញ USDT* 💵\n\n📋 *តារាងសេវាកម្ម USDT*\n\n$10 – $49 → សេវា $1.00\n$50 – $99 → សេវា $1.50\n$100 – $199 → សេវា $2.50\n$200 – $399 → សេវា $4.00\n$400 – $699 → សេវា $6.00\n$700 – $1,199 → សេវា $8.00\n$1,200 – $2,499 → សេវា $11.00\n$2,500 – $4,999 → សេវា $17.00\n$5,000 – $7,499 → សេវា $23.00\n$7,500 – $10,000 → សេវា $26.00\n\n💳 *គាំទ្រការទូទាត់:* ABA, ACLEDA KHQR និង Wallet Crypto\n\n🔗 *ជ្រើសរើស Network:*",
        "sell_usdt": "💰 *លក់ USDT* 💰\n\n*Min:* {min_amount} USDT\n*Fee:* {sell_fee}%\n\n*Networks:*\n🔷 TRC20 (លឿន, ថោក)\n🔶 BEP20 (លឿន)\n💎 ERC20 (ថ្លៃ)\n\n*Network:*",
        "support": "📞 *មជ្ឈមណ្ឌលគាំទ្រ* 📞\n\n24/7! 💚\n\n*ជួយ:*\n💬 សំណួរ\n🛠️ បច្ចេកទេស\n💱 ណែនាំ\n📩 ទៅអ្នកគ្រប់គ្រង\n\n*ទំនាក់:*",
        "groups": "👥 *ក្រុម USDT* 👥\n\n*ហេតុអ្វី P2P?*\n✅ ជេរផ្ទាល់\n✅ អត្រាល្អ\n✅ គាំទ្រ\n✅ ព័ត៌មាន\n\n*សុវត្ថិ:* ⚠️ ប្រយ័ត្ន scammers",
        "rules": "📜 *ច្បាប់* 📜\n\n1️⃣ *ទូទាត់* - ABA/KHQR, ធនាគារ\n2️⃣ *កុំផ្ទេរ* - កុំ\n3️⃣ *ផ្ទៀង* - មុនដោះ USDT\n4️⃣ *ទាន់* - ផ្ញើភ័ស្តុតាង\n5️⃣ *លុប* - ញឹក = ពិន័យ\n6️⃣ *ភាគី* - កុំ\n7️⃣ *វិវាទ* - ក្នុងប្រព័ន្ធ\n8️⃣ *សុវត្ថិ* - ស= ផ្អាក\n9️⃣ *អត្រា* - ប្រែ\n🔟 *ហានិ* - P2P មាន",
        "rates": "📊 *អត្រា USDT* 📊\n\n💵 *អត្រាប្តូរ:* 1 USD = {usd_to_khr:,} KHR\n\n📋 *តារាងសេវាកម្ម USDT*\n\n$10 – $49 → សេវា $1.00\n$50 – $99 → សេវា $1.50\n$100 – $199 → សេវា $2.50\n$200 – $399 → សេវា $4.00\n$400 – $699 → សេវា $6.00\n$700 – $1,199 → សេវា $8.00\n$1,200 – $2,499 → សេវា $11.00\n$2,500 – $4,999 → សេវា $17.00\n$5,000 – $7,499 → សេវា $23.00\n$7,500 – $10,000 → សេវា $26.00\n\n💳 *គាំទ្រការទូទាត់:* ABA, ACLEDA KHQR និង Wallet Crypto",
        "enter_amount_buy": "💰 *បញ្ចូល USDT ទិញ:*\n\nMin: {min_amount} USDT",
        "enter_amount_sell": "💰 *បញ្ចូល USDT លក់:*\n\nMin: {min_amount} USDT",
        "enter_wallet": "🏦 *អាស័យ Wallet USDT:*\n\n(TRC20/BEP20/ERC20)",
        "upload_invoice": "📷 *ផ្ញើរវិក្កយ* 📷\n\n💡 10MB | 📁 JPG, PNG",
        "invoice_uploaded": "✅ *វិក្កយបាន!* ✅\n\n📋 *Order #{order_id}*\n🔹 Amount: {amount} USDT\n🔹 Status: ⏳ រងការត្រួត\n\n💚 អរគុណ!",
        "order_timeout": "⏰ *Order #{order_id} ផុត* ⏰\n\n⚠️ ពេល ({timeout} min) ផុត\n\n📞 ថ្មី: /start",
        "order_cancelled": "❌ *បានលុ�*\n\nNew: /start",
        "unknown_command": "❓ *មិនស្គួញ*\n\nMenu ឬ /start",
        "select_language": "🌐 *ជ្រើស* 🌐\n\n:",
        "no_history": "📭 *No History*\n\nNo transactions yet.\n\n/start",
        "group_welcome": "👋 *Welcome to USDT Cambodia Exchange Group* 🏦\n\n🎯 *What we offer:*\n✅ Best USDT rates in Cambodia\n✅ Fast & secure transactions\n✅ 24/7 customer support\n✅ Multiple payment methods\n\n💬 *Need help?* Click the button below to start chatting with our bot!",
        "group_welcome_km": "👋 *Welcome to USDT Cambodia Exchange Group* 🏦\n\n🎯 *What we offer:*\n✅ Best USDT rates in Cambodia\n✅ Fast & secure transactions\n✅ 24/7 customer support\n✅ Multiple payment methods\n\n💬 *Need help?* Click the button below to start chatting with our bot!",
        "group_welcome_zh": "👋 *Welcome to USDT Cambodia Exchange Group* 🏦\n\n🎯 *What we offer:*\n✅ Best USDT rates in Cambodia\n✅ Fast & secure transactions\n✅ 24/7 customer support\n✅ Multiple payment methods\n\n💬 *Need help?* Click the button below to start chatting with our bot!",
    },
    "zh": {
        "welcome": "👋 *欢迎来到 USDT 柬埔寨交易所* 🏦\n\n✅ 快速安全交易 | 💰 最佳汇率 | 📞 24/7 在线客服\n\n👇 请选择您需要的操作:",
        "buy_usdt": "💵 *购买 USDT* 💵\n\n📋 *USDT 费率表*\n\n$10 – $49   →   费用 $1.00\n$50 – $99    →   费用 $1.50\n$100 – $199  →   费用 $2.50\n$200 – $399  →   费用 $4.00\n$400 – $699  →   费用 $6.00\n$700 – $1,199 →   费用 $8.00\n$1,200 – $2,499 →   费用 $11.00\n$2,500 – $4,999 →   费用 $17.00\n$5,000 – $7,499 →   费用 $23.00\n$7,500 – $10,000 →   费用 $26.00\n\n💳 *支持支付方式:* ABA / ACLEDA KHQR / Crypto Wallet\n\n🔗 *请选择充币网络:*",
        "sell_usdt": "💰 *出售 USDT* 💰\n\n📦 *最低出售:* {min_amount} USDT\n💵 *手续费:* {sell_fee}%\n\n📋 *支持的区块链网络:*\n\n🔷 TRC20   (最快, 手续费最低)\n🔶 BEP20   (速度快)\n💎 ERC20   (相对较慢, 手续费较高)\n\n🔗 *请选择收款网络:*",
        "support": "📞 *在线客服中心* 📞\n\n💚 我们全天候为您提供服务！\n\n🎯 *服务范围:*\n💬 交易咨询与帮助\n🛠️ 技术问题支持\n💱 购买/出售指导\n📩 联系专属客服\n\n📞 *立即联系我们:* @{config.SUPPORT_USERNAME}",
        "groups": "👥 *官方 USDT 交易群* 👥\n\n✨ *加入 P2P 群的优势:*\n✅ 直接与其他用户交易\n✅ 获取更优惠的交易汇率\n✅ 实时市场动态与资讯\n✅ 专业社区支持与交流\n\n⚠️ *安全提示:* 请务必通过官方渠道交易，谨防诈骗！\n\n👥 *立即加入:* 点击下方按钮",
        "rules": "📜 *平台交易规则* 📜\n\n1️⃣ *支付方式* - 仅支持 ABA 银行转账、ACLEDA KHQR 及银行转账\n2️⃣ *禁止私下交易* - 严禁在平台外进行任何形式的转账或交易\n3️⃣ *先收款后放币* - 核实收款后立即释放 USDT\n4️⃣ *及时确认* - 付款后请立即上传付款凭证\n5️⃣ *取消政策* - 频繁取消订单将受到限制\n6️⃣ *账户安全* - 禁止使用他人账户进行交易\n7️⃣ *争议处理* - 如有争议请通过平台客服解决\n8️⃣ *风控措施* - 可疑行为将导致账户暂停\n9️⃣ *汇率时效* - 汇率可能随时变动，请以实时汇率为准\n🔟 *风险提示* - P2P 交易存在一定风险，请谨慎操作",
        "rates": "📊 *实时 USDT 汇率* 📊\n\n💵 *基准汇率:* 1 USDT = {usd_to_khr:,} KHR\n\n💰 *交易手续费:*\n• 购买 USDT: {buy_fee}%\n• 出售 USDT: {sell_fee}%\n\n📦 *最低交易金额:* {min_amount} USDT\n\n💡 *温馨提示:* 汇率会根据市场波动实时更新，请以最终确认为准",
        "enter_amount_buy": "💰 *输入购买 USDT 金额* 💰\n\n📦 最低购买金额: {min_amount} USDT\n📈 最高购买金额: 10,000 USDT\n\n💵 *请输入您要购买的 USDT 数量:*",
        "enter_amount_sell": "💰 *输入出售 USDT 金额* 💰\n\n📦 最低出售金额: {min_amount} USDT\n📈 最高出售金额: 10,000 USDT\n\n💵 *请输入您要出售的 USDT 数量:*",
        "enter_payment_detail": "🏦 *输入收款信息* 🏦\n\n📷 上传 KHQR 二维码图片，或\n💳 输入 ABA 银行账户信息\n\n💡 我们将向此账户发送 KHR 付款:",
        "payment_detail_received": "✅ *收款信息已收到!* ✅\n\n📋 我们将向以下账户发送付款:\n{payment_detail}\n\n💰 请向平台钱包发送 USDT",
        "enter_wallet": "🏦 *输入收款钱包地址* 🏦\n\n📋 请输入您要接收 USDT 的钱包地址:\n\n💡 支持的网络: TRC20 / BEP20 / ERC20\n\n🔗 *请粘贴钱包地址:*",
        "upload_invoice": "📷 *上传付款凭证* 📷\n\n💡 请上传您的付款截图或银行转账凭证\n\n📁 *支持格式:* JPG, PNG, WEBP\n📦 *文件大小:* 最大 10MB\n\n📸 *点击下方按钮上传:*",
        "invoice_uploaded": "✅ *付款凭证已上传!* ✅\n\n📋 *订单编号:* #{order_id}\n💵 *交易金额:* {amount} USDT\n📊 *当前状态:* ⏳ 等待客服审核\n\n💚 *感谢您的信任！*\n客服将尽快核实并处理您的订单。",
        "order_timeout": "⏰ *订单 #{order_id} 已过期* ⏰\n\n⚠️ *超时提醒:* 付款时间已超过 {timeout} 分钟\n\n📞 如需继续交易，请重新发起新订单\n💡 输入 /start 开始新的交易",
        "order_cancelled": "❌ *订单已取消* ❌\n\n📞 如需帮助请联系客服\n💡 输入 /start 重新开始",
        "unknown_command": "❓ *未识别的命令* ❓\n\n💡 请使用菜单按钮或输入 /start\n📞 客服: @{config.SUPPORT_USERNAME}",
        "select_language": "🌐 *请选择语言* 🌐\n\n🇺🇸 English  |  🇰🇭 ភាសាខ្មែរ  |  🇨🇳 中文\n\n👇 *请点击下方选择您的语言:*",
        "no_history": "📭 *暂无交易记录* 📭\n\n💡 您还没有任何交易记录\n\n📞 开始交易请输入 /start\n💰 立即体验快速安全的 USDT 交易！"
    }
}

user_states, user_messages, transactions = {}, {}, {}

def set_state(user_id, state, data=None):
    user_states[user_id] = {"state": state, "data": data or {}, "timestamp": time.time()}
    logger.info(f"User {user_id} -> {state}")

def get_state(user_id):
    return user_states.get(user_id, {"state": "START", "data": {}, "timestamp": time.time()})

def clear_state(user_id):
    user_states.pop(user_id, None)
    user_messages.pop(user_id, None)

def add_message_id(user_id, msg_id):
    if user_id not in user_messages: user_messages[user_id] = []
    if msg_id not in user_messages[user_id]: user_messages[user_id].append(msg_id)

async def delete_old_messages(context, user_id, chat_id):
    for msg_id in user_messages.pop(user_id, []):
        try: await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except: pass

def get_user_language(user_id): return get_state(user_id)["data"].get("language", "en")

def get_message(key, lang="en", **kwargs):
    text = MESSAGES.get(lang, MESSAGES["en"]).get(key, key)
    for k, v in kwargs.items(): text = text.replace(f"{{{k}}}", str(v))
    return text

def validate_trc20(a): return len(a.strip()) == 34 and a.strip().startswith('T')
def validate_bep20(a): return len(a.strip()) == 42 and a.strip().startswith('0x')
validate_erc20 = validate_bep20

def get_khqr_link(amount): return f"https://acledabank.com.kh/acleda?data={config.KHQR_PAYMENT_DATA}&key={config.KHQR_KEY}&amount={int(amount)}" if amount > 0 else "https://acledabank.com.kh/acleda"

# ================= OXAPAY API =================
OXAPAY_NETWORK_MAP = {
    "TRC20": "TRON",
    "BEP20": "BSC",
    "ERC20": "ETH"
}

async def get_oxapay_address(network, order_id, amount=0):
    """Generate a static payment address using Oxapay API"""
    if not config.USE_OXAPAY:
        return None
    
    oxapay_network = OXAPAY_NETWORK_MAP.get(network, "TRON")
    
    payload = {
        "merchant_api_key": config.OXAPAY_API_KEY,
        "network": oxapay_network,
        "to_currency": "USDT",
        "auto_withdrawal": False,
        "order_id": order_id,
        "description": f"Order #{order_id}"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                config.OXAPAY_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            
            if data.get("status") == 100:
                return {
                    "address": data["data"]["address"],
                    "tag": data["data"].get("tag", ""),
                    "uri": data["data"].get("payURI", "")
                }
            else:
                error_msg = data.get("message", "Unknown error")
                logger.error(f"Oxapay error: {error_msg}")
                return None
    except Exception as e:
        logger.error(f"Oxapay API error: {e}")
        return None

def get_lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(LANGUAGES["en"]["name"], callback_data="lang_en"),
        InlineKeyboardButton(LANGUAGES["km"]["name"], callback_data="lang_km"),
        InlineKeyboardButton(LANGUAGES["zh"]["name"], callback_data="lang_zh")
    ]])

def get_main_keyboard(lang="en"):
    keyboards = {
        "en": [
            [KeyboardButton("🟢 Buy USDT"), KeyboardButton("🔴 Sell USDT")],
            [KeyboardButton("📞 Support"), KeyboardButton("👥 Groups")],
            [KeyboardButton("📜 Rules"), KeyboardButton("📊 Rates")],
            [KeyboardButton("📋 History"), KeyboardButton("🔙 Back")]
        ],
        "km": [
            [KeyboardButton("🟢 ទិញ USDT"), KeyboardButton("🔴 លក់ USDT")],
            [KeyboardButton("📞 គាំទ្រ"), KeyboardButton("👥 ក្រុម")],
            [KeyboardButton("📜 ច្បាប់"), KeyboardButton("📊 អត្រា")],
            [KeyboardButton("📋 ប្រវត្តិ"), KeyboardButton("🔙 ត្រឡប់")]
        ],
        "zh": [
            [KeyboardButton("🟢 购买 USDT"), KeyboardButton("🔴 出售 USDT")],
            [KeyboardButton("📞 客服"), KeyboardButton("👥 群组")],
            [KeyboardButton("📜 规则"), KeyboardButton("📊 汇率")],
            [KeyboardButton("📋 记录"), KeyboardButton("🔙 返回")]
        ]
    }
    return ReplyKeyboardMarkup(keyboards.get(lang, keyboards["en"]), resize_keyboard=True)

def get_network_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔷 TRC20", callback_data="net_trc20"),
         InlineKeyboardButton("🔶 BEP20", callback_data="net_bep20"),
         InlineKeyboardButton("💎 ERC20", callback_data="net_erc20")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ])

def get_confirm_keyboard(lang="en"):
    labels = {
        "en": ["✅ Payment Done", "🔙 Cancel"],
        "km": ["✅ បានទូ", "🔙 បោះ"],
        "zh": ["✅ 付款完成", "🔙 取消"]
    }
    l = labels.get(lang, labels["en"])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(l[0], callback_data="confirm_payment")],
        [InlineKeyboardButton(l[1], callback_data="cancel_order")]
    ])

def get_invoice_keyboard(uploaded=False, lang="en"):
    labels = {
        "en": ["✅ Invoice Uploaded", "🔙 Cancel Order", "📷 Upload Invoice"],
        "km": ["✅ បានផ្ញើ", "🔙 បោះបង់", "📷 ផ្ញើវិក្កយ"],
        "zh": ["✅ 凭证已上传", "🔙 取消订单", "📷 上传凭证"]
    }
    l = labels.get(lang, labels["en"])
    if uploaded:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(l[0], callback_data="invoice_uploaded")],
            [InlineKeyboardButton(l[1], callback_data="cancel_order")]
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(l[2], callback_data="upload_invoice")],
            [InlineKeyboardButton(l[1], callback_data="cancel_order")]
        ])

def get_admin_keyboard(user_id, order_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Approve", callback_data=f"admin_approve_{user_id}_{order_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"admin_reject_{user_id}_{order_id}")]
    ])

def calc_fee(a, p): return round(a * (p/100), 2)
def fmt_khr(a): return f"{int(a * config.EXCHANGE_RATE['USD_TO_KHR']):,}"
def gen_oid(): return f"ORD-{int(time.time())}"

def save_transaction(user_id, order_data):
    if user_id not in transactions:
        transactions[user_id] = []
    transactions[user_id].append({
        "order_id": order_data.get("order_id", ""),
        "type": order_data.get("type", "BUY"),
        "amount": order_data.get("amount", 0),
        "network": order_data.get("network", ""),
        "status": order_data.get("status", "PENDING"),
        "timestamp": time.time(),
        "fee": order_data.get("fee", 0)
    })

def get_user_transactions(user_id, limit=10):
    user_trans = transactions.get(user_id, [])
    return sorted(user_trans, key=lambda x: x.get("timestamp", 0), reverse=True)[:limit]

def format_transaction_message(tx_list, lang="en"):
    if not tx_list:
        return None
    
    status_icons = {
        "COMPLETED": "✅", "APPROVED": "✅", "PENDING": "⏳", "REJECTED": "❌", "CANCELLED": "🚫"
    }
    
    type_labels = {
        "en": {"BUY": "Buy USDT", "SELL": "Sell USDT"},
        "km": {"BUY": "Buy USDT", "SELL": "Sell USDT"},
        "zh": {"BUY": "Buy USDT", "SELL": "Sell USDT"}
    }
    
    icons = status_icons
    labels = type_labels.get(lang, type_labels["en"])
    
    msg = "📜 *Transaction History* 📜\n\n"
    
    for tx in tx_list:
        status = tx.get("status", "PENDING")
        type_label = labels.get(tx.get("type", "BUY"), "Buy USDT")
        date = datetime.fromtimestamp(tx.get("timestamp", time.time())).strftime("%Y-%m-%d %H:%M")
        
        msg += f"{icons.get(status, '📋')} *#{tx.get('order_id', 'N/A')}*\n"
        msg += f"  Type: {type_label}\n"
        msg += f"  Amount: {tx.get('amount', 0)} USDT\n"
        msg += f"  Network: {tx.get('network', 'N/A')}\n"
        msg += f"  Date: {date}\n"
        msg += f"  Status: {status}\n\n"
    
    return msg

async def start(update, context):
    user = update.message.from_user
    logger.info(f"User {user.id} started the bot")
    
    # Check if user already has a language selected
    existing_state = get_state(user.id)
    existing_lang = existing_state.get("data", {}).get("language")
    
    if existing_lang:
        # User already selected language, go directly to main menu
        await update.message.reply_text(
            get_message("welcome", existing_lang),
            reply_markup=get_main_keyboard(existing_lang),
            parse_mode="Markdown"
        )
        return
    
    # New user, show language selection
    clear_state(user.id)
    await update.message.reply_text(
        get_message("select_language"),
        reply_markup=get_lang_keyboard(),
        parse_mode="Markdown"
    )

async def help_command(update, context):
    await update.message.reply_text("Use /start or menu buttons", parse_mode="Markdown")

async def support_command(update, context):
    lang = get_user_language(update.message.from_user.id)
    await update.message.reply_text(
        get_message("support", lang),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📞 Contact Support", url=f"https://t.me/{config.SUPPORT_USERNAME}")]]),
        parse_mode="Markdown"
    )

async def rules_command(update, context):
    lang = get_user_language(update.message.from_user.id)
    await update.message.reply_text(get_message("rules", lang), parse_mode="Markdown")

async def history_command(update, context):
    user_id = update.message.from_user.id
    lang = get_user_language(user_id)
    tx_list = get_user_transactions(user_id, limit=10)
    
    if not tx_list:
        await update.message.reply_text(get_message("no_history", lang), parse_mode="Markdown")
        return
    
    history_text = format_transaction_message(tx_list, lang)
    await update.message.reply_text(history_text, parse_mode="Markdown")

async def handle_text(update, context):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    state_info = get_state(user_id)
    current_state = state_info["state"]
    lang = state_info["data"].get("language", "en")
    
    logger.info(f"User {user_id} sent: {text} (state: {current_state}, lang: {lang})")
    
    if text in ["/start", "🔙 Back", "🔙 ត្រឡប់", "🔙 返回"]:
        clear_state(user_id)
        await start(update, context)
        return
    
    if text == "/help":
        await help_command(update, context)
        return
    
    back_buttons = ["🔙 Back", "🔙 ត្រឡប់", "🔙 返回"]
    if text in back_buttons:
        clear_state(user_id)
        await start(update, context)
        return
    
    buy_buttons = ["🟢 Buy USDT", "🟢 ទិញ USDT", "🟢 购买 USDT"]
    if text in buy_buttons:
        # Preserve existing data (including language) when setting new state
        existing_data = state_info.get("data", {})
        if "language" not in existing_data:
            existing_data["language"] = lang
        set_state(user_id, "BUY_NETWORK", existing_data)
        await update.message.reply_text(
            get_message("buy_usdt", lang),
            reply_markup=get_network_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    sell_buttons = ["🔴 Sell USDT", "🔴 លក់ USDT", "🔴 出售 USDT"]
    if text in sell_buttons:
        # Preserve existing data (including language) when setting new state
        existing_data = state_info.get("data", {})
        if "language" not in existing_data:
            existing_data["language"] = lang
        set_state(user_id, "SELL_NETWORK", existing_data)
        sell_text = get_message("sell_usdt", lang,
            min_amount=config.EXCHANGE_RATE['MIN_AMOUNT'],
            sell_fee=config.EXCHANGE_RATE['SELL_FEE_PERCENT'])
        await update.message.reply_text(
            sell_text,
            reply_markup=get_network_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    support_buttons = ["📞 Support", "📞 គាំទ្រ", "📞 客服"]
    if text in support_buttons:
        await support_command(update, context)
        return
    
    groups_buttons = ["👥 Groups", "👥 ក្រុម", "👥 群组"]
    if text in groups_buttons:
        await update.message.reply_text(
            get_message("groups", lang),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥 Join Group", url=config.GROUP_LINK)]]),
            parse_mode="Markdown"
        )
        return
    
    rules_buttons = ["📜 Rules", "📜 ច្បាប់", "📜 规则"]
    if text in rules_buttons:
        await rules_command(update, context)
        return
    
    rates_buttons = ["📊 Rates", "📊 អត្រា", "📊 汇率"]
    if text in rates_buttons:
        rates_text = get_message("rates", lang,
            usd_to_khr=config.EXCHANGE_RATE['USD_TO_KHR'],
            buy_fee=config.EXCHANGE_RATE['BUY_FEE_PERCENT'],
            sell_fee=config.EXCHANGE_RATE['SELL_FEE_PERCENT'],
            min_amount=config.EXCHANGE_RATE['MIN_AMOUNT'])
        await update.message.reply_text(rates_text, parse_mode="Markdown")
        return
    
    history_buttons = ["📋 History", "📋 ប្រវត្តិ", "📋 记录"]
    if text in history_buttons:
        await history_command(update, context)
        return
    
    if current_state in ["BUY_AMOUNT", "SELL_AMOUNT"]:
        try:
            amount = float(text.replace(',', '').replace('$', ''))
            
            if amount < config.EXCHANGE_RATE["MIN_AMOUNT"]:
                msg = await update.message.reply_text(f"❌ Minimum amount is {config.EXCHANGE_RATE['MIN_AMOUNT']} USDT")
                add_message_id(user_id, msg.message_id)
                return
            
            if amount > 10000:
                msg = await update.message.reply_text("❌ Maximum is 10,000 USDT")
                add_message_id(user_id, msg.message_id)
                return
            
            state_info["data"]["amount"] = amount
            state_info["data"]["order_id"] = generate_order_id()
            state_info["data"]["type"] = "BUY" if current_state == "BUY_AMOUNT" else "SELL"
            
            await delete_old_messages(context, user_id, update.message.chat_id)
            
            if current_state == "BUY_AMOUNT":
                set_state(user_id, "BUY_WALLET", state_info["data"])
                msg = await update.message.reply_text(
                    get_message("enter_wallet", lang),
                    parse_mode="Markdown"
                )
                add_message_id(user_id, msg.message_id)
            else:
                # SELL - first ask for payment details
                state_info["data"]["fee"] = calculate_fee(amount, config.EXCHANGE_RATE['SELL_FEE_PERCENT'])
                set_state(user_id, "SELL_PAYMENT_DETAILS", state_info["data"])
                msg = await update.message.reply_text(
                    get_message("enter_payment_detail", lang),
                    parse_mode="Markdown"
                )
                add_message_id(user_id, msg.message_id)
            return
        
        except ValueError:
            msg = await update.message.reply_text("❌ Invalid amount")
            add_message_id(user_id, msg.message_id)
            return
    
    if current_state == "BUY_WALLET":
        wallet = text.strip()
        
        if len(wallet) < 10:
            msg = await update.message.reply_text("❌ Invalid wallet address")
            add_message_id(user_id, msg.message_id)
            return
        
        state_info["data"]["wallet"] = wallet
        
        network = state_info["data"]["network"]
        amount = state_info["data"]["amount"]
        order_id = state_info["data"]["order_id"]
        fee = calculate_fee(amount, config.EXCHANGE_RATE['BUY_FEE_PERCENT'])
        state_info["data"]["fee"] = fee
        total_khr = (amount + fee) * config.EXCHANGE_RATE["USD_TO_KHR"]
        
        set_state(user_id, "BUY_CONFIRM", state_info["data"])
        
        await delete_old_messages(context, user_id, update.message.chat_id)
        
        khqr_image = None
        if config.KHQR_IMAGE_PATH and os.path.exists(config.KHQR_IMAGE_PATH):
            khqr_image = config.KHQR_IMAGE_PATH
        
        network_display = {"TRC20": "TRC20", "BEP20": "BEP20", "ERC20": "ERC20"}
        
        payment_text = f"""📋 *Order #{order_id}* 📋

🔹 Type: Buy USDT
🔹 Network: {network_display.get(network, network)}
🔹 Amount: {amount} USDT
🔹 Fee: {fee} USDT
🔹 Total: {amount + fee} USDT

💵 *Payment:*
{total_khr:,} KHR

💳 *Bank:* {config.SUPPORT_USERNAME}
🔗 [Pay with KHQR]({get_khqr_link(total_khr)})

🏦 *Receive:*
`{wallet}`

⚠️ *Important:* Pay exactly {total_khr:,} KHR
⏰ *Timeout:* 15 minutes"""
        
        if khqr_image:
            try:
                with open(khqr_image, 'rb') as photo:
                    msg = await update.message.reply_photo(
                        photo=photo,
                        caption=payment_text,
                        reply_markup=get_confirm_keyboard(lang),
                        parse_mode="Markdown"
                    )
                    add_message_id(user_id, msg.message_id)
            except Exception:
                msg = await update.message.reply_text(
                    payment_text,
                    reply_markup=get_confirm_keyboard(lang),
                    parse_mode="Markdown"
                )
                add_message_id(user_id, msg.message_id)
        else:
            msg = await update.message.reply_text(
                payment_text,
                reply_markup=get_confirm_keyboard(lang),
                parse_mode="Markdown"
            )
            add_message_id(user_id, msg.message_id)
        
        return
    
    # Handle SELL_PAYMENT_DETAILS state
    if current_state == "SELL_PAYMENT_DETAILS":
        payment_detail = text.strip()
        
        if len(payment_detail) < 5:
            msg = await update.message.reply_text("❌ Please enter valid payment details")
            add_message_id(user_id, msg.message_id)
            return
        
        state_info["data"]["payment_detail"] = payment_detail
        
        network = state_info["data"]["network"]
        amount = state_info["data"]["amount"]
        order_id = state_info["data"]["order_id"]
        fee = state_info["data"]["fee"]
        receive_khr = (amount - fee) * config.EXCHANGE_RATE["USD_TO_KHR"]
        
        await delete_old_messages(context, user_id, update.message.chat_id)
        
        # Try to get Oxapay address
        oxapay_info = await get_oxapay_address(network, order_id)
        
        if oxapay_info:
            wallet = oxapay_info["address"]
            wallet_tag = oxapay_info.get("tag", "")
            pay_uri = oxapay_info.get("uri", "")
            state_info["data"]["oxapay_address"] = wallet
            state_info["data"]["oxapay_tag"] = wallet_tag
        else:
            # Fallback to static wallet
            wallet = config.PLATFORM_USDT_WALLET.get(network, "")
            wallet_tag = ""
            pay_uri = ""
        
        set_state(user_id, "SELL_CONFIRM", state_info["data"])
        
        network_display = {"TRC20": "TRC20", "BEP20": "BEP20", "ERC20": "ERC20"}
        
        # Build wallet display
        wallet_display = f"`{wallet}`"
        if wallet_tag:
            wallet_display += f"\n🏷️ Memo: `{wallet_tag}`"
        if pay_uri:
            wallet_display += f"\n🔗 [Pay Link]({pay_uri})"
        
        confirm_text = f"""📋 *Order #{order_id}* 📋

🔹 Type: Sell USDT
🔹 Network: {network_display.get(network, network)}
🔹 Amount: {amount} USDT
🔹 Fee: {fee} USDT
🔹 You Receive: {receive_khr:,} KHR

💳 *Your Payment Details:*
{payment_detail}

💰 *Send USDT to:*
{wallet_display}

⚠️ *Important:* Send only {network} USDT
⏰ *Timeout:* 15 minutes"""
        
        await update.message.reply_text(
            confirm_text,
            reply_markup=get_confirm_keyboard(lang),
            parse_mode="Markdown"
        )
        return
    
    msg = await update.message.reply_text(
        get_message("unknown_command", lang),
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )
    add_message_id(user_id, msg.message_id)

def calculate_fee(amount, fee_percent):
    return round(amount * (fee_percent / 100), 2)

def generate_order_id():
    return f"ORD-{int(time.time())}"

async def handle_photo(update, context):
    user_id = update.message.from_user.id
    state_info = get_state(user_id)
    current_state = state_info["state"]
    lang = state_info["data"].get("language", "en")
    
    logger.info(f"User {user_id} sent photo (state: {current_state})")
    
    # Handle KHQR photo upload during SELL_PAYMENT_DETAILS
    if current_state == "SELL_PAYMENT_DETAILS":
        photo = update.message.photo[-1]
        photo_file = await context.bot.get_file(photo.file_id)
        
        os.makedirs("invoices", exist_ok=True)
        
        timestamp = int(time.time())
        order_id = state_info["data"].get("order_id", "UNKNOWN")
        photo_path = f"invoices/khqr_{order_id}_{timestamp}.jpg"
        
        await photo_file.download_to_drive(photo_path)
        
        # Store KHQR info
        state_info["data"]["khqr_image"] = photo_path
        state_info["data"]["payment_detail"] = "KHQR Image Uploaded"
        
        network = state_info["data"]["network"]
        amount = state_info["data"]["amount"]
        fee = state_info["data"]["fee"]
        receive_khr = (amount - fee) * config.EXCHANGE_RATE["USD_TO_KHR"]
        
        await delete_old_messages(context, user_id, update.message.chat_id)
        
        # Try to get Oxapay address
        oxapay_info = await get_oxapay_address(network, order_id)
        
        if oxapay_info:
            wallet = oxapay_info["address"]
            wallet_tag = oxapay_info.get("tag", "")
            pay_uri = oxapay_info.get("uri", "")
            state_info["data"]["oxapay_address"] = wallet
            state_info["data"]["oxapay_tag"] = wallet_tag
        else:
            # Fallback to static wallet
            wallet = config.PLATFORM_USDT_WALLET.get(network, "")
            wallet_tag = ""
            pay_uri = ""
        
        set_state(user_id, "SELL_CONFIRM", state_info["data"])
        
        network_display = {"TRC20": "TRC20", "BEP20": "BEP20", "ERC20": "ERC20"}
        
        # Build wallet display
        wallet_display = f"`{wallet}`"
        if wallet_tag:
            wallet_display += f"\n🏷️ Memo: `{wallet_tag}`"
        if pay_uri:
            wallet_display += f"\n🔗 [Pay Link]({pay_uri})"
        
        confirm_text = f"""📋 *Order #{order_id}* 📋

🔹 Type: Sell USDT
🔹 Network: {network_display.get(network, network)}
🔹 Amount: {amount} USDT
🔹 Fee: {fee} USDT
🔹 You Receive: {receive_khr:,} KHR

💳 *Your Payment Details:*
📷 KHQR Image Uploaded

💰 *Send USDT to:*
{wallet_display}

⚠️ *Important:* Send only {network} USDT
⏰ *Timeout:* 15 minutes"""
        
        await update.message.reply_text(
            confirm_text,
            reply_markup=get_confirm_keyboard(lang),
            parse_mode="Markdown"
        )
        return
    
    if current_state != "INVOICE_UPLOAD":
        await update.message.reply_text(get_message("upload_invoice", lang), parse_mode="Markdown")
        return
    
    if state_info["data"].get("invoice_uploaded", False):
        await update.message.reply_text("❌ Invoice already uploaded!", parse_mode="Markdown")
        return
    
    photo = update.message.photo[-1]
    photo_file = await context.bot.get_file(photo.file_id)
    
    os.makedirs("invoices", exist_ok=True)
    
    timestamp = int(time.time())
    order_id = state_info["data"].get("order_id", "UNKNOWN")
    photo_path = f"invoices/invoice_{order_id}_{timestamp}.jpg"
    
    await photo_file.download_to_drive(photo_path)
    
    state_info["data"]["invoice_path"] = photo_path
    state_info["data"]["invoice_uploaded"] = True
    set_state(user_id, "INVOICE_UPLOAD", state_info["data"])
    
    confirm_text = get_message("invoice_uploaded", lang,
        order_id=order_id,
        amount=state_info['data'].get('amount', 0))
    
    await update.message.reply_text(confirm_text, parse_mode="Markdown")
    
    username = update.message.from_user.username or update.message.from_user.first_name or "Unknown"
    
    wallet_address = state_info['data'].get('wallet', 'N/A')
    network = state_info['data'].get('network', 'N/A')
    order_type = state_info['data'].get('type', 'BUY')
    fee = state_info['data'].get('fee', 0)
    payment_detail = state_info['data'].get('payment_detail', 'N/A')
    
    # Add payment details for SELL orders
    payment_section = "" if order_type == "BUY" else f"""💰 *User Payment Details (to receive KHR):*
{payment_detail}

"""
    
    admin_text = f"""🆕 *New Payment Received* 🆕

📋 *Order #{order_id}*

🔹 User: @{username} (ID: `{user_id}`)
🔹 Type: {order_type} USDT
🔹 Network: {network}
🔹 Amount: {state_info['data'].get('amount', 0)} USDT
🔹 Fee: {fee} USDT

{payment_section}🏦 *User Wallet Address:*
`{wallet_address}`

💳 *Status:* ✅ Invoice Uploaded

📷 *Invoice Attached*"""
    
    try:
        with open(photo_path, 'rb') as invoice_photo:
            await context.bot.send_photo(
                chat_id=config.ADMIN_ID,
                photo=invoice_photo,
                caption=admin_text,
                reply_markup=get_admin_keyboard(user_id, order_id),
                parse_mode="Markdown"
            )
    except Exception:
        await context.bot.send_message(
            chat_id=config.ADMIN_ID,
            text=admin_text,
            reply_markup=get_admin_keyboard(user_id, order_id),
            parse_mode="Markdown"
        )
    
    clear_state(user_id)

async def handle_callback(update, context):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    state_info = get_state(user_id)
    lang = state_info["data"].get("language", "en")
    
    logger.info(f"User {user_id} callback: {data}")
    
    if data.startswith("lang_"):
        lang_code = data.replace("lang_", "")
        if lang_code in LANGUAGES:
            await delete_old_messages(context, user_id, query.message.chat_id)
            
            try:
                await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
            except Exception:
                pass
            
            # Properly set the state with selected language
            set_state(user_id, "MAIN_MENU", {"language": lang_code})
            
            msg = await context.bot.send_message(
                chat_id=user_id,
                text=get_message("welcome", lang_code),
                reply_markup=get_main_keyboard(lang_code),
                parse_mode="Markdown"
            )
            add_message_id(user_id, msg.message_id)
        return
    
    if data.startswith("net_"):
        network = data.replace("net_", "").upper()
        network_names = {"TRC20": "TRC20", "BEP20": "BEP20", "ERC20": "ERC20"}
        
        state_info["data"]["network"] = network
        current_state = state_info["state"]
        
        if current_state == "BUY_NETWORK":
            set_state(user_id, "BUY_AMOUNT", state_info["data"])
            await query.edit_message_text(
                get_message("enter_amount_buy", lang,
                    min_amount=config.EXCHANGE_RATE['MIN_AMOUNT']),
                parse_mode="Markdown"
            )
        elif current_state == "SELL_NETWORK":
            set_state(user_id, "SELL_AMOUNT", state_info["data"])
            await query.edit_message_text(
                get_message("enter_amount_sell", lang,
                    min_amount=config.EXCHANGE_RATE['MIN_AMOUNT']),
                parse_mode="Markdown"
            )
        return
    
    if data == "back_main":
        clear_state(user_id)
        try:
            await query.edit_message_text("🔙 Returning...")
        except Exception:
            pass
        await start(query, context)
        return
    
    if data == "confirm_payment":
        state_info = get_state(user_id)
        order_id = state_info["data"].get("order_id", "UNKNOWN")
        
        state_info["data"]["payment_timestamp"] = time.time()
        set_state(user_id, "INVOICE_UPLOAD", state_info["data"])
        
        await delete_old_messages(context, user_id, query.message.chat_id)
        
        msg = await context.bot.send_message(
            chat_id=user_id,
            text=get_message("upload_invoice", lang),
            reply_markup=get_invoice_upload_keyboard(uploaded=False, lang=lang),
            parse_mode="Markdown"
        )
        add_message_id(user_id, msg.message_id)
        return
    
    if data == "upload_invoice":
        state_info = get_state(user_id)
        order_id = state_info["data"].get("order_id", "UNKNOWN")
        
        if state_info["data"].get("invoice_uploaded", False):
            await query.answer("❌ Invoice already uploaded!", show_alert=True)
            return
        
        await context.bot.send_message(
            chat_id=user_id,
            text=get_message("upload_invoice", lang),
            reply_markup=get_invoice_upload_keyboard(uploaded=False, lang=lang),
            parse_mode="Markdown"
        )
        return
    
    if data == "invoice_uploaded":
        await query.answer("✅ Invoice uploaded! Please wait.", show_alert=True)
        return
    
    if data == "cancel_order":
        clear_state(user_id)
        try:
            await query.edit_message_text(get_message("order_cancelled", lang))
        except Exception:
            pass
        
        await context.bot.send_message(
            chat_id=user_id,
            text=get_message("order_cancelled", lang),
            reply_markup=get_main_keyboard(lang)
        )
        return
    
    if data.startswith("admin_"):
        parts = data.split("_")
        action = parts[1]
        target_user_id = int(parts[2])
        order_id = parts[3]
        
        state_info = get_state(target_user_id)
        target_lang = state_info.get("data", {}).get("language", "en")
        amount = state_info.get("data", {}).get("amount", 0)
        network = state_info.get("data", {}).get("network", "")
        order_type = state_info.get("data", {}).get("type", "BUY")
        fee = state_info.get("data", {}).get("fee", 0)
        wallet_address = state_info.get("data", {}).get("wallet", "N/A")
        
        if action == "approve":
            save_transaction(target_user_id, {
                "order_id": order_id,
                "type": order_type,
                "amount": amount,
                "network": network,
                "status": "APPROVED",
                "fee": fee
            })
            
            if order_type == "SELL":
                platform_wallet = config.PLATFORM_USDT_WALLET.get(network, "")
                admin_buyer_msg = f"✅ *Order #{order_id} Approved!*\n\n💰 {amount} USDT has been received!\n💵 Payment will be processed to your bank shortly."
            else:
                admin_buyer_msg = f"✅ *Order #{order_id} Approved!*\n\n💚 USDT ({amount} {network}) will be sent to your wallet shortly!"
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=admin_buyer_msg,
                    parse_mode="Markdown"
                )
            except Exception:
                pass
            
            if order_type == "BUY":
                status_text = f"✅ Order #{order_id} - APPROVED\nType: {order_type} {network}\nAmount: {amount} USDT\nSend to: `{wallet_address}`"
            else:
                status_text = f"✅ Order #{order_id} - APPROVED\nType: {order_type} {network}\nAmount: {amount} USDT\nFee: {fee} USDT"
        
        elif action == "reject":
            save_transaction(target_user_id, {
                "order_id": order_id,
                "type": order_type,
                "amount": amount,
                "network": network,
                "status": "REJECTED",
                "fee": fee
            })
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"❌ *Order #{order_id} Rejected!*\n\n📞 Contact @{config.SUPPORT_USERNAME}",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
            status_text = f"❌ Order #{order_id} - REJECTED\nAmount: {amount} USDT ({network})"
        
        try:
            await query.edit_message_caption(status_text)
        except Exception:
            try:
                await query.edit_message_text(status_text)
            except Exception:
                pass
        
        clear_state(target_user_id)
        return
    
    try:
        await query.edit_message_text("Unknown action")
    except Exception:
        await query.answer("Unknown action")

def get_invoice_upload_keyboard(uploaded=False, lang="en"):
    labels = {
        "en": ["✅ Invoice Uploaded", "🔙 Cancel Order", "📷 Upload Invoice"],
        "km": ["✅ វិក្កយបានផ្ញើ", "🔙 បោះបង់កម្មង់", "📷 ផ្ញើវិក្កយ"],
        "zh": ["✅ 凭证已上传", "🔙 取消订单", "📷 上传凭证"]
    }
    label = labels.get(lang, labels["en"])
    
    if uploaded:
        keyboard = [
            [InlineKeyboardButton(label[0], callback_data="invoice_uploaded")],
            [InlineKeyboardButton(label[1], callback_data="cancel_order")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(label[2], callback_data="upload_invoice")],
            [InlineKeyboardButton(label[1], callback_data="cancel_order")]
        ]
    return InlineKeyboardMarkup(keyboard)

async def check_timeouts(context):
    timeout_seconds = config.PAYMENT_TIMEOUT_SECONDS
    
    for user_id in list(user_states.keys()):
        state_info = get_state(user_id)
        current_state = state_info["state"]
        lang = state_info["data"].get("language", "en")
        
        if current_state in ["BUY_CONFIRM", "SELL_CONFIRM", "INVOICE_UPLOAD"]:
            state_timestamp = state_info.get("timestamp", time.time())
            elapsed = time.time() - state_timestamp
            
            if elapsed > timeout_seconds:
                order_id = state_info["data"].get("order_id", "UNKNOWN")
                timeout_minutes = timeout_seconds // 60
                
                logger.info(f"Order #{order_id} timed out for user {user_id}")
                
                try:
                    timeout_text = get_message("order_timeout", lang,
                        order_id=order_id,
                        timeout=timeout_minutes)
                    
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=timeout_text,
                        parse_mode="Markdown"
                    )
                except Exception:
                    pass
                
                clear_state(user_id)

async def handle_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when users join or leave the group."""
    chat_member = update.my_chat_member
    
    if chat_member is None:
        return
    
    user = chat_member.from_user
    chat = chat_member.chat
    new_status = chat_member.new_chat_member.status
    old_status = chat_member.old_chat_member.status
    
    # Only respond when user joins (not when they leave or get banned)
    if new_status == "member" and old_status in ["left", "kicked", "restricted"]:
        logger.info(f"User {user.id} ({user.first_name}) joined group {chat.id}")
        
        username = user.first_name or "User"
        bot_username = context.bot.username
        
        keyboard = [
            [
                InlineKeyboardButton("🟢 Buy USDT", callback_data="BUY_USDT"),
                InlineKeyboardButton("🔴 Sell USDT", callback_data="SELL_USDT")
            ],
            [
                InlineKeyboardButton("📊 Exchange Rate", callback_data="RATE")
            ],
            [
                InlineKeyboardButton("🆘 Support", url=f"https://t.me/{bot_username}")
            ]
        ]
        
        welcome_text = f"""🎉 ស្វាគមន៍ {username} មកកាន់ MP Exchange (https://t.me/iknowkhstore)!

⚠️ សូមប្រយ័ត្នការបោកប្រាស់
🚫 MP Exchange មិនដែល Inbox អ្នកមុនទេ

💵 ទិញ–លក់ USDT ងាយស្រួល សុវត្ថិភាព និងរហ័ស
🙏 សូមអរគុណដែលជឿទុកចិត្ត MP Exchange"""
        
        try:
            # Send welcome to group
            await context.bot.send_message(
                chat_id=chat.id,
                text=welcome_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
            # Also try to DM the user
            await context.bot.send_message(
                chat_id=user.id,
                text=welcome_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            logger.error(f"Failed to send welcome message: {e}")

# Handle welcome message when users join group
async def handle_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when users join the group."""
    if update.message is None:
        return
    
    chat = update.message.chat
    
    # Only process in groups/supergroups
    if chat.type == "private":
        return
    
    new_members = update.message.new_chat_members
    if not new_members:
        return
    
    for member in new_members:
        # Skip if it's the bot itself
        if member.id == context.bot.id:
            continue
        
        logger.info(f"User {member.id} ({member.first_name}) joined group {chat.id}")
        
        username = member.first_name or "User"
        bot_username = context.bot.username
        
        keyboard = [
            [
                InlineKeyboardButton("🟢 Buy USDT", callback_data="BUY_USDT"),
                InlineKeyboardButton("🔴 Sell USDT", callback_data="SELL_USDT")
            ],
            [
                InlineKeyboardButton("📊 Exchange Rate", callback_data="RATE")
            ],
            [
                InlineKeyboardButton("🆘 Support", url=f"https://t.me/{bot_username}")
            ]
        ]
        
        welcome_text = f"""🎉 ស្វាគមន៍ {username} មកកាន់ MP Exchange (https://t.me/iknowkhstore)!

⚠️ សូមប្រយ័ត្នការបោកប្រាស់
🚫 MP Exchange មិនដែល Inbox អ្នកមុនទេ

💵 ទិញ–លក់ USDT ងាយស្រួល សុវត្ថិភាព និងរហ័ស
🙏 សូមអរគុណដែលជឿទុកចិត្ត MP Exchange"""
        
        try:
            # Send welcome to group
            await context.bot.send_message(
                chat_id=chat.id,
                text=welcome_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            logger.error(f"Failed to send welcome message: {e}")

# Handle welcome message button callbacks
async def handle_welcome_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from welcome message buttons - send DM to user."""
    query = update.callback_query
    if query is None:
        return
    
    user = query.from_user
    chat = query.message.chat_id
    message_id = query.message.message_id
    
    await query.answer()
    
    bot_username = context.bot.username
    
    keyboard = [
        [
            InlineKeyboardButton("🟢 Buy USDT", callback_data="BUY_USDT"),
            InlineKeyboardButton("🔴 Sell USDT", callback_data="SELL_USDT")
        ],
        [
            InlineKeyboardButton("📊 Exchange Rate", callback_data="RATE")
        ],
        [
            InlineKeyboardButton("🆘 Support", url=f"https://t.me/{bot_username}")
        ]
    ]
    
    if query.data == "BUY_USDT":
        response_text = "🟢 Buy USDT\n\nPlease enter the amount of USDT you want to buy:\n\nExample: 100"
    elif query.data == "SELL_USDT":
        response_text = "🔴 Sell USDT\n\nPlease enter the amount of USDT you want to sell:\n\nExample: 100"
    elif query.data == "RATE":
        response_text = "📊 Exchange Rate\n\n💵 USDT → KHR\n\nCurrent rates will be displayed here."
    else:
        return
    
    try:
        # Send response to user's DM
        await context.bot.send_message(
            chat_id=user.id,
            text=response_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Remove the welcome message button in group
        await context.bot.edit_message_reply_markup(
            chat_id=chat,
            message_id=message_id,
            reply_markup=None
        )
    except Exception as e:
        logger.error(f"Failed to send DM: {e}")
        # Fallback: edit message in group
        await query.edit_message_text(response_text)

# Group link deletion handler
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete links sent in group and warn user."""
    if update.message is None:
        return
    
    chat = update.message.chat
    
    # Only process in groups/supergroups, not private chats
    if chat.type == "private":
        return
    
    user = update.message.from_user
    text = update.message.text or ""
    
    # Skip admins (you can configure admin IDs in config.py)
    if hasattr(config, 'ADMIN_ID') and user.id in [config.ADMIN_ID] if isinstance(config.ADMIN_ID, list) else user.id == config.ADMIN_ID:
        return
    
    # Check for URLs (simplified)
    url_pattern = re.compile(r'https?://|www\.|[a-zA-Z0-9]+\.[a-zA-Z]{2,}', re.IGNORECASE)
    has_link = bool(url_pattern.search(text)) or any(e.url for e in (update.message.entities or []))

# ================= REAL-TIME CRYPTO RATES =================
import httpx

# Cache for exchange rates (cache for 60 seconds)
_rate_cache = {
    'usdt_price': None,
    'btc_price': None,
    'eth_price': None,
    'last_update': 0
}

CACHE_DURATION = 60  # seconds

async def fetch_crypto_prices():
    """Fetch real-time crypto prices from Binance API."""
    global _rate_cache
    
    # Check cache first
    current_time = time.time()
    if _rate_cache['last_update'] and (current_time - _rate_cache['last_update']) < CACHE_DURATION:
        return _rate_cache
    
    try:
        # Fetch USDT prices from Binance
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get BTC/USDT price
            btc_response = await client.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
            btc_price = float(btc_response.json().get('price', 0))
            
            # Get ETH/USDT price
            eth_response = await client.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT')
            eth_price = float(eth_response.json().get('price', 0))
            
            # Get USDT price (usually close to $1)
            usdt_response = await client.get('https://api.binance.com/api/v3/ticker/price?symbol=USDTUSDT')
            usdt_price = float(usdt_response.json().get('price', 1.0))
            
            # Update cache
            _rate_cache = {
                'usdt_price': usdt_price,
                'btc_price': btc_price,
                'eth_price': eth_price,
                'last_update': current_time
            }
            
            logger.info(f"Fetched crypto prices: BTC=${btc_price:,.2f}, ETH=${eth_price:,.2f}")
            return _rate_cache
    except Exception as e:
        logger.error(f"Failed to fetch crypto prices: {e}")
        # Return cached data or defaults
        if _rate_cache['last_update']:
            return _rate_cache
        return {
            'usdt_price': 1.0,
            'btc_price': 0,
            'eth_price': 0,
            'last_update': 0
        }

def get_formatted_rates(usd_to_khr, buy_fee, sell_fee, min_amount, crypto_data=None):
    """Format rates message with real-time crypto data."""
    from datetime import datetime
    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    
    crypto_section = ""
    if crypto_data and crypto_data.get('btc_price', 0) > 0:
        crypto_section = f"""
━━━━━━━━━━━━━━━━━
💹 *Crypto Market:*
• BTC: ${crypto_data['btc_price']:,.2f}
• ETH: ${crypto_data['eth_price']:,.2f}
• USDT: ${crypto_data['usdt_price']:,.4f}"""
    
    rate_text = f"""📊 *Real-Time Exchange Rates* 📊
⏰ Updated: {now}

💵 *USD to KHR:* 1 USD = {usd_to_khr:,} KHR

💰 *Buy USDT:*
• Fee: {buy_fee}%
• Min: {min_amount} USDT

💸 *Sell USDT:*
• Fee: {sell_fee}%
• Min: {min_amount} USDT

🔷 *TRC20:* Fast, Low Fee
🔶 *BEP20:* Fast
💎 *ERC20:* Higher Fee{crypto_section}

━━━━━━━━━━━━━━━━━
💬 *Contact:* @{config.SUPPORT_USERNAME}
🌐 *Channel:* https://t.me/iknowkhstore"""
    return rate_text


# ================= SCHEDULED RATE BROADCAST =================
async def send_scheduled_rates(context: ContextTypes.DEFAULT_TYPE):
    """Send exchange rates to channel/group on schedule with real-time data."""
    if not getattr(config, 'RATE_BROADCAST_ENABLED', False):
        return
    
    channel_id = getattr(config, 'RATE_CHANNEL_ID', None)
    if not channel_id:
        logger.warning("RATE_CHANNEL_ID not configured")
        return
    
    # Get current exchange rate info
    usd_to_khr = config.EXCHANGE_RATE.get('USD_TO_KHR', 4050)
    buy_fee = config.EXCHANGE_RATE.get('BUY_FEE_PERCENT', 2)
    sell_fee = config.EXCHANGE_RATE.get('SELL_FEE_PERCENT', 1)
    min_amount = config.EXCHANGE_RATE.get('MIN_AMOUNT', 10)
    
    # Fetch real-time crypto prices
    crypto_data = await fetch_crypto_prices()
    
    # Build rate message with real-time data
    rate_text = get_formatted_rates(usd_to_khr, buy_fee, sell_fee, min_amount, crypto_data)
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("🟢 Buy USDT", callback_data="BUY_USDT"),
            InlineKeyboardButton("🔴 Sell USDT", callback_data="SELL_USDT")
        ],
        [
            InlineKeyboardButton("💬 Contact Support", url=f"https://t.me/{config.SUPPORT_USERNAME}")
        ]
    ]
    
    try:
        await context.bot.send_message(
            chat_id=channel_id,
            text=rate_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        logger.info(f"Sent scheduled exchange rates to channel {channel_id}")
    except Exception as e:
        logger.error(f"Failed to send scheduled rates: {e}")

def get_broadcast_interval():
    """Get broadcast interval in minutes."""
    interval = getattr(config, 'RATE_BROADCAST_INTERVAL', '1hour')
    
    intervals = {
        '30min': 30,
        '1hour': 60,
        '1day': 1440
    }
    
    return intervals.get(interval, 60)  # Default: 1 hour


def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CommandHandler("rules", rules_command))
    app.add_handler(CommandHandler("history", history_command))
    
    app.add_handler(CallbackQueryHandler(handle_welcome_buttons, pattern="^(BUY_USDT|SELL_USDT|RATE)$"))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_members))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.ALL, handle_group_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    job_queue = app.job_queue
    
    # Start scheduled rate broadcast if enabled
    if getattr(config, 'RATE_BROADCAST_ENABLED', False):
        interval_minutes = get_broadcast_interval()
        job_queue.run_repeating(
            send_scheduled_rates,
            interval=interval_minutes * 60,  # Convert to seconds
            first=30  # Start 30 seconds after bot starts
        )
        logger.info(f"Scheduled rate broadcast enabled: every {interval_minutes} minutes")
    
    job_queue.run_repeating(check_timeouts, interval=60, first=60)
    
    logger.info("Starting USDT Cambodia Exchange Bot (Multi-Language)...")
    app.run_polling()


if __name__ == "__main__":
    main()