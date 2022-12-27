import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)





@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветствую тебя, молодой человечек!\n\
Этот бот создан для того, чтобы тебе было удобнее \
конвертировать валюту и не искать подходящие сайты. \
С помощью команд "/start" и "/help", вы можете получить \
всю необходимую инофрмацию заново. Команда "/values" \
покажет все доступные валюты. Для конвертации валюты \
запишите данные в формате <исходная валюта> <желаемая валюта> \
<количество исходной валюты>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount)}'

        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)


