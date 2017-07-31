import requests, json
from dateutil import rrule
from datetime import datetime, timedelta
from random import randint

#cuidado por si hay que hacer url encoding
user = ['olaznog10@gmail.com', 'olaznog10@gmail.com', 'olaznog10@gmail.com']
password = ['######', '######', '######']
cookies = ['', '', '']

headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cache-control': 'no-cache',
}


def login(pos):
    url = 'http://www.timpik.com/login?user=' + user[pos] + '&pass=' + password[pos] + '&recordarme=1&logear='
    response = requests.request('POST', url, headers=headers)
    print('login', response)
    cookies[pos] = response.cookies


def find_by_day(date, pos):
    #El cero de provincia creo que es la tuya actual.
    url = 'http://www.timpik.com/events?interestingGamesGetData=1&bt3=1&date=' + str(date) + '&sport=undefined&filter=2&provincia=0'
    response = requests.request('POST', url, headers=headers, cookies=cookies[pos])
    json_events = get_events(response.text.split('\n'))
    event_ids = []
    print('Buscando en el día', current_date, response)
    for event in json_events:
        #Aqui hay que mejorar para que solo se añada los eventos que queremos
        if 'Completo' not in event['evento']['infoCapacity']:
            #120 es gea
            if event['evento']['pro'] is not None and event['evento']['pro']['id'] == 120:
                print(current_date, 'Unirme', event['evento']['name'])
                for i in range(len(user) - 1):
                    if cookies[i] is None:
                        login(i)
                    join_event(event['evento']['id'], i)
            else:
                print(current_date,'Pregunta', event['evento']['name'])
        else:
            print(current_date, 'Completo', event['evento']['name'])

def get_events(lines):
    for line in lines:
        line = line.strip()
        if 'datosEventos' in line:
            #el 19 es para quitar la inicializacion y el -1 quita el ;
            return json.loads(line[19:-1])


def join_event(id, pos):
    url = 'http://www.timpik.com/events?joinGame'
    payload = 'evento_id=' + str(id) + '&m=1&update=Aceptar'
    response = requests.request('POST', url, data=payload, headers=headers, cookies=cookies[pos])
    print(response.text)


if __name__ == '__main__':
    pos = randint(0, len(user)-1)
    login(pos)
    start_date = datetime.today()
    next_days = start_date + timedelta(days=3)
    for current_date in rrule.rrule(rrule.DAILY, dtstart=start_date, until=next_days):
        find_by_day(int(current_date.timestamp()*1000), pos)