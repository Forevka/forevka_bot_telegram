import sys, traceback, time, config, telebot,sqlite3, dbworker, random, grabing, ast, get_weather, virus_total
import wget,os
import lxml.html as lhtml
from google import search
from telebot import types
from vedis import Vedis
from calculator.simple import SimpleCalculator
from googletrans import Translator

conn = sqlite3.connect('bot_data.sqlite')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

bot = telebot.TeleBot(config.token)
###
markup = types.ReplyKeyboardMarkup()
markup.row('Политика', 'Спорт')
markup.row('Культура', 'Наука')
hide_mark=types.ReplyKeyboardRemove()

markup_story=types.ReplyKeyboardMarkup()
markup_story.row('ItHappens', 'Bash.im')

markup_weather=types.ReplyKeyboardMarkup()
#sticker=types.get_sticker_set("Catkus")

@bot.message_handler(func=lambda message: True, commands=['help',"test","news","roll","sticker","advice","story","weather","check","music","comics"])
def check_command(message):
    if message.text=="/help":
            bot.send_message(message.chat.id,"Я могу:\n/test - тестовая функция\n/help - показать это сообщение\n/news - покажу вам новость на выбор\n/roll - случайное число от 1 до 100\n/calc - решу вам уравнение\n/trans - переведу вам слово(через дорогу)\n/say - скажу вашу фразу\n/story - расскажу занятную историю связанную с IT\n/weather - покажу погоду за вибраною датою та часом\n/check - провірю ваш файл на віруси\n/music - відправлю вам музику сгенеровану комп'ютером\n/comics - відправлю вам комікс")
    elif message.text=="/test":
            bot.send_message(message.chat.id,"TEST TEST \nTEST TEST")
    elif message.text=="/news":
            #data = urllib2.urlopen(query)
            #reply=search('Новости', tld='ru', lang='ru', stop=1)
            bot.send_message(message.chat.id,"Про какие новости вы хотите узнать?\nТыкай, тыкай! Ну или вводи сам", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.S_CHOOSE_THEME.value)
            #bot.send_message(message.chat.id,"Про какие новости вы хотите узнать?\n Тыкай, тыкай!", reply_markup=hide_mark)
    elif message.text=="/sticker":
            img_file=open("stickers/kuku.webp")
            bot.send_document(message.chat.id,img_file)
    elif message.text=="/roll":
            bot.send_message(message.chat.id,"Случайное число 1 до 100: "+str(random.randint(1,100)))
    elif message.text=="/story":
        #
        bot.send_message(message.chat.id, "С какого сайта?", reply_markup=markup_story)
        dbworker.set_state(message.chat.id, config.States.S_GET_STORY.value)
    elif message.text=="/weather":
        reply=get_weather.weather();
        data_time=[];
        temperature=[];
        winter_speed=[];
        winter_direction=[];
        description=[];
        for i in range(0,len(reply),1):
            #print(reply[i][0])
            data_time.append(reply[i][0])
            #print(data_time[i])
            temperature.append(reply[i][1])
            winter_speed.append(reply[i][2])
            winter_direction.append(reply[i][3])
        description.append(reply[i][4])
        for i in range(0,20,1):
            markup_weather.row(data_time[i],data_time[i+20])
        bot.send_message(message.chat.id, "Погода за какое время?",reply_markup=markup_weather)
        dbworker.set_state(message.chat.id, config.States.S_ENTER_DATE.value)
    elif message.text=="/check":
        bot.send_message(message.chat.id, "Відправ мені файл який потрібно перевірити на віруси")
        dbworker.set_state(message.chat.id, config.States.S_CHECK_AV.value)
    elif message.text=="/music":
        music=grabing.get_music();
        bot.send_audio(message.chat.id, audio=open(music, 'rb'))
        os.remove(music)
    elif message.text=="/comics":
        list_img=grabing.get_comics();
        bot.send_message(message.chat.id, list_img[0])
        bot.send_photo(message.chat.id, photo=open(list_img[2], 'rb'))
        bot.send_message(message.chat.id, list_img[1])
        os.remove(list_img[2])
    #elif message.text=="/calc":
     #   bot.send_message(message.chat.id,"Отправьте уравнение")
      #  dbworker.set_state(message.chat.id, config.States.S_ENTER_EXPR.value)
        #print(config.States.S_ENTER_EXPR.value)
        
    #elif message.text=="/sticker":
    #       bot.send_sticker(message.chat.id,)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GET_STORY.value)
def user_story_send(message):    
    if message.text=="ItHappens":
        reply=grabing.get_story(message.text);
    elif message.text=="Bash.im":
        reply=grabing.get_story(message.text);
    else:
        reply="Незнаю такого сайта :("
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, reply, reply_markup=hide_mark)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CHECK_AV.value, content_types=['document'])
def user_check_antivirus(message):
    #print("AV")
    #bot.send_message(message.chat.id, message)
    file_id=message.document.file_id;
    new_file=bot.get_file(file_id)
    print(new_file)
    #test_file=urllib.URLopener()
    path="https://api.telegram.org/file/bot"+config.token+"/"+new_file.file_path
    print(path)
    source=wget.download(path)
    print(source)
    reply=virus_total.virus_check(source)
    #urllib.urlretrieve("https://api.telegram.org/file/"+config.token+"/"+new_file.file_path, message.document.file_name)
    #https://api.telegram.org/file/bot<token>/<file_path>
    #new_file.download(message.document.file_name)
    bot.send_message(message.chat.id, reply)
    
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_DATE.value)
def user_entering_date(message):
    reply=get_weather.weather();
    data_time=[];
    for i in range(0,len(reply),1):
        #print(reply[i][0])
        data_time.append(reply[i][0])
        if data_time[i]==message.text:
            reply="Дата: "+reply[i][0]+"\nТемпература: "+reply[i][1]+"\nШвидкість вітру: "+reply[i][2]+"\nНапрям вітру: "+reply[i][3]+"\nОпади: "+reply[i][4]
            break
    dbworker.set_state(message.chat.id, config.States.S_START.value) 
    bot.send_message(message.chat.id, reply, reply_markup=hide_mark)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_EXPR.value)
def user_entering_expression(message):
    reply=""
    try:
        reply=message.text+"="+str(eval(message.text))
    except:
        reply="Чето пошло не так...\nВозможно делишь на ноль"
    #reply=message.text
    bot.send_message(message.chat.id, reply)
    dbworker.set_state(message.chat.id, config.States.S_START.value)           
            
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CHOOSE_THEME.value)
def user_entering_theme(message):
    reply=grabing.find_news(message.text)#grabing.find_science();#"https://ukr.media/science/"+str(random.randomint(334000,335030)
    bot.send_message(message.chat.id, reply, reply_markup=hide_mark)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: True,content_types=["text"])
def check_text(message):
    reply="";
    if message.text=="Привет":
        bot.send_message(message.chat.id,"HI")
    if message.text[0]=="/":
        if message.text.find("calc")>0:
            #bot.send_message(message.chat.id,"Calculator")
            reply=message.text[6:]
            if len(reply)>0:
                try:
                    reply=reply+"="+str(eval(reply))
                except ValueError:
                    reply="Что-то пошло не так"
                except ZeroDivisionError:
                    reply="Делишь на ноль"
            else:
                reply="Нету уравнения, вводи так:\n/calc 12+6"
        if message.text.find("trans")>0:
            #reply="translate"
            reply=message.text[10:]
            destin=message.text[7:9]
            if len(reply)>0:
                #print(destin)
                print(reply)
                translator = Translator()
                try:
                    reply=translator.translate(reply, dest=destin, src="uk")
                    reply="Переведено як: "+str(reply.text)
                except:
                    reply="Чето пошло не так"
            else:
                reply="Нема слова для переводу\nВводи так: /trans мова_в_яку_переводити слово_для_переводу\nen-англійська\nru-російська\nПриклад: /trans en привіт"
        if message.text.find("say")>0:
            reply=message.text[4:]
            if len(reply)<=0:
                reply="Ты не сказал что мне нужно говорить!\n/say привет. И я отправлю привет"
        bot.send_message(message.chat.id,reply)
    #else:
    #   bot.send_message(message.chat.id,"Я такого не знаю!")
    #elif message.text=="/faq":
    #   bot.send_message(message.chat.id,"I am Forevka BOT!")
    


def telegram_main(n):
    try:
        bot.polling(none_stop=True,timeout=180)
    except:
        traceback_error_string=traceback.format_exc()
        with open("Error.Log", "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<error polling="">>\r\n"+ traceback_error_string + "\r\n<<error polling="">>")
        bot.stop_polling()
        time.sleep(10)
        #telegram_main(1);
        
        
if __name__ == '__main__':
    telegram_main(1);
     #bot.polling(none_stop=True)
