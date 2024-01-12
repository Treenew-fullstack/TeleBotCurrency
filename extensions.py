import requests
import json


vol_keys = {"доллар": "USD",
            "евро": "EUR",
            "рубль": "RUB", }


class APIException(Exception):
    """Материнский класс исключений"""
    pass


class TooManyPar(APIException):
    """Исключение избыточного количества параметров"""
    def __str__(self):
        return "Слишком много параметров! Должно быть 3 параметра"


class IntoYourself(APIException):
    """Исключение конвертации валют самой в себя"""
    def __str__(self):
        return "Невозможно конвертировать валюту саму в себя!)"


class WrongBase(APIException):
    """Исключение ошибок ввода конвертируемой валюты"""
    def __str__(self):
        return "Вы где-то ошиблись в первой валюте!"


class WrongCurrent(APIException):
    """Исключение ошибок ввода валюты в которую конвертируют"""
    def __str__(self):
        return "Вы где-то ошиблись во второй валюте!"


class WrongAmmount(APIException):
    """Исключение ошибок ввода количества валют"""
    def __str__(self):
        return "Что-то не так с количеством валюты!"


class GetAPI:
    """Операция запроса к API с возвратом результата json и операция умножения на количество"""
    @staticmethod
    def get_price(base, curr, ammount):
        r = requests.get(
            f"https://api.currencyapi.com/v3/latest?apikey=cur_live_Pey9s17Gs9ZfmCVZd2uFZrvYjBYAAT4mJuOhOQOa&"
            f"currencies={vol_keys[curr]}&base_currency={vol_keys[base]}")
        return f"{(json.loads(r.content)["data"][vol_keys[curr]]["value"]) * float(ammount)}"
