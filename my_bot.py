import telebot
from telebot import types
import conf     # импортируем наш секретный токен
import re
import io

bot = telebot.TeleBot(conf.TOKEN)  # создаем экземпляр бота


#################### рифмуем!!!! ############################

@bot.message_handler()
def rhyme(message):
    print(message.text)
    with open('result.txt', 'r', encoding='utf') as result:
        tekstcel = result.read()
        print(tekstcel)
        tekst = message.text.lower()
        wzor = '(([уеыаоэяиюё][йцкнгшщзхфвпрлджчсмтбъь]*)*[уеыаоэяиюё][йцкнгшщзхфвпрлджчсмтбъь]*[^а-я]*)$'
        wzor2 = '(([уеыаоэяиюё][йцкнгшщзхфвпрлджчсмтбъь]*)*[уеыаоэяиюё][йцкнгшщзхфвпрлджчсмтбъь]*)'
        result = re.findall(wzor, tekst)
        print(result)
        key = result[0][0]
        print(key)
        key = re.findall(wzor2, key)[0][0]
        print(key)
        key = '(.*' + key + '[^а-я]*)\n'
        print(key)
        result2 = re.findall(key, tekstcel)
        print(result2)
        if len(result2) == 0:
            bot.send_message(message.chat.id, 'пізда тобі а не рифма')
        else:
            result2 = result2[0]
            bot.send_message(message.chat.id, result2)
        # return result2


############################################################

FILENAME = 'result.txt'

def lemma_stuff(FILENAME, USERS_INPUT):
    with io.open(FILENAME, 'r', encoding = 'utf8') as f:
        tekst = f.read()
    with io.open('lexlist.txt','r',encoding='utf8') as f:
        lexlist = f.read().split()
    with io.open('wordlist.txt','r',encoding='utf8') as f:
        wordlist = f.read().split()
    keyword = USERS_INPUT
    keylemma = m.lemmatize(keyword)[0]
    check = 1
    i = 0
    keyword2 = ''
    while check:
        if lexlist[i] == keylemma:
            keyword2 = wordlist[i]
            check = 0
        else:
            i = i+1
    if keyword2 != '':
        keyword2 = '.*' + keyword2 + '.*'
        result = re.findall(keyword2, tekst)[0]
        return result
    else:
        return 'упс сорямба я не нашла ничего'


#############################################################

@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    # создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()

    # добавляем на нее две кнопки
    button1 = types.InlineKeyboardButton(text="Поэтесса", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Следопытка", callback_data="button2")
    keyboard.add(button1)
    keyboard.add(button2)

    # отправляем сообщение пользователю
    bot.send_message(message.chat.id, "Привет, чувачок/чувакесса,\nэтот бот поможет тебе найти 13 причин "
                                      "почему тебе стоит бросить парня. Даже если у тебя нет парня. Это не так важно."
                                      "\n\nУ бота есть две ассистентки, которые готовы помочь тебе сделать"
                                      "важное решение. Выбирай :)", reply_markup=keyboard)
memory=0

# функция запустится, когда пользователь нажмет на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call, memory=0):
    if call.message:
        if call.data == "button1":
            message = bot.send_message(call.message.chat.id, "Вы обратились за помощью к Поэтессе. Пришлите любое сообщение,"
                                                   "и поэтесса подберёт вам 1 причину бросить парня __в рифму__ ^^")
            print(message)
            bot.register_next_step_handler(message, rhyme)
            memory = 1

        if call.data == "button2":
            message = bot.send_message(call.message.chat.id, "Вы обратились за помощью к Следопытке. Пришлите 1 (одно) слово,"
                                                   "и следопытка найдёт 1 причину бросить парня, в которой"
                                                   "будет ваше слово ;)")
            print(message)
            bot.register_next_step_handler(message, rhyme)
            memory = 2
    return memory

@bot.message_handler(content_types=["text"])
def send_reason(message):
    if memory == 1:
        bot.send_message(message.chat.id, rhyme(message.text))
    if memory == 2:
        bot.send_message(message.chat.id, lemma_stuff('results.txt', message.text))

if __name__ == '__main__':
    bot.polling(none_stop=True)
