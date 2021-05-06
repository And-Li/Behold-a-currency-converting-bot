import telebot
from utils import APIException, CryptoConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message):
    text = 'To begin converting input commands divided by spaces in next order : \n<Currency name you need to convert> \
<Currency you need to convert into><The amount>\n \
To see the list of available currencies: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  # Выводит список валют
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('You should have given 3 parameters!\nRead the /help')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'User error: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Failed to process the operation of \n{e}')
    else:
        text = f'Price of {amount} {quote} in {base}s - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
