import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool


# Получаем все страницы с товаром
def get_all_collections():
    links = []
    link = "https://www.rusplitka.ru/catalog/"

    for i in range(1, 438):  # Первая цифра, начало, вторая количество страниц + 1
        new_link = link + 'page-' + str(i) + '/'
        i += 1
        if i <= 40:
            links.append(new_link)
    return links


# Сохраняем все ссылки на страницы в список, и записываем его в текстовый файл
pages_list = get_all_collections()
with open("pages_list.txt", 'w') as file:
    for line in pages_list:
        file.write(line + '\n')
    file.close()


# Получаем ссылки на все товары
def get_catalog():
    cat_links = []

    for page in pages_list:
        response = requests.get(page)
        html_ = response.text
        soup = BS(html_, "html.parser")
        catalog = soup.find_all('a', class_='title')
        print(f"Распарсил {page}, перехожу к следующей странице.")

        for link in catalog:
            a = link.get('href')
            cat_links.append(a)
    return cat_links


catalog_list = get_catalog()

#Сохраняем ссылки на товары в файл
with open("catalog_list.txt", 'w') as file:
    for line in catalog_list:
        file.write(f"https://www.rusplitka.ru{line}\n")
    file.close()

