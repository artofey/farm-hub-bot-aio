import json

from aiogram import types


def get_data_from_message(message: types.Message) -> dict:
    """
    Получить из сообщения нужные данные и вернуть их в виде словаря
    :param message:
    :return:
    """
    data = dict()
    data['user'] = {
        'id': str(message.from_user.id),
        'user_name': str(message.from_user.username),
    }
    data['market'] = get_resource_from_market_text(str(message.text))
    return data


def get_resource_from_market_text(in_text: str) -> dict:
    resources = dict()
    text = in_text.split('\n\n')[1]  # получили центральный блок
    strings = text.split('\n')
    first_string = strings.pop(0)
    free_slots = get_free_slots(first_string)
    enum_strings = enumerate(strings)
    for idx, string in enum_strings:
        next_string = strings[idx + 1]
        golds = int(next_string.split()[0])
        if string in resources.keys():
            resources[string] = resources[string] + golds
        else:
            resources[string] = golds
        next(enum_strings)
    return {
        'resources': resources,
        'free_slots': free_slots
    }


def get_free_slots(string: str) -> int:
    """
    Получает из строки число свободных слотов на бирже
    :param string:
    :return:
    >>> get_free_slots('Твои предложения (9/12):')
    3
    """
    temp = string.split()[-1][:-1].strip()  # получил значение в скобках
    temp = temp.split('/')  # разрезал скобки  по слешу
    n1 = temp[0][1:]
    n2 = temp[1][:-1]
    return int(n2) - int(n1)


if __name__ == '__main__':
    with open('temp.json', encoding='utf-8') as f:
        data = json.load(f)
    text_ = str(data['text'])
    print(get_resource_from_market_text(text_))
