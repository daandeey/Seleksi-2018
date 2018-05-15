from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

def make_dict(flight_infos):
    result = dict()
    result['result'] = []
    for flight_info in flight_infos:
        for data in flight_info:
            ticket = dict()
            ticket["flight_id"] = data[0]
            ticket["airlines"] = data[1]
            ticket["price"] = data[2]
            ticket["dep_city"] = data[3]
            ticket["dep_time"] = data[4]
            ticket["arr_city"] = data[5]
            ticket["arr_time"] = data[6]
            result["result"].append(ticket)
    return result

def generate_url(range_date, dep_city, arr_city):
    urls = []
    
    for city in arr_city:
        for date in range_date:
            url = 'https://www.tiket.com/pesawat/cari?d=' + dep_city + '&a=' + city + '&date=' 
            url += date + '&adult=1&child=0&infant=0'
            urls.append(url)
    
    return urls

def get_flight_infos(url):
    flight_infos = []
    data_names = ['data-airlines', 'data-airlinesname', 'data-price']

    page = urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find_all('tr', {'class' : 'flight-rows'}) 
    
    for row in rows:
        td3 = row.find('td', {'class' : 'td3'})
        arr_city = td3.find('h5').text
        arr_time = td3.find('h4').text
        td2 = row.find('td', {'class' : 'td2'})
        dep_city = td2.find('h5').text
        dep_time = td2.find('h4').text
        
        datas = [row.get(data) for data in data_names]
        datas.append(dep_city)
        datas.append(dep_time)
        datas.append(arr_city)
        datas.append(arr_time)
        flight_infos.append(datas)
        
    return flight_infos

def print_flight_infos(flight_infos):
    for data in flight_infos:
        print(data)

dep_city = 'CGK'
arr_city = ['DPS', 'BDO']
range_date = ['2018-05-16','2018-05-17','2018-05-18']
flight_infos_all = []

urls = generate_url(range_date, dep_city, arr_city)
for url in urls:
    print(url)
    flight_infos_all.append(get_flight_infos(url))
    print_flight_infos(get_flight_infos(url))
    print()
    print()
    
result = make_dict(flight_infos_all)
with open('data.json', 'w') as outfile:
    json.dump(result, outfile)
