from typing import List

from config import DB_URL                       # параметры подключения к БД из модуля конфигурации config.py
from .repository import sql_api                 # подключаем API для работы с БД
from .repository.connectorfactory import SQLStoreConnectorFactory

"""
    В данном модуле реализуются бизнес-логика обработки клиентских запросов.
    Здесь также могут применяться SQL-методы, представленные в модуле repository.sql_api
"""

# Структура основного навигационнго меню (<nav>) веб-приложения,
# оформленное в виде объекта dict
navmenu = [
    {
        'name': 'ГЛАВНАЯ',
        'addr': '/'
    },
    {
        'name': 'О НАС',
        'addr': '/about'
    },
    {
        'name': 'КОНТАКТЫ',
        'addr': '/contact'
    },
]


def get_source_files_list() -> List[tuple]:
    """ Получаем список обработанных файлов """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)  # инициализируем соединение
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.select_all_from_source_files(db_connector)  # получаем список всех обработанных файлов
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result


def get_processed_data(source_file: int, page_num: int = None) -> List[tuple]:
    """ Получаем обработанные данные из основной таблицы """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.select_rows_from_processed_data(db_connector, source_file=source_file, offset=page_num)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result


def get_data_by_tourney_name(name: str) -> List[tuple]:
    """ Получаем обработанные данные из основной таблицы """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.get_rows_by_tourney_name(db_connector, name)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result


def get_data_by_winner_name(name: str) -> List[tuple]:
    """ Получаем обработанные данные из основной таблицы """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.get_rows_by_winner_name(db_connector, name)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result


def get_data_by_loser_name(name: str) -> List[tuple]:
    """ Получаем обработанные данные из основной таблицы """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.get_rows_by_loser_name(db_connector, name)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result


def get_data_by_country(country: str) -> List[tuple]:
    """ Получаем обработанные данные из основной таблицы """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.get_rows_by_country(db_connector, country)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result
