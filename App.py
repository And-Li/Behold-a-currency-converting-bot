import telebot
import requests
import json
TOKEN = '1752137763:AAEBho_l-VPWnqtMcK7spXB8PrTv6Z18fUI'
bot = telebot.TeleBot(TOKEN)
keys = {'bitcoin': 'BTC', 'etherium': 'ETH', 'dollar': 'USD', }


class ConvertException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('Too many parameters')

        if quote == base:
            raise ConvertException(f'Impossible to convert the same currency {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту{quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту{base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количесвто {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base

@bot.message_handler(commands=['start', 'help'])
def helper(message):
    text = 'Чтобы начать работу - введите команду боту в следующем формате: \n<Имя валюты> \
<В какую валюту перевести><Количество переводимой валюты>\n \
Увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  # Выводит список валют
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    if len(values) != 3:
        raise ConvertException('Too many parameters')
    quote, base, amount = values
    total_base = CryptoConverter.convert(quote, base, amount)
    text = f'Price of {amount} {quote} in {base}s - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()
