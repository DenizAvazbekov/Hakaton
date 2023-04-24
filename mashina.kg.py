from bs4 import BeautifulSoup
import requests
import csv
def code_html(url: str):
    r = requests.get(url)
    return r.text
def code_soup(html: str):
    syp = BeautifulSoup(html, 'html.parser')
    return syp
def get_last_page(soup: BeautifulSoup) -> int:
    page = soup.find('ul', class_='pagination').find_all('a', class_='page-link')
    return int(page[-1].get('data-page'))
def code_data(soup: BeautifulSoup) -> list:
    container = soup.find('div', class_='table-view-list')
    cars = container.find_all('div', class_='list-item')
    result = []
    for car in cars:
        name = car.find('h2', class_='name').text.strip()
        try:
            img = car.find('img', class_='lazy-image').get('data-src')
        except:
            img = 'No image!'
        price_car = car.find('div', class_='block price')
        price = price_car.find('p').text.strip()
        ls = ['year-miles', 'body-type', 'volume']
        desc = ' '.join(car.find('p', class_=x).text.strip() for x in ls)
        data = {
            'name': name, 'desc': desc, 'price': price, 'img': img
        }
        result.append(data)
    return result
def prepare_csv() -> None:
    with open('cars.csv', 'w') as file:
        Stroki = ['Number', 'Name', 'Description', 'Price', 'Image Url']
        writer = csv.DictWriter(file, Stroki)
        writer.writerow({
            'Number': 'Number',
            'Name': 'Name',
            'Description': 'Description',
            'Price': 'Price',
            'Image Url': 'Image Url'
        })
count = 1
def write_to_csv(data: dict) -> None:
    with open('cars.csv', 'a') as file:
        Stroki = ['Number', 'Name', 'Description', 'Price', 'Image Url']
        writer = csv.DictWriter(file, Stroki)
        global count
        for car in data:
            writer.writerow({
            'Number': count,
            'Name': car['name'],
            'Description': car['desc'],
            'Price': car['price'],
            'Image Url': car['img']
        })
        count += 1
def main():
    i = 1
    prepare_csv()
    while True:
        url = f'https://www.mashina.kg/search/all/?page={i}'
        html = code_html(url)
        soup = code_soup(html)
        data = code_data(soup)
        write_to_csv(data)
        last_page = get_last_page(soup)
        print(f'Parsed page {i}/{last_page}!')
        if i == 15: 
            break
        i += 1
if __name__ == '__main__':
    main()
    