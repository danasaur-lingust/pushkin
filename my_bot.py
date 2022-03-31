import telebot
from telebot import types
import random
import conf     # импортируем наш секретный токен
import re
import io
from pymystem3 import Mystem

bot = telebot.TeleBot(conf.TOKEN)  # создаем экземпляр бота
m = Mystem()

#################### рифмуем!!!! ############################

def rhyme(message):
    with open('result.txt', 'r', encoding='utf') as result:
        tekstcel = result.read()
        tekst = message.text.lower()
        wzor = '([уеыаоэяиюё]*([йцкнгшщзхфвпрлджчсмтбъь]*[уеыаоэяиюё][йцкнгшщзхфвпрлджчсмтбъь]*)[^а-я]*)$'
        wzor2 = '([уеыаоэяиюё]*([йцкнгшщзхфвпрлджчсмтбъь]*[уеыаоэяиюё][йцкнгшщзхфвпрлджчсмтбъь]*))'
        result = re.findall(wzor, tekst)
        print(result)
        if result:
            key = result[0][0]
            print(key)
            key = re.findall(wzor2, key)[0][0]
            key2 = re.findall(wzor2, key)[0][1]
            key = '(.*' + key + '[^а-я]*)\n'
            key2 = '(.*' + key2 + '[^а-я]*)\n'
            result2 = re.findall(key, tekstcel)
            result3 = re.findall(key2, tekstcel)
            print(result2)
            if len(result2) > 0:
                result2 = result2[random.randint(0,len(result2)-1)]
                bot.send_message(message.chat.id, result2)
                print('ONE')
            elif len(result3) > 0:
                result3 = result3[random.randint(0,len(result3)-1)]
                bot.send_message(message.chat.id, result3 + '\n\nну окей получилось похуже но всё равно)))')
                print('TWO')
            else:
                bot.send_message(message.chat.id, 'фіг тобі а не рифма')


############################################################

def lemma_stuff(messaggee):
    keyword = messaggee.text
    with io.open('result.txt', 'r', encoding = 'utf8') as f:
        tekst = f.read()
    with io.open('lexlist.txt','r',encoding='utf8') as f:
        lexlist = f.read().split()
        print('okay')
    with io.open('wordlist.txt','r',encoding='utf8') as f:
        wordlist = f.read().split()
        print('okay')
    print(type(keyword))
    keylemma = m.lemmatize(keyword)
    print('okay', keylemma)
    check = 1
    i = 0
    keyword2 = ''
    while check:
        if lexlist[i] == keylemma[0]:
            keyword2 = wordlist[i]
            print(wordlist[i], 'wellll')
            check = 0
        else:
            i = i+1
            if i >= len(lexlist):
                check = 0
    print(list(keyword2))
    if len(keyword2) > 0:
        print('HEYYYYYYYYYYYYYYY')
        keyword2 = '.*' + keyword2 + '.*'
        result = re.findall(keyword2, tekst)
        result = result[random.randint(0, len(result)-1)]
        bot.send_message(messaggee.chat.id, result)
    else:
        bot.send_message(messaggee.chat.id, 'я нашла розбійника прям перед монитором')


#############################################################
memory=0


@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    print('fuckkkkkkkkkkkkkkkkkkkkkkkk')
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

# функция запустится, когда пользователь нажмет на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call, memory=0):
    if call.message:
        if call.data == "button1":
            message = bot.send_message(call.message.chat.id, "Вы обратились за помощью к Поэтессе. "
                                                             "Пришлите любое сообщение, и поэтесса "
                                                             "подберёт вам 1 причину бросить парня в рифму ^^")
            bot.register_next_step_handler(message, rhyme)
            memory = 1

        if call.data == "button2":
            message = bot.send_message(call.message.chat.id, "Вы обратились за помощью к Следопытке. "
                                                             "Пришлите 1 (одно) слово, и следопытка найдёт "
                                                             "1 причину бросить парня, в которой "
                                                             "будет ваше слово ;)")
            bot.register_next_step_handler(message, lemma_stuff)
            memory = 2
    return memory

@bot.message_handler(content_types=["text"])
def send_reason(message):
    # создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()

    # добавляем на нее две кнопки
    button1 = types.InlineKeyboardButton(text="Поэтесса", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Следопытка", callback_data="button2")
    keyboard.add(button1)
    keyboard.add(button2)

    if memory == 1:
        bot.send_message(message.chat.id, rhyme(message.text))
    elif memory == 2:
        bot.send_message(message.chat.id, lemma_stuff(message.text))

if __name__ == '__main__':
    bot.polling(none_stop=True)
