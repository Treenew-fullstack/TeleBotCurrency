import telebot
import extensions
import Token

TOKEN = Token.TOKEN

bot = telebot.TeleBot(TOKEN)

vol_keys = extensions.vol_keys


@bot.message_handler(commands=["start", "help"])
def welcome(message):
    bot.send_message(message.chat.id, f"Приветствую Вас! Я могу конвертировать разные валюты в разном количестве!"
                            f"\n \nЧтобы я это осуществил, в сообщении необходимо ввести через пробел валюту, которую"
                            f" необходимо конвертировать, валюту, В которую необходимо конвертировать, а затем "
                            f"необходимое количество конвертируемой валюты!(Всё с прописной буквы!!!)\n \n"
                            f"После ввода отправьте сообщение\n\n!"
                            f"Посмотреть список валют для конвертации - комманда /values")


@bot.message_handler(commands=["values"])
def values_list(message):
    text = "Я умею конвертировать:"
    for key in vol_keys.keys():
        text = "\n".join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text",])
def convert(message: telebot.types.Message):

    try:
        vol_len = message.text.split(" ")
        if 3 != len(vol_len):
            raise extensions.TooManyPar
        base, curr, ammount = vol_len
        if base == curr:
            raise extensions.IntoYourself
        try:
            vol_keys[base]
        except:
            raise extensions.WrongBase
        try:
            vol_keys[curr]
        except:
            raise extensions.WrongCurrent
        try:
            float(ammount)
        except:
            raise extensions.WrongAmmount
        base_vol = vol_keys[base]
        curr_vol = vol_keys[curr]
    except extensions.APIException as er:
        bot.reply_to(message, f"У Вас ОШИБКА!\n{er}")
    except Exception as er:
        bot.reply_to(message, f"Не удалось совершить операцию\n{er}")
    else:
        text = f"{ammount} {base_vol} равно {extensions.GetAPI.get_price(base, curr, ammount)} {curr_vol}"
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
