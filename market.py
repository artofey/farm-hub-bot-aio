import json

from aiogram import types

from app.models import User, Market, Resource
from app.db import get_or_create, Session, Base, engine


def get_all_markets():
    session = Session()
    all_markets = session.query(Market).all()
    markets = {mrkt.user.user_name: [] for mrkt in all_markets}
    strings_markets = []
    for market in all_markets:
        markets[market.user.user_name].append(f'{market.resource.name} - {market.count}')

    for key, value in markets.items():
        strings_markets.append(f'@{key}')
        for line in value:
            strings_markets.append(line)
        strings_markets.append('\n')

    return '\n'.join(strings_markets) or 'None'


def save_market_to_db(msg_data: dict):
    """
    - Получить запись текущего юзера (запрос в базу по имени и взять одну запись,
        если исключение что нет записи, то создать юзера нового)
    - Получить все записи маркетов текущего юзера
    -
    :return:
    """
    print('----now------')
    print(msg_data)
    session = Session()
    user = get_or_create(session, User, user_name=msg_data['user']['user_name'])
    user.free_slots = int(msg_data['market']['free_slots'])
    user.telegram_id = int(msg_data['user']['telegram_id'])
    user.name = str(msg_data['user']['name'])

    all_markets_user = session.query(Market).filter_by(user=user).all()
    # удалить все магазины текущего юзера из базы
    for market in all_markets_user:
        session.delete(market)
    session.commit()
    res_dict = msg_data['market']['resources']
    current_resources = [get_or_create(session, Resource, name=resource) for resource in res_dict.keys()]
    current_markers = [Market(user=user,
                              resource=res,
                              count=res_dict[res.name],
                              last_update=msg_data['user']['last_update']) for res in current_resources]
    session.add_all(current_markers)
    session.commit()


def get_data_from_message(message: types.Message) -> dict:
    """
    Получить из сообщения нужные данные и вернуть их в виде словаря
    :param message:
    :return:
    """
    data = dict()
    data['user'] = {
        'telegram_id': str(message.from_user.id),
        'user_name': str(message.from_user.username),
        'name': str(message.from_user.full_name),
        'last_update': int(message.date.timestamp()),
    }
    data['market'] = get_resource_from_market_text(str(message.text))
    return data


def get_resource_from_market_text(market_text: str) -> dict:
    """ Получить словарь со списком ресурсов и свободными слотами из текста биржи """
    resources = dict()
    text = market_text.split('\n\n')[1]  # получили центральный блок
    strings = text.split('\n')
    first_string = strings.pop(0)
    free_slots = get_free_slots(first_string)
    enum_strings = enumerate(strings)
    for idx, string in enum_strings:
        next_string = strings[idx + 1]
        count = int(next_string.split()[0])
        if string in resources.keys():
            resources[string] = resources[string] + count
        else:
            resources[string] = count
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
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with open('temp.json', encoding='utf-8') as f:
        data = json.load(f)
    text_ = str(data['text'])
    print(get_resource_from_market_text(text_))
    new_data = dict()
    new_data['user'] = {
        'telegram_id': str(data['from']['id']),
        'user_name': str(data['from']['username']),
        'name': str(data['from']['first_name']),
        'last_update': int(data['date']),
    }
    new_data['market'] = get_resource_from_market_text(str(data['text']))

    # save_market_to_db(new_data)
    print(get_all_markets())
