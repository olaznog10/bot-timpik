import requests, json
from dateutil import rrule
from datetime import datetime, timedelta

#cuidado por si hay que hacer url encoding
user = 'olaznog10@gmail.com'
password = '######'

headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cache-control': 'no-cache',
}


def login():
    url = 'http://www.timpik.com/login?user=' + user + '&pass=' + password + '&recordarme=1&logear='
    response = requests.request('POST', url, headers=headers)
    print('login', response)
    return response.cookies


def find_by_day(date, cookies):
    #El cero de provincia creo que es la tuya actual.
    url = 'http://www.timpik.com/events?interestingGamesGetData=1&bt3=1&date=' + str(date) + '&sport=undefined&filter=2&provincia=0'
    response = requests.request('POST', url, headers=headers, cookies=cookies)
    json_events = get_events(response.text.split('\n'))
    event_ids = []
    print('Buscando en el día', current_date, response)
    for event in json_events:
        #Aqui hay que mejorar para que solo se añada los eventos que queremos
        if 'Completo' not in event['evento']['infoCapacity']:
            #120 es gea
            if event['evento']['pro'] != None and event['evento']['pro']['id'] == 120:
                print(current_date, 'Unirme', event['evento']['name'])
                join_event(event['evento']['id'])
            else:
                print(current_date,'Pregunta', event['evento']['name'])
        else:
            print(current_date,'Completo', event['evento']['name'])
    return event_ids


def get_events(lines):
    for line in lines:
        line = line.strip()
        if 'datosEventos' in line:
            return json.loads(line[19:-1])


def join_event(id):
    url = 'http://www.timpik.com/events?joinGame'
    payload = 'evento_id=' + str(id) + '&m=1&update=Aceptar'
    response = requests.request('POST', url, data=payload, headers=headers, cookies=cookies)
    print(response.text)


if __name__ == '__main__':
    cookies = login()
    start_date = datetime.today()
    ten_days = start_date + timedelta(days=10)
    for current_date in rrule.rrule(rrule.DAILY, dtstart=start_date, until=ten_days):
        find_by_day(int(current_date.timestamp()*1000), cookies)