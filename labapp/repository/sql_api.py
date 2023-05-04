from typing import List

from .connector import StoreConnector


"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""


def select_all_from_source_files(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    query = f'SELECT * FROM source_files ORDER BY processed_date DESC'
    result = connector.execute(query).fetchall()
    return result


def select_rows_from_processed_data(connector: StoreConnector, source_file: int, offset: int = None, limit: int = 10) -> List[tuple]:
    """ Выборка строк из таблицы с обработанными данными.
        offset - смещение строк при выборке.
        limit - количество строк в выбоке.
        Например, при запросе: SELECT * FROM processed_data WHERE source_file = {source_file} LIMIT 20,10
        будет выбрано 10 строк, начиная с 21-ой.
    """
    result = []
    if limit is None or offset is None:
        result = connector.execute(f"SELECT * FROM matches WHERE source_file = {source_file}").fetchall()
    else:
        result = connector.execute(f"SELECT * FROM matches WHERE source_file = {source_file} "
                                   f"LIMIT {offset*limit},{limit}").fetchall()
    return result


def get_rows_by_tourney_name(connector: StoreConnector, name: str) -> List[tuple]:
    result = connector.execute(f"SELECT * FROM matches WHERE tourney_name='{name}'").fetchall()
    return result


def get_rows_by_winner_name(self, name: str):
    result = self.execute(f"SELECT * FROM matches WHERE winner_name='{name}'").fetchall()
    return result


def get_rows_by_loser_name(self, name: str):
    result = self.execute(f"SELECT * FROM matches WHERE loser_name='{name}'").fetchall()
    return result


def get_rows_by_country(self, country: str):
    result = self.execute(f"SELECT * FROM matches WHERE winner_ioc='{country}' OR loser_ioc='{country}'").fetchall()
    return result
