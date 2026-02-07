# 🇰🇭 USDT Cambodia Exchange Bot

A production-ready Telegram bot for USDT Buy/Sell operations with KHQR payment support for Cambodia market.

## ✨ Features

- 🟢 **Buy USDT** - Purchase USDT using Cambodia bank via KHQR
- 🔴 **Sell USDT** - Sell USDT and receive payment via Cambodia bank
- 🔗 **Multi-Network Support** - TRC20, BEP20, ERC20
- 📱 **State-Based Flow** - Smooth conversation handling
- 👮 **Admin Panel** - Approve/Reject transactions
- ⏰ **Timeout Handling** - 30-minute payment window
- 📞 **Support System** - Built-in support contact
- 📜 **Rules Display** - Clear exchange rules

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Bot

Edit [`config.py`](config.py) with your settings:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789
PLATFORM_USDT_WALLET = {
    "TRC20": "your_trc20_address",
    "BEP20": "your_bep20_address",
    "ERC20": "your_erc20_address"
}
KHQR_IMAGE_URL = "https://your-domain.com/khqr.png"
```

### 3. Get Your Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` to create a new bot
3. Follow the instructions
4. Copy the token and paste it in [`config.py`](config.py)

### 4. Get Your Admin ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Copy your user ID and paste it in [`config.py`](config.py)

### 5. Run the Bot

```bash
python main.py
```

## 📁 Project Structure

```
BOT USDT/
├── main.py           # Main bot application
├── config.py         # Configuration file
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## 🧠 Bot Flow

### Buy USDT Flow

```
User selects "Buy USDT"
        ↓
Select Network (TRC20/BEP20/ERC20)
        ↓
Enter USDT Amount
        ↓
Enter User Wallet Address
        ↓
Show KHQR Payment Code
        ↓
User Pays via Cambodia Bank
        ↓
Admin Receives Notification
        ↓
Admin Approve/Reject
        ↓
User Notified + Thank You Message
```

### Sell USDT Flow

```
User selects "Sell USDT"
        ↓
Select Network (TRC20/BEP20/ERC20)
        ↓
Enter USDT Amount
        ↓
Show Platform Wallet Address
        ↓
User Transfers USDT to Platform
        ↓
Admin Receives Notification
        ↓
Admin Approve/Reject
        ↓
User Notified + Payment Sent + Thank You Message
```

## 🛠️ Configuration Options

### config.py Settings

| Setting | Description | Example |
|---------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token from BotFather | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `ADMIN_ID` | Your Telegram user ID | `123456789` |
| `PLATFORM_USDT_WALLET` | Platform wallet addresses for each network | `{"TRC20": "...", ...}` |
| `KHQR_IMAGE_URL` | URL of KHQR payment code image | `https://example.com/khqr.png` |
| `SUPPORT_USERNAME` | Your support username | `YourSupport` |
| `GROUP_LINK` | Telegram group link | `https://t.me/yourgroup` |
| `PAYMENT_TIMEOUT_SECONDS` | Payment timeout in seconds | `1800` (30 minutes) |

## 🎮 Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show main menu |
| `/help` | Show help information |
| `/support` | Get support contact |
| `/rules` | View exchange rules |

## 👮 Admin Functions

Admins receive notifications for each order with:

- **Approve Button** - Approve transaction and notify user
- **Reject Button** - Reject transaction and notify user
- **View Details Button** - View full order details

## 🔒 Security Best Practices

1. **Never share your bot token**
2. **Use environment variables for sensitive data** (recommended for production)
3. **Verify all transactions manually**
4. **Enable rate limiting** (for production deployment)
5. **Use webhook mode** instead of polling for high traffic

## 🚀 Deployment Options

### Option 1: Local Run

```bash
python main.py
```

### Option 2: VPS (Linux)

```bash
# SSH into your server
sudo apt update
sudo apt install python3-pip git screen

# Clone and setup
git clone <your-repo-url>
cd BOT\ USDT/
pip install -r requirements.txt

# Run in screen
screen -S usdt_bot
python main.py
# Press Ctrl+A then D to detach
```

### Option 3: Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

## 📝 Next Upgrades (Version 2)

- [ ] **Database Integration** - PostgreSQL/MySQL for order history
- [ ] **Multi-Admin Support** - Multiple admins with roles
- [ ] **Auto-Timeout Handling** - Automatic order cancellation
- [ ] **Exchange Rate API** - Automatic rate updates
- [ ] **Transaction History** - User transaction log
- [ ] **Webhook Mode** - Production-ready deployment
- [ ] **Multi-Language** - Khmer language support 🇰🇭
- [ ] **Web Dashboard** - Admin web panel
- [ ] **User Authentication** - Registration system

## 🤝 Contributing

Feel free to fork and improve this bot. Pull requests are welcome!

## 📞 Support

Need help? Contact: @YourSupport

## 📄 License

This project is open source and available for personal and commercial use.

---

**Made with ❤️ for Cambodia USDT Exchange**
