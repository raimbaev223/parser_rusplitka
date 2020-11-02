import requests
from bs4 import BeautifulSoup as BS
import re
import csv
from multiprocessing import Pool
from datetime import datetime



start = datetime.now()
#Получаем ссылки на товары из файла
links = []
with open("catalog_list.txt", 'r') as file:
    for url in file:
        url = url.strip()
        links.append(url)


def get_data():
    data = []
    i = 0
    try:
        for url in links:
            if url == "https://www.rusplitka.ru/catalog/land/":
                pass
            else:
                response = requests.get(url)
                html = response.text
                code = re.findall(r'\d', url)
                join_ = ''
                code_ = join_.join(code)
                code_ = f"Код товара - {code_}"

                soup = BS(html, "html.parser")

                title = soup.find('h1', itemprop="name") #получаем название товаров
                title = title.text

                description = soup.find('div', id="prod") #получаем описание товара
                description = description.text.replace('\n', '')

                price = soup.find('span', class_='bold') #Получаем цены и обрезаем лишнее
                price = price.text[4:]

                specifications = soup.find('ul', class_="list-unstyled attrs").text# full spec
                specs = specifications.replace('	', ' ').replace('\n', ',')
                specs = ' '.join(specs.split())
                print(specs)

                photos_list = []
                photos = soup.find('ul', class_='photos-inner').find_all('a') #получаем количество фото и ссылки на них
                for li in photos:
                    href = li.get('href')
                    href = f"https://www.rusplitka.ru{href}"
                    photos_list.append(href)
                len_photos = f"Количество фото - {len(photos)}"
                i += 1
                size = soup.find('ul', class_="list-inline list-commas inline")#получаем размеры товаров
                size = size.text.replace('\n', '')


                data.append([
                        url,
                        title,
                        code_,
                        description,
                        size,
                        price,
                        len_photos,
                        photos_list
                        ])#записываем данные в список
                with open('all_data.csv', 'w') as file:
                    writer = csv.writer(file)
                    for row in data:
                        writer.writerow((row))

            print("Спарсил " + url + ">>>>>" + str(i))#это чтоб не было скучно смотреть в пустую консоль
        print("Данные записаны в файл")
        return data

    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        get_data()
        end = datetime.now()
        total = end - start
        print(f"Скрипт отработал за {total} секунд")
    except Exception as e:
        print(e)