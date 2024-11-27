import telebot
import requests
import threading

TOKEN = 'توكن البوت '
bot = telebot.TeleBot(TOKEN)


ALLOWED_USERS = [ ايدي ]  

def is_user_allowed(user_id):
    return user_id in ALLOWED_USERS

@bot.message_handler(commands=['start'])
def send_phone(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "انت غر مشترك في هذا البوت يرجى تحدث مع المطور من احل الاشتراك @I_IY9 والرجاء الانضمام هنا للحصول على كل شي جديد  https://t.me/HACKTEAM33")
        return

    bot.reply_to(message, "بوت اسماعيل يرحب بك في اي وقت يرجى الانضمام هنا https://t.me/HACKTEAM33 وايضا اشترك هنا فضلا وليس امرا  https://t.me/HACKTEAM33 ")
    bot.send_message(message.chat.id, "حط رقمك هنا الشرائح المدعومة يوز فقط 📱 ")
    bot.register_next_step_handler(message, send_verification_code)

def send_verification_code(message):
    phone_number = message.text
    url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": phone_number,
        "language": "AR"
    }
    headers = {
        "User-Agent": "okhttp/4.9.3",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    if "ROOGY" in response.text:
        bot.send_message(message.chat.id, "حط الرمز لي وصلك وستغفر في طريق 💬")
        bot.register_next_step_handler(message, verify_code, phone_number)
    else:
        bot.send_message(message.chat.id, "هناك خطأ ما اعد التشغيل بعد قليل ")

def verify_code(message, phone_number):
    otp_code = message.text
    url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": phone_number,
        "language": "AR",
        "otp": otp_code
    }
    headers = {
        "User-Agent": "okhttp/4.9.3",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    response_json = response.json()
    if "access_token" in response_json:
        bot.send_message(message.chat.id, "تم التحقق من الرمز... سيتم ارسال الانترنت بعد كل 20 دقيقه  بشكل تلقائي 🌹")
        access_token = response_json["access_token"]
        send_requests_six_times(message, access_token)
        
        threading.Timer(20 * 60, repeat_requests, args=[message, access_token]).start()
    else:
        bot.send_message(message.chat.id, "هناك خطأ ما اثناء الارسال 💔")

def send_requests_six_times(message, access_token):
    for i in range(6):
        threading.Timer(2 * i, send_final_request, args=[message, access_token]).start()

def send_final_request(message, access_token):
    url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'language': 'AR',
        'request-id': 'ed66ca07-7aee-4b97-952c-f0fcbc7eee0f',
        'flavour-type': 'gms',
        'Content-Type': 'application/json; charset=utf-8',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = '{"skipMgm":false,"mgmValue":"5.5GB"}'

    response = requests.post(url, headers=headers, data=data)
    bot.send_message(message.chat.id, "استغفر الله... سيتم إرسال لك انترنت  ")

    balance = check_balance(access_token)
    if balance is not None:
        bot.send_message(message.chat.id, f"رصيد الانترنت الحالي هو  : {balance}")
    else:
        bot.send_message(message.chat.id, "لم يتم استرجاع الرصيد.")

def check_balance(access_token):
    url = "https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/balance"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "okhttp/4.9.3",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'language': "AR",
        'request-id': "995fd8a7-853c-481d-b9c6-0a24295df76a",
        'flavour-type': "gms"
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    accounts = response_json.get('accounts', [])

    for account in accounts:
        if account.get('label') == 'رصيد التكفل المهدى':
          return account.get('value', None)

    bot.send_message(message.chat.id, "  رصيد الانترنت الجديد هو :")
    
    return None

def repeat_requests(message, access_token):
    send_final_request(message, access_token)
    threading.Timer(20 * 60, repeat_requests, args=[message, access_token]).start()

# تشغيل البوت
bot.polling(none_stop=True)