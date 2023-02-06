
import config
import telebot
from telebot import *
import types
import aiogram
from  aiogram import *


bot = telebot.TeleBot(config.token)

user_num1 = ''
user_num2 = ''
user_proc = ''
result = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Привет" + message.from_user.first_name + ", я калькулятор\n Введите число", reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)

def process_num1_step(message, result = None):
    try:
        global user_num1
        if result == None:
            user_num1 = int(message.text)
        else:
           user_num1 = int(result) 


        markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
        procbtn1 = types.KeyboardButton('+')
        procbtn2 = types.KeyboardButton('-')
        procbtn3 = types.KeyboardButton('*')
        procbtn4 = types.KeyboardButton('/')
        markup.add(procbtn1, procbtn2, procbtn3, procbtn4)

        msg = bot.send_message(message.chat.id, "Выберите опреацию", reply_markup = markup)
        bot.register_next_step_handler(msg, process_proc_step)
    except Exception as e:
        bot.reply_to(message, "Это не число или что-то не так ....")

    def process_proc_step(message):
        try:
            global user_proc
            user_proc = message.text
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(message.chat.id, "Введите второе число", reply_markup=markup)
            bot.register_next_step_handler(msg, process_num2_step)
        except Exception as e:
            bot.reply_to(message, "Вы ввели не число или что-то не так ....")

def process_num2_step(message):
    try:
        global user_num2       
        user_num2 = int(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
        procbtn1 = types.KeyboardButton('Результат')
        procbtn2 = types.KeyboardButton('Продолжить вычисление')
        markup.add(procbtn1, procbtn2)
        msg = bot.send_message(message.chat.id, "Показать результат или продолжить действия?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_continue_step)
    except Exception as e:
        bot.reply_to(message, "Это не число или что-то не так ....")

def process_continue_step(message):
    try:
        culc()
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() == 'результат':
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text.lower() == 'продолжить вычисление':
            process_num1_step(message, result)
    except Exeption as e:
        bot.reply_to(message, "Что-то пошло не так ....")

def calcResultPrint():
    global user_num1, user_num2, user_proc, result
    return "Результат" + str(user_num1) +' '+ user_proc + ' ' + str(user_num2) + '=' + str(result)

def culc():
    global user_num1, user_num2, user_proc, result
    result = eval(str(user_num1) + user_proc + str(user_num2))
    return result

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
#if__name__ == '__main__':
bot.infinity_polling()

