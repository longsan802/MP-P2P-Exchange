# Script to fix markdown parsing issues in main.py

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix both occurrences - remove emoji before bold markup
old_text = "💰 *📥 DEPOSIT USDT via Oxapay:*"
new_text = "*📥 DEPOSIT USDT via Oxapay:*"

count = content.count(old_text)
print(f"Found {count} occurrences of old text")

content = content.replace(old_text, new_text)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
