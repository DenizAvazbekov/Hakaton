import requests
from bs4 import BeautifulSoup
import csv
import time

def get_html(url):
    r = requests.get(url)
    return r.text

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')

    data = []
    for item in items:
        try:
            name = item.find('div', class_='listbox_title').text.strip()
        except:
            name = ''

        try:
            price = item.find('div', class_='listbox_price').find('strong').text.strip().replace(',', '')
        except:
            price = ''

        try:
            img = item.find('div', class_='listbox_img').find('img').get('src')
        except:
            img = ''

        data.append({
            'name': name,
            'price': price,
            'img': img
        })

    return data

def write_csv(data):
    with open('phones.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование', 'Цена', 'Фото'])
        for item in data:
            writer.writerow([item['name'], item['price'], item['img']])

def main():
    url = 'https://www.kivano.kg/mobilnye-telefony'

    while True:
        try:
            html = get_html(url)
            data = get_data(html)
            write_csv(data)
            print('Данные записаны в файл phones.csv')
        except:
            print('Ошибка при парсинге данных')

        time.sleep(3600)  # 1 hour delay before next update

if __name__ == '__main__':
    main()

