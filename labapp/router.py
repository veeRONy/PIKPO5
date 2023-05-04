# Подключаем объект приложения Flask из __init__.py
from labapp import app
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, jsonify

import labapp.webservice as webservice   # подключаем модуль с реализацией бизнес-логики обработки запросов

"""
    Модуль регистрации обработчиков маршрутов, т.е. здесь реализуется обработка запросов
    при переходе пользователя на определенные адреса веб-приложения
"""


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """ Обработка запроса к индексной странице """
    # Пример вызова метода с выборкой данных из БД и вставка полученных данных в html-шаблон
    processed_files = webservice.get_source_files_list()
    # "рендеринг" (т.е. вставка динамически изменяемых данных) в шаблон index.html и возвращение готовой страницы
    return render_template('index.html',
                           title='Статистика теннисных матчей',
                           page_name='СТАТИСТИКА ТЕННИСТНЫХ МАТЧЕЙ',
                           navmenu=webservice.navmenu,
                           processed_files=processed_files)


@app.route('/contact', methods=['GET'])
def contact():
    """ Обработка запроса к странице contact.html """
    return render_template('contact.html',
                           title='Контакты',
                           page_name='КОНТАКТЫ',
                           navmenu=webservice.navmenu)


@app.route('/about', methods=['GET', 'POST'])
def about():
    """ Обработка запроса к странице about.html """
    return render_template('about.html',
                           title='О сайте',
                           page_name='О САЙТЕ',
                           navmenu=webservice.navmenu)


@app.route('/data/<int:source_file_id>', methods=['GET', 'POST'])
def get_data(source_file_id: int):
    """
        Вывод данных по идентификатору обработанного файла.
        Функция также пытается получить значение GET-параметра pageNum
        из запроса типа: http://127.0.0.1:8000/data/16?pageNum=2
    """
    processed_data = []
    pageNum = request.args.get('pageNum')
    if pageNum is not None:
        processed_data = webservice.get_processed_data(source_file=source_file_id, page_num=int(pageNum))
    else:
        processed_data = webservice.get_processed_data(source_file=source_file_id)

    sort_data = request.args.get('sort')
    if sort_data:
        processed_data = sorted(processed_data, key=lambda row: row[3])
        if sort_data == 'down':
            processed_data = processed_data[::-1]

    tourney_name = request.form.get('select_tourney_name')
    winner_name = request.form.get('select_winner_name')
    loser_name = request.form.get('select_loser_name')
    country = request.form.get('select_country')

    if tourney_name:
        processed_data = webservice.get_processed_data(source_file=source_file_id)
        processed_data = webservice.get_data_by_tourney_name(tourney_name)

    if winner_name:
        processed_data = webservice.get_processed_data(source_file=source_file_id)
        processed_data = webservice.get_data_by_winner_name(winner_name)

    if loser_name:
        processed_data = webservice.get_processed_data(source_file=source_file_id)
        processed_data = webservice.get_data_by_loser_name(loser_name)

    if country:
        processed_data = webservice.get_processed_data(source_file=source_file_id)
        processed_data = webservice.get_data_by_country(country)

    return render_template('data.html',
                           title='Статистика теннисных матчей',
                           page_name=f'Статистика теннисных матчей - файл №{source_file_id}',
                           navmenu=webservice.navmenu,
                           processed_data=processed_data)


@app.route('/api/contactrequest', methods=['POST'])
def post_contact():
    """ Пример обработки POST-запроса для демонстрации подхода AJAX (см. formsend.js и ЛР№5 АВСиКС) """
    request_data = request.json     # получаeм json-данные из запроса
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте, например, не заполнено обязательное поле 'firstname'
    if not request_data or request_data['firstname'] == '':
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе отправляем json-ответ с сообщением об успешном получении запроса
    else:
        msg = request_data['firstname'] + ", ваш запрос получен !"
        return jsonify({'message': msg})


@app.route('/notfound', methods=['GET'])
def not_found_html():
    """ Возврат html-страницы с кодом 404 (Не найдено) """
    return render_template('404.html', title='404', err={'error': 'Not found', 'code': 404})


def bad_request():
    """ Формирование json-ответа с ошибкой 400 протокола HTTP (Неверный запрос) """
    return make_response(jsonify({'message': 'Bad request !'}), 400)





tourney_names = {'Atp Cup',
                 'Adelaide',
                 'Melbourne',
                 'Adelaide 2',
                 'Australian Open',
                 'Sydney',
                 'Cordoba'
                 'Montpellier'
                 'Pune'
                 'Buenos Aires'
                 'Rotterdam'
                 'Dallas'
                 'Delray Beach'
                 'Doha'
                 'Rio de Janeiro'
                 'Marseille'
                 'Acapulco'
                 'Dubai'
                 'Santiago'
                 'Indian Wells Masters'
                 'Miami Masters'
                 'Houston'
                 'Marrakech'
                 'Monte Carlo Masters'
                 'Barcelona'
                 'Belgrade'
                 'Estoril'
                 'Munich'
                 'Madrid Masters'
                 'Rome Masters'
                 'Geneva'
                 'Lyon'
                 'Roland Garros'
                 's Hertogenbosch'
                 'Stuttgart'
                 'Halle'
                 'Queens Club'
                 'Mallorca'
                 'Eastbourne'
                 'Wimbledon'
                 'Bastad'
                 'Newport'
                 'Hamburg'
                 'Gstaad'
                 'Atlanta'
                 'Kitzbuhel'
                 'Umag'
                 'Los Cabos'
                 'Washington'
                 'Canada Masters'
                 'Cincinnati Masters'
                 'Winston-Salem'
                 'Us Open'
                 'San Diego'
                 'Metz'
                 'Laver Cup'
                 'Seoul'
                 'Sofia'
                 'Tel Aviv'
                 'Astana'
                 'Tokyo'
                 'Florence'
                 'Gijon'
                 'Naples'
                 'Stockholm'
                 'Antwerp'
                 'Basel'
                 'Vienna'
                 'Paris Masters'
                 'NextGen Finals'
                 'Tour Finals'
                 'Davis Cup Finals RR: ARG vs CRO'
                 'Davis Cup Finals SF: AUS vs CRO'
                 'Davis Cup Finals QF: AUS vs NED'
                 'Davis Cup Finals F: CAN vs AUS'
                 'Davis Cup Finals QF: CRO vs ESP'
                 'Davis Cup Finals SF: ITA vs CAN'
                 'Davis Cup Finals QF: ITA vs US'
                 'Davis Cup QLS R1: ARG vs CZE'
                 'Davis Cup QLS R1: AUS vs HUN'
                 'Davis Cup QLS R1: AUT vs KOR'
                 'Davis Cup QLS R1: BEL vs FIN'
                 'Davis Cup QLS R1: CAN vs NED'
                 'Davis Cup QLS R1: ESP vs ROU'
                 'Davis Cup QLS R1: FRA vs ECU'
                 'Davis Cup QLS R1: GER vs BRA'
                 'Davis Cup QLS R1: ITA vs SVK'
                 'Davis Cup QLS R1: KAZ vs NOR'
                 'Davis Cup QLS R1: KAZ vs NOR'
                 'Davis Cup QLS R1: SWE vs JPN'
                 'Davis Cup QLS R1: USA vs COL'
                 'Davis Cup WG1 R1: AUT vs PAK'
                 'Davis Cup WG1 R1: BIH vs MEX'
                 'Davis Cup WG1 R1: BRA vs POR'
                 'Davis Cup WG1 R1: CHI vs PER'
                 'Davis Cup WG1 R1: COL vs TUR'
                 'Davis Cup WG1 R1: CZE vs ISR'
                 'Davis Cup WG1 R1: ECU vs SUI'
                 'Davis Cup WG1 R1: FIN vs NZL'
                 'Davis Cup WG1 R1: HUN vs UKR'
                 'Davis Cup WG1 R1: IND vs NOR'
                 'Davis Cup WG1 R1: JPN vs UZB'
                 'Davis Cup WG1 R1: SVK vs ROU'
                 'Davis Cup WG1 PO: CHI vs SLO'
                 'Davis Cup WG1 PO: IND vs DEN'
                 'Davis Cup WG1 PO: PAK vs LTU'
                 'Davis Cup WG1 PO: UZB vs TUR'
                 'Davis Cup WG2 R1: BAR vs IRL'
                 'Davis Cup WG2 R1: BOL vs THA'
                 'Davis Cup WG2 R1: DEN vs ESA'
                 'Davis Cup WG2 R1: DOM vs LAT'
                 'Davis Cup WG2 R1: LBN vs MON'
                 'Davis Cup WG2 R1: LTU vs EGY'
                 'Davis Cup WG2 R1: POL vs INA'
                 'Davis Cup WG2 R1: RSA vs BUL'
                 'Davis Cup WG2 R1: SLO vs EST'
                 'Davis Cup WG2 R1: TPE vs HKG'
                 'Davis Cup WG2 R1: TUN vs GRE'
                 'Davis Cup WG2 R1: URU vs CHN'
                 'Davis Cup WG2 PO: EGY vs CYP'
                 'Davis Cup WG2 PO: GRE vs JAM'
                 'Davis Cup WG2 PO: HKG vs BEN'}
