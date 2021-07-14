from glob import glob
import logging
from mybot.parser import parser_wth
from random import randint, choice
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import settings


#PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}
#mybot = Updater('settings.API_KEY', use_context=True, request_kwargs=PROXY)


logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    print('Call /start')
    update.message.reply_text('Дороу')


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Your number: {user_number}\nMy number: {bot_number}\nYou Win'
    elif user_number == bot_number:
        message = f'Your number: {user_number}\nMy number: {bot_number}\nDraw'
    elif user_number < bot_number:
        message = f'Your number: {user_number}\nMy number: {bot_number}\nYou Lose'
    return message


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            massage = play_random_numbers(user_number)
        except (TypeError, ValueError):
            massage = 'Enter an integer'
    else:
        massage = 'Enter number'
    update.message.reply_text(massage)


def send_cat_picture(update, context):
    cat_photos_list = glob('mybot/images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def get_holiday(update, context):
    list_holiday = parser_wth.list_holiday()
    for holiday in list_holiday:
        update.message.reply_text(holiday)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('holiday', get_holiday))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot started', )
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
