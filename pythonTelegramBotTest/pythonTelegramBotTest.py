import telebot
import datetime
import requests
import time
import schedule


from bs4 import BeautifulSoup


ty=datetime.datetime.today()

URLholi = "https://www.calend.ru/holidays/"+ str(ty.month) + '-' +str(ty.day) +'/'
URLnames = "https://www.calend.ru/names/"+ str(ty.month) + '-' +str(ty.day) +'/'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Accept': '*/*'}

def get_html(url,params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_hol(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('li', class_='three-three')

    holidays =[]

    for item in items:
        holidays.append(item.find('span', class_='title').get_text(strip=True))
    return holidays

def get_nam(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('span', class_='caption')

    names =[]

    for item in items:
        names.append(item.find('a', class_='title').get_text(strip=True))
    return names


def send_hol(holidays,message):
    for holiday in holidays:
        def send_h():
            def sendh():
                bot.send.message(chat_id, 'Сегодня отличный повод выпить бутылочку пивка! Ведь сегодня весь мир празднует '+holiday)
            schedule.every(900/lh).minutes.do(sendh)
        schedule.every().day.at('08:00').do(send_h)

def send_m_and_n(names, message):
    def send_m():
        bot.send_message(message.from_user.id, 'С добрым утром! Сегодня именины у этих прекрасных людей:')
        for name in names:
             bot.send_message(message.from_user.id,name)
        bot.send_message(message.from_user.id, 'Так выпьем же за них!')
    def send_n():
        bot.send_message(message.from_user.id, 'Надеюсь у тебя был хороший день. Доброй ночи!')
    schedule.every().day.at('07:00').do(send_m)
    schedule.every().day.at('00:00').do(send_n)
        

token ='1894145912:AAHd4C0YxJljldK6tv7xCdLDg4qtRAY5Izs'
bot=telebot.TeleBot(token)
@bot.message_handler(content_types=['text'])

def main(message):

    htmlh = get_html(URLholi)
    if htmlh.status_code==200:
        htmln = get_html(URLnames)
        if htmln.status_code==200:

            holidays = get_hol(htmlh.text)
            lh= len(holidays)

            names = get_nam(htmln.text)
            ln=len(names)

            send_m_and_n(names,message)
            send_hol(holidays,message)

    if message.text == "/help":
        bot.send_message(message.from_user.id, "Тебе никто не поможет.")
    elif message.text =="/stop":
        bot.send_message(message.from_user.id, "Меня никто не остановит.")
    else:
         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help или /stop")
    while True:
        schedule.run_pending()
        time.sleep(5)

# RUN
bot.polling(none_stop=True)